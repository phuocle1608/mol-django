from django.urls import path, include
from . import views


app_name = 'QLBH'

urlpatterns = [
    path('', views.Homepage.as_view(), name ='index'),
    path('donhang/', views.DonhangTonghop.as_view(), name = 'dsdonhang'),
    path('donhang/<int:donhang_id>/', views.DonhangDetail.as_view(), name = 'donhang_detail'),
    # path('test/', views.Test.as_view(), name='test'),
    path('nhap_don_hang/', views.NhapDonHang.as_view(), name='nhap_don_hang'),
    path('nhap_khach_hang/', views.NhapKhachHang.as_view(), name='nhap_khach_hang'),
    path('donhang/update/<int:donhang_id>', views.Updatedonhang.as_view(), name='sua_don_hang'),
    path('login/', views.Login.as_view(), name='login'),
    path('ajax_update_db/', views.AjaxUpdateDatabase.as_view(), name='ajax_update_db')
]
