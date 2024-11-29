from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/',views.user_logout, name='logout'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('search/', views.book_search, name='book_search'),
    path('book/<int:pk>/borrow/', views.borrow_book, name='borrow_book'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('return/<int:borrow_id>/', views.return_book, name='return_book'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
