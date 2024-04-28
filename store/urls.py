from django.urls import path
from.views import *
from user.views import *
from blog.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
        path('',store,name='store'),
        path('category/<slug:slug>/',category_detail,name='category_detail'),
        path('<slug:slug>/product/',product_detail,name='detail'),
        path('<int:id>/delete/',product_delete,name="delete"),
        path('cart/delete/',cart_delete,name='delete_cart'),
        path('update-product/',updateProduct,name='updateProduct'),
        path('cart/',cart,name='cart'),
        path('add_to_cart/<int:product_id>/',add_to_cart,name="add_to_cart"),
        path('checkout/',checkout,name='checkout'),
        path('increase/cart/<int:item_id>/',increase_quantity,name='increase_quantity'),
        path('update-quantity/',update_all_quantities, name='cart_update'),
        path('login/',login,name="login"),
        path('user/register/',user_create,name="user_create"),
        
        path('blog/posts/',post_list, name = 'post_list'),
        path('post/<slug:slug>/',post_detail, name = 'post'),
     
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)