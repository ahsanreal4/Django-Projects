from django.urls import path
from . import views

urlpatterns = [
    path('menu-items', views.MenuItemListView.as_view(), name='menu-items'),
    path('menu-items/<int:pk>', views.MenuItemSingleView.as_view(), name='menu-item'),
    path('groups/manager/users', views.ManagerGroupListView.as_view(), name='manager-groups'),
    path('groups/manager/users/<int:pk>', views.ManagerGroupSingleView.as_view(), name='manager-group'),
    path('groups/delivery-crew/users', views.DeliveryCrewGroupListView.as_view(), name='delivery-crews'),
    path('groups/delivery-crew/users/<int:pk>', views.DeliveryCrewGroupSingleView.as_view(), name='delivery-crew'),
    path('cart/menu-items', views.CartListView.as_view(), name='carts'),
    path('orders', views.OrderListView.as_view(), name='orders'),
    path('orders/<int:pk>', views.OrderSingleView.as_view(), name='order'),
]
