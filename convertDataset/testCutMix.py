import cv2
import numpy as np
import os
import random
from pathlib import Path

# --- CẤU HÌNH ĐƯỜNG DẪN FOLDER ---
FOLDER_DISEASE = Path("../train/diseases") # Chứa ảnh đốm bệnh đã xóa nền (Folder 1)
FOLDER_IMAGES  = Path("../train/test")     # Chứa ảnh gốc cần cutmix (Folder 2)

# Thư mục xuất ảnh kết quả
OUTPUT_IMAGES  = Path("../train/cutmix_images")
OUTPUT_IMAGES.mkdir(exist_ok=True)


def create_leaf_mask(image):
    """
    [NÂNG CẤP CHỐNG LỆCH HẬU CẢNH MỜ]
    Kết hợp lọc màu HSV và loại bỏ vùng mất nét (Xóa phông/Bokeh) bằng toán tử Gradient/Độ tương phản.
    """
    # 1. Khử nhiễu nhẹ ảnh gốc
    blurred_img = cv2.GaussianBlur(image, (3, 3), 0)
    
    # 2. Lọc dải màu xanh bằng HSV như cũ
    hsv = cv2.cvtColor(blurred_img, cv2.COLOR_BGR2HSV)
    lower_green = np.array([35, 35, 40]) # Nới nhẹ một chút dải màu
    upper_green = np.array([90, 255, 255])
    color_mask = cv2.inRange(hsv, lower_green, upper_green)
    
    # 3. [BƯỚC ĐỘT PHÁ] Tìm các vùng có cấu trúc gân lá sắc nét (Tiền cảnh)
    # Vùng hậu cảnh bị mờ (bị xóa phông) sẽ có giá trị Laplacian rất thấp
    gray = cv2.cvtColor(blurred_img, cv2.COLOR_BGR2GRAY)
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)
    laplacian = np.uint8(np.absolute(laplacian))
    
    # Tạo ngưỡng để giữ lại vùng có độ sắc nét cao (gân lá, biên lá)
    _, sharp_mask = cv2.threshold(laplacian, 10, 255, cv2.THRESH_BINARY)
    
    # Đóng kín các vùng sắc nét để tạo khối thân lá
    kernel_sharp = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
    sharp_mask_closed = cv2.morphologyEx(sharp_mask, cv2.MORPH_CLOSE, kernel_sharp)
    
    # 4. Giao hai mặt nạ: Phải VỪA CÓ MÀU XANH, VỪA PHẢI SẮC NÉT (Không bị mờ nhòe)
    final_mask = cv2.bitwise_and(color_mask, sharp_mask_closed)
    
    # 5. Dọn dẹp lại mặt nạ cuối cùng
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    final_mask = cv2.morphologyEx(final_mask, cv2.MORPH_CLOSE, kernel)
    final_mask = cv2.morphologyEx(final_mask, cv2.MORPH_OPEN, kernel)
    
    return final_mask


def get_safe_random_point_in_mask(mask, disease_shape):
    """
    Sử dụng Distance Transform để tìm vùng lõi sâu bên trong thân lá,
    bắt buộc tâm dán phải cách xa rìa lá một khoảng bằng kích thước đốm bệnh.
    """
    h_dis, w_dis = disease_shape[:2]
    # Tăng thêm biên an toàn lên +10 pixel để đốm bệnh lùi sâu vào trong tâm lá hơn
    safe_radius = max(h_dis, w_dis) // 2 + 10

    dist_transform = cv2.distanceTransform(mask, cv2.DIST_L2, 5)

    _, safe_zone = cv2.threshold(dist_transform, safe_radius, 255, cv2.THRESH_BINARY)
    safe_zone = safe_zone.astype(np.uint8)

    coordinates = np.argwhere(safe_zone > 0)

    if len(coordinates) == 0:
        # Dự phòng nếu không tìm được lõi sâu, lấy thân lá thường nhưng thụt lề biên cố định
        coordinates = np.argwhere(mask > 0)
        if len(coordinates) == 0:
            return None

    y, x = random.choice(coordinates)
    return int(x), int(y)


