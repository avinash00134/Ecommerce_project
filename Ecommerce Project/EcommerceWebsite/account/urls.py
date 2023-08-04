from django.urls import path,include
from django.conf import settings
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home , name='home'),
    path('customer_register/',views.register_customer,name='customer_register'),
    path('seller_register/',views.register_seller,name='seller_register'),
    path('logout/',views.logoutUser,name='logout'),
    path('login/',views.login_page,name='login'),
    path('cart/',views.cart,name='cart'),
    path('checkout/',views.checkout,name="checkout"),
    path('my_orders/',views.my_orders,name='my_orders'),
    path('my_cart/<int:product_id>',views.add_to_cart,name="add_to_cart"),
    path('my_carts/<int:cart_id>',views.add_quantity,name="add_quantity"),
    path('carts/<int:cart_id>',views.subtract_quantity,name="subtract_quantity"),
    path('delete_product_cart/<int:cart_id>',views.delete_product_cart,name="delete_product_cart"),
    path('order_confirmation/<str:data>',views.order,name="order_confirm"),
    path('Add Product/',views.add_product,name="add_product"),
    path('Edit Product/<int:prod_id>',views.edit_product,name="edit_product"),
    path('View Product/',views.view_product,name="view_product"),
    path('Delete Product/<int:prod_id>',views.delete_product,name="delete_product"),
    path('request_order/',views.request_order,name="request_order"),
    path('view_product_details/<int:prod_id>/',views.view_product_detail,name="view_product_detail"),
    path('add_product_csv/',views.products_csv,name="add_product_csv"),
    path('Edit Order/<int:ord_id>',views.edit_order,name="edit_order"),
    path('Delete Order/<int:ord_id>',views.delete_order,name="delete_order"),
    path('Cancel Order/<int:ord_id>',views.cancel_order,name="cancel_order"),
    path('View Order/<int:ord_id>',views.view_order,name="view_order"),
    path('invoice-download/<int:ord_id>',views.render_pdf_view, name="pdfdownload"),
    path('social-auth/', include('social_django.urls',namespace='social')),
    path('payment',views.payment,name="order_success"),
    path('search/', views.search_view,name="search"),
    path('tags/<int:prod_id>/<slug:tag_slug>/', views.view_product_detail, name='posts_by_tag'),
]   

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)