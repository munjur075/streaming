from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='videos/')
    hls_path = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.title