from django.urls import path,include
from django.conf.urls import url
from user import views
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
router = DefaultRouter()
router.register('User_Api',views.User_Api) 
router.register('pandas_Api',views.pandas_Api) 
app_name = 'user'
urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/',    views.LoginView.as_view(), name='login'),
    path('logout/',    views.LogoutView.as_view(), name='logout'),
    url('api/', include(router.urls)),
]
urlpatterns += router.urls