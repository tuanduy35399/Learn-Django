import random
import cv2
import os
import glob
import numpy as np

def load_yolo_labels(label_path, img_w, img_h):
    """Đọc file .txt theo chuẩn YOLO (normalized) và chuyển sang hệ pixel của ảnh gốc"""
    bboxes = []
    if not os.path.exists(label_path):
        return bboxes 
        
    with open(label_path, 'r') as f:
        for line in f.readlines():
            line = line.strip().split()
            if len(line) == 5:
                cls_id = int(line[0])
                x_c, y_c, w, h = map(float, line[1:])
                
                pixel_x_c = x_c * img_w
                pixel_y_c = y_c * img_h
                pixel_w = w * img_w
                pixel_h = h * img_h
                
                bboxes.append([cls_id, pixel_x_c, pixel_y_c, pixel_w, pixel_h])
    return bboxes

def mosaic_augmentation(all_img_list, all_label_list, output_size=(640, 640), scale_range=(0.4, 0.6), filter_scale=10):
    """Bốc ngẫu nhiên 4 ảnh và tiền xử lý Mosaic"""
    out_h, out_w = output_size
    output_img = np.zeros([out_h, out_w, 3], dtype=np.uint8)
    
    # 1. Bốc ngẫu nhiên ngẫu nhiên 4 chỉ mục ảnh từ Dataset
    idxs = random.sample(range(len(all_img_list)), 4)
    
    # 2. Tạo tâm cắt ngẫu nhiên cho Mosaic
    scale_x = random.uniform(scale_range[0], scale_range[1])
    scale_y = random.uniform(scale_range[0], scale_range[1])
    divid_point_x = int(scale_x * out_w)
    divid_point_y = int(scale_y * out_h)

    new_anno = []
    
    # 3. Ghép 4 ảnh vào 4 góc
    for i, idx in enumerate(idxs):
        img_path = all_img_list[idx]
        lbl_path = all_label_list[idx]

        img = cv2.imread(img_path)
        if img is None: continue
        img_h, img_w, _ = img.shape
        
        # Tải bboxes hệ pixel của ảnh này
        img_annos = load_yolo_labels(lbl_path, img_w, img_h)
        
        # Xác định vị trí từng góc
        if i == 0:    # Top-Left
            target_w, target_h = divid_point_x, divid_point_y
            x_offset, y_offset = 0, 0
        elif i == 1:  # Top-Right
            target_w, target_h = out_w - divid_point_x, divid_point_y
            x_offset, y_offset = divid_point_x, 0
        elif i == 2:  # Bottom-Left
            target_w, target_h = divid_point_x, out_h - divid_point_y
            x_offset, y_offset = 0, divid_point_y
        elif i == 3:  # Bottom-Right
            target_w, target_h = out_w - divid_point_x, out_h - divid_point_y
            x_offset, y_offset = divid_point_x, divid_point_y

        # Resize ảnh con dán vào canvas lớn
        img_resized = cv2.resize(img, (target_w, target_h))
        output_img[y_offset:y_offset+target_h, x_offset:x_offset+target_w, :] = img_resized
        
        # Tính tỷ lệ co dãn riêng cho từng góc
        gain_x = target_w / img_w
        gain_y = target_h / img_h
        
        # Tính toán lại tọa độ Box cho ảnh Canvas lớn (Đơn vị: Pixel)
        for bbox in img_annos:
            cls_id = bbox[0]
            xmin = bbox[1] - bbox[3] * 0.5
            ymin = bbox[2] - bbox[4] * 0.5
            xmax = bbox[1] + bbox[3] * 0.5
            ymax = bbox[2] + bbox[4] * 0.5

            # Áp tỷ lệ và cộng thêm độ lệch vị trí (Offset)
            new_xmin = max(0, min(xmin * gain_x + x_offset, out_w))
            new_ymin = max(0, min(ymin * gain_y + y_offset, out_h))
            new_xmax = max(0, min(xmax * gain_x + x_offset, out_w))
            new_ymax = max(0, min(ymax * gain_y + y_offset, out_h))
            
            new_w = new_xmax - new_xmin
            new_h = new_ymax - new_ymin

            # Lọc bỏ box lỗi hoặc bị cắt mất hoàn toàn
            if new_w > filter_scale and new_h > filter_scale:
                new_anno.append([cls_id, int(new_xmin), int(new_ymin), int(new_xmax), int(new_ymax)])

    return output_img, new_anno