def run_multi_object_cutmix(current_idx=1, total=100, min_diseases=2, max_diseases=5):
    """
    Hàm xử lý CutMix gán ĐA DẠNG NHIỀU VẾT BỆNH lên cùng 1 tấm ảnh.
    """
    disease_files = list(FOLDER_DISEASE.glob("*.*"))
    image_files = list(FOLDER_IMAGES.glob("*.*"))
    
    if not disease_files or not image_files:
        print("⚠️ Không tìm thấy dữ liệu ảnh đầu vào ở Folder 1 hoặc Folder 2!")
        return False 

    img_path = random.choice(image_files)
    bg_img = cv2.imread(str(img_path))
    h_bg, w_bg = bg_img.shape[:2]

    # Tự động tạo mask cải tiến (HSV + Laplacian Sharpness)
    bg_mask = create_leaf_mask(bg_img)

    num_spots_to_paste = random.randint(min_diseases, max_diseases)
    
    output_img = bg_img.copy()
    spots_pasted_successfully = 0

    for _ in range(num_spots_to_paste):
        dis_path = random.choice(disease_files)
        disease_img = cv2.imread(str(dis_path), cv2.IMREAD_UNCHANGED)
        
        target_point = get_safe_random_point_in_mask(bg_mask, disease_img.shape)
        if target_point is None:
            continue 

        center_x, center_y = target_point
        h_dis, w_dis = disease_img.shape[:2]

        x1 = max(0, center_x - w_dis // 2)
        y1 = max(0, center_y - h_dis // 2)
        x2 = min(w_bg, x1 + w_dis)
        y2 = min(h_bg, y1 + h_dis)
        
        crop_w, crop_h = x2 - x1, y2 - y1
        if crop_w <= 0 or crop_h <= 0:
            continue
        
        disease_crop = disease_img[0:crop_h, 0:crop_w]
        roi = output_img[y1:y2, x1:x2]

        if disease_crop.shape[-1] == 4:
            dis_mask = disease_crop[:, :, 3]
            dis_rgb = disease_crop[:, :, :3]
        else:
            dis_gray = cv2.cvtColor(disease_crop, cv2.COLOR_BGR2GRAY)
            _, dis_mask = cv2.threshold(dis_gray, 10, 255, cv2.THRESH_BINARY)
            dis_rgb = disease_crop

        # Thu nhỏ mask gọt viền lem
        kernel = np.ones((3, 3), np.uint8)
        dis_mask_eroded = cv2.erode(dis_mask, kernel, iterations=1)

        # Làm mờ biên hòa trộn mịn
        mask_blur = cv2.GaussianBlur(dis_mask_eroded, (5, 5), 0)

        alpha = mask_blur.astype(float) / 255.0
        alpha = np.expand_dims(alpha, axis=2)

        roi_blended = dis_rgb.astype(float) * alpha + roi.astype(float) * (1.0 - alpha)
        roi_blended = np.clip(roi_blended, 0, 255).astype(np.uint8)

        output_img[y1:y2, x1:x2] = roi_blended
        spots_pasted_successfully += 1

    if spots_pasted_successfully == 0:
        print(f"⚠️ Bỏ qua ảnh {img_path.name}: Không thể định vị vùng lá sắc nét.")
        return False

    rand_id = random.randint(1000, 9999)
    out_img_name = f"cutmix_multi_{img_path.stem}_{rand_id}.jpg"
    cv2.imwrite(str(OUTPUT_IMAGES / out_img_name), output_img)

    print(f"[{current_idx}/{total}] Đã xuất thành công: {out_img_name} (Đã dán {spots_pasted_successfully} vết bệnh)")
    return True


if __name__ == "__main__":
    N = 100
    print(f"🚀 Bắt đầu sinh {N} ảnh dữ liệu tăng cường (Đã sửa lỗi lệch bokeh)...")
    
    success_count = 0
    attempts = 0
    
    while success_count < N:
        attempts += 1
        success = run_multi_object_cutmix(current_idx=success_count + 1, total=N, min_diseases=2, max_diseases=5)
        if success:
            success_count += 1
            
        if attempts > N * 5: 
            print("⚠️ Chương trình dừng sớm do bốc ảnh lỗi quá số lần quy định.")
            break
            
    print(f"🎉 Hoàn thành! Kiểm tra ngay thư mục 'cutmix_images'.")