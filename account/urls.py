from django.urls import path, include 
from account import views 
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import SimpleRouter
from category.views import CategoryViewSet
from product.views import ProductViewSet

router = SimpleRouter()

router.register('products', ProductViewSet,)
router.register('category', CategoryViewSet,)


urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.RegistrationView.as_view()),
    path('activate/<uuid:activation_code>/', views.ActivationView.as_view()),
    path('login/', views.LoginApiView.as_view()),
    path('logout/', views.LogoutApiView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('', include(router.urls)),
    path('forgot/', views.ForgotPasswordView.as_view()),
    path('restore/', views.RestorePasswordView.as_view()),
    path('spam-follow/', views.FollowSpamApi.as_view()),
]
