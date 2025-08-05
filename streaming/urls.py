from django.urls import path
from .views import upload_video, stream_video

urlpatterns = [
    path('', upload_video, name='upload_video'),
    path('stream/<int:video_id>/', stream_video, name='stream_video'),
]