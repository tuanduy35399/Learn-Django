from rest_framework.routers import DefaultRouter
from .views import TodoViewSet

router= DefaultRouter() 
# Cấu trúc: router.register(r'prefix', ViewSet)
#r'todos': Đây là tiền tố cho URL. Khi đó, API của bạn sẽ có dạng api/todos/.
#TodoViewSet: Class ViewSet mà bạn đã định nghĩa.
#basename='todo' (tùy chọn): Tên dùng cho việc tạo URL ngược (reverse URL)

router.register(r'todo',TodoViewSet)
urlpatterns= router.urls