from django.contrib import admin
from django.urls import path
from HeartSync.views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('insert_cities/',insert_cities,name='insert_cities'),
    path('insert-interests/',insert_interests, name='insert_interests'),
    path('insert-profiles/',insert_profiles, name='insert_profiles'),
    path('insert-likes/',insert_likes, name='insert_likes'),
    path('insert-matches/',insert_matches, name='insert_matches'),
    path('insert-messages/',insert_messages, name='insert_messages'),
    path('insert-blocks/',insert_blocks, name='insert_blocks'),
    path('show_user/',show_user,name='show_user'),
    path('create_user/',create_user,name='create_user'),
    path('home/',home,name='home'),
    path('user_login/',user_login,name='login'),
    path('user_logout/',user_logout,name='user_logout'),
    path('like/<int:profile_id>/', like, name='like'),
    path('pass_user/<int:profile_id>/',pass_user,name='pass_user'),
    path('matches/',matches,name='matches'),
    path('discover/',discover,name='discover'),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
