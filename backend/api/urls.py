from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'user',views.RegisterView, basename = 'user')
router.register(r'photo',views.PhotoModelViewSet,basename='photo')

urlpatterns = [
    # Example:
    # path('photos/', views.PhotoListView.as_view(), name='photo-list'),
    path('route/', include(router.urls)),
    path('photos/', views.PhotoModelViewSet.as_view({'get': 'list', 'post': 'create'}), name='photo-list'),
    path('photos/<int:pk>/', views.PhotoModelViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='photo-detail'),
]