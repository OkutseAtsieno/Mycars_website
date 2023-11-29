from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_view
from .forms import LoginForm, MyPasswordResetForm, MyPasswordChangeForm, MySetPasswordForm
from django.conf import settings
from django.conf.urls.static import static
from .views import UpdateAddress, CategoryTitleView, Checkout,CategoryView,ProductDetail

urlpatterns = [
    path("", views.home, name="home"),
    path("base/", views.base, name="base"),
    path("contact/", views.contact, name="contact"),
    path('Product-detail/<int:pk>/', views.ProductDetail.as_view(), name='product_detail'),
    path("category-title/<value>", CategoryTitleView.as_view(), name="category-title"),
    path("about/", views.about, name="about"),
    path("category/<slug:value>", views.CategoryView.as_view(), name="category"),
    path("update-address/<int:pk>/", UpdateAddress.as_view(), name="updateAddress"),
    path('category/<str:subcategory>/',CategoryView.as_view(),name='category'),
    path('product/<int:pk>/',ProductDetail.as_view(),name='product-detail'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('checkout/', Checkout.as_view(), name='checkout'),
    path('pluscart/', views.plus_cart, name='pluscart'),
    path('minuscart/', views.minus_cart, name='minuscart'),
    path('removecart/', views.remove_cart, name='removecart'),
    path('Orders/', views.orders, name='orders'),
    path('pluswishlist/', views.plus_wishlist, name='pluswishlist'),
    path('minuswishlist/', views.minus_wishlist, name='minuswishlist'),

    # login authentication
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
    path('accounts/login/', auth_view.LoginView.as_view(template_name='login.html', authentication_form=LoginForm), name='login'),

    path('password-reset/', auth_view.PasswordResetView.as_view(
        template_name='password_reset.html', form_class=MyPasswordResetForm),
        name='password_reset'),
    path('password-reset/done/', auth_view.PasswordResetDoneView.as_view(template_name='password-reset-done.html'), name='password_reset_done'),    
    path('password-change/', auth_view.PasswordChangeView.as_view(template_name='Changepassword.html', form_class=MyPasswordChangeForm, success_url='/password-changedone'), name='password_change'),
    path('password-changedone/', auth_view.PasswordChangeDoneView.as_view(template_name='passwordChangedone.html'), name='password-changedone'),
    path('logout/', auth_view.LogoutView.as_view(next_page='login'), name='user-logout'),   # redirect to the login page
    path('password-reset-confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name='password-reset-confirm.html', form_class=MySetPasswordForm), name='password_reset_confirm'),
    path('password-reset-complete/', auth_view.PasswordResetCompleteView.as_view(template_name='password-reset-complete.html'), name='password_reset_complete'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)