
import os
import shutil
from django.conf import settings
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Video

@receiver(post_delete, sender=Video)
def delete_video_files(sender, instance, **kwargs):
    # Delete original uploaded video file
    if instance.video_file and os.path.isfile(instance.video_file.path):
        try:
            os.remove(instance.video_file.path)
            print(f"Deleted video file: {instance.video_file.path}")
        except Exception as e:
            print(f"Error deleting video file: {e}")

    # Delete HLS folder (all chunks and playlist)
    hls_folder = os.path.join(settings.MEDIA_ROOT, os.path.dirname(instance.hls_path))
    if os.path.isdir(hls_folder):
        try:
            shutil.rmtree(hls_folder)
            print(f"Deleted HLS folder: {hls_folder}")
        except Exception as e:
            print(f"Error deleting HLS folder: {e}")
