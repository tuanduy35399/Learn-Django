from app.v1.client.views import client_list
from django.urls import path

urlpatterns = [
    path('client/', client_list) 
    # neu django thuan ko API thi can co name='client_list' de sau nay ben file HTML tham chieu qua
    # hoac de redirect (chuyen huong trang)
    #def create_client(request):
    # tạo client
    #return redirect('client_list')
]
