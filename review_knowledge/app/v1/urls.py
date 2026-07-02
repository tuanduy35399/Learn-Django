from app.v1.client.client_views import client_detail, client_list
from django.urls import path
from app.v1.post.post_views import post_detail, post_list

urlpatterns = [
    path('client/', client_list),
    # neu django thuan ko API thi can co name='client_list' de sau nay ben file HTML tham chieu qua
    # hoac de redirect (chuyen huong trang)
    #def create_client(request):
    # tạo client
    #return redirect('client_list')
    path('client/<int:primary_key>/', client_detail, name='client_detail'),
    path('post/', post_list),
    path('post/<int:pk>/',post_detail),
]
