from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.
class Client(models.Model):
    # Cách cũ
    # GENDER= [
    #     # (gia_tri_luu_db, gia_tri_hien_thi)
    #     ("male", "Male"), # dung tuple vi no co tinh bat bien, khong the sua doi
    #     ("female", "Female"), #toi uu hoa bo nho, tuple truy xuat nhanh
    # ]
    #Cách mới dùng ENUM 
    class Gender(models.IntegerChoices): # neu dung 1 con so de thay cho chu male thi chuyen sang dung IntegerChoices thay vi TextChoices
        MALE= 1, _("Male")
        FEMALE = 0, _("Female") #lưu số vào db để tiết kiệm dữ liệu
        #dùng enum để đồng nhất, viết logic ở các file view, test không cần ghi rõ chuỗi "male" nữa
    name = models.CharField(_("Ten"),blank=False, max_length=200)
    gender= models.IntegerField(_("Gioi tinh"),choices= Gender.choices, default=Gender.MALE)
    active = models.BooleanField(_("Kich hoat"),default=False)
    createdAt= models.DateTimeField(_("Thoi gian tao"), auto_now_add=True)
    lastAccess = models.DateTimeField(_("Lan cuoi truy cap"), auto_now=True)
    def __str__(self):
        return self.name

class Post(models.Model):
    author = models.ForeignKey(Client, on_delete= models.CASCADE, related_name="posts",verbose_name=_("Tac gia")) 
    #related name dùng để Client gọi ngược lại Post 
    #Client sẽ gọi client.posts.all()
    # trong python bắt buộc các tham số ko tên phải đặt trước tham số có tên
    # phải đúng thứ tự các tham số ForeignKey(ten bảng tham chiếu, on_delete,verbose_name)
    title = models.CharField(_("Tieu de"),max_length=500, blank=False)
    content = models.TextField(_("Noi dung"))
    createdAt= models.DateTimeField(_("Ngay dang"), auto_now_add=True)
    updateAt= models.DateTimeField(_("Ngay cap nhat"), auto_now_add=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.author:
            self.author.save()
    def __str__(self):
        return self.title