def save_mosaic_result(img, annos, output_img_dir, output_lbl_dir, file_idx, output_size=(640, 640)):
    """Chuyển đổi ngược nhãn về dạng Normalize YOLO và tiến hành lưu file"""
    out_h, out_w = output_size
    
    # Định dạng tên file xuất ra (ví dụ: mosaic_00001.jpg / .txt)
    base_filename = f"mosaic_{file_idx:05d}"
    img_save_path = os.path.join(output_img_dir, f"{base_filename}.jpg")
    lbl_save_path = os.path.join(output_lbl_dir, f"{base_filename}.txt")
    
    # 1. Lưu hình ảnh
    cv2.imwrite(img_save_path, img)
    
    # 2. Chuẩn hóa lại tọa độ và lưu file nhãn .txt
    with open(lbl_save_path, 'w') as f:
        for anno in annos:
            cls_id, xmin, ymin, xmax, ymax = anno
            
            # Tính lại tâm (x_center, y_center) và kích thước (w, h) ở hệ Pixel
            x_center = (xmin + xmax) / 2.0
            y_center = (ymin + ymax) / 2.0
            w = xmax - xmin
            h = ymax - ymin
            
            # Chia cho kích thước ảnh output để Normalize (về khoảng 0 -> 1)
            x_center_norm = x_center / out_w
            y_center_norm = y_center / out_h
            w_norm = w / out_w
            h_norm = h / out_h
            
            # Ghi vào file theo đúng cấu trúc chuẩn YOLO
            f.write(f"{cls_id} {x_center_norm:.6f} {y_center_norm:.6f} {w_norm:.6f} {h_norm:.6f}\n")

# ==================== CẤU HÌNH VÀ VẬN HÀNH VÒNG LẶP TẠO ẢNH ====================
if __name__ == "__main__":
    
    # 1. Cấu hình thư mục ĐẦU VÀO (Gốc)
    IMAGE_DIR = "../train/images" 
    LABEL_DIR = "../train/labels" 
    
    # 2. Cấu hình thư mục ĐẦU RA (Nơi lưu ảnh và nhãn Mosaic mới tạo)
    OUTPUT_IMAGE_DIR = "../train/mosaic_images"
    OUTPUT_LABEL_DIR = "../train/mosaic_labels"
    
    # 3. SỐ LƯỢNG ẢNH MOSAIC BẠN MUỐN TẠO RA
    NUM_MOSAIC_TO_GENERATE = 100  # Bạn có thể đổi thành 100, 500, 1000 tùy ý
    
    # Tạo các thư mục đầu ra nếu chúng chưa tồn tại
    os.makedirs(OUTPUT_IMAGE_DIR, exist_ok=True)
    os.makedirs(OUTPUT_LABEL_DIR, exist_ok=True)
    
    # Quét dữ liệu đầu vào
    valid_extensions = ("*.jpg", "*.jpeg", "*.png", "*.bmp")
    all_img_list = []
    for ext in valid_extensions:
        all_img_list.extend(glob.glob(os.path.join(IMAGE_DIR, ext)))
    all_img_list.sort()
    
    all_label_list = []
    for img_p in all_img_list:
        base_name = os.path.splitext(os.path.basename(img_p))[0]
        lbl_p = os.path.join(LABEL_DIR, f"{base_name}.txt")
        all_label_list.append(lbl_p)

    num_total_images = len(all_img_list)
    print(f"Tìm thấy tổng cộng: {num_total_images} ảnh trong thư mục nguồn.")

    if num_total_images < 4:
        print("Lỗi: Thư mục nguồn phải có tối thiểu 4 ảnh trở lên để chạy Random Mosaic!")
    else:
        print(f"Bắt đầu tiến trình tạo {NUM_MOSAIC_TO_GENERATE} ảnh Mosaic ngẫu nhiên...")
        
        # Vòng lặp chạy sinh dữ liệu tự động theo số lượng yêu cầu
        for count in range(1, NUM_MOSAIC_TO_GENERATE + 1):
            # Hàm sinh Mosaic (Mỗi lần gọi vòng lặp sẽ pick random 4 ảnh mới hoàn toàn)
            mosaic_img, updated_annotations = mosaic_augmentation(
                all_img_list, all_label_list, output_size=(640, 640), scale_range=(0.4, 0.6)
            )
            
            # Lưu cả ảnh và file nhãn chuẩn YOLO vào folder đích
            save_mosaic_result(
                mosaic_img, updated_annotations, 
                OUTPUT_IMAGE_DIR, OUTPUT_LABEL_DIR, 
                file_idx=count, output_size=(640, 640)
            )
            
            if count % 10 == 0 or count == NUM_MOSAIC_TO_GENERATE:
                print(f" Tiến độ: Đã xử lý và lưu thành công {count}/{NUM_MOSAIC_TO_GENERATE} ảnh.")
                
        print(f"\n Hoàn thành! Kiểm tra kết quả tại:")
        print(f" -> Thư mục ảnh: {OUTPUT_IMAGE_DIR}")
        print(f" -> Thư mục nhãn: {OUTPUT_LABEL_DIR}")