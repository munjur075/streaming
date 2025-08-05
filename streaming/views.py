import os
import subprocess
from django.shortcuts import render, redirect, get_object_or_404
from .models import Video
from .forms import VideoForm
from django.conf import settings
from django.http import JsonResponse


def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save()
            input_path = video.video_file.path
            output_dir = os.path.join(settings.MEDIA_ROOT, f'hls/{video.id}')
            os.makedirs(output_dir, exist_ok=True)

            output_path = os.path.join(output_dir, 'index.m3u8')
            cmd = [
                r'C:\Users\munju\Desktop\ffmpeg\bin\ffmpeg.exe',  # full exe path here
                '-i', input_path,
                '-codec:', 'copy',
                '-start_number', '0',
                '-hls_time', '10',
                '-hls_list_size', '0',
                '-f', 'hls', output_path
            ]
            try:
                subprocess.run(cmd, check=True)
            except FileNotFoundError:
                return render(request, 'streaming/upload.html', {
                    'form': form,
                    'error': 'FFmpeg not found. Please install it and set PATH or use full path to ffmpeg.exe.'
                })
            except subprocess.CalledProcessError as e:
                return render(request, 'streaming/upload.html', {
                    'form': form,
                    'error': f'FFmpeg error: {e}'
                })

            video.hls_path = f'hls/{video.id}/index.m3u8'
            video.save()
            # return redirect('stream_video', video_id=video.id)
            return JsonResponse({'message': 'Video uploaded and converted!', 'video_id': video.id})
    else:
        form = VideoForm()
    return render(request, 'streaming/upload.html', {'form': form})



def stream_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    return render(request, 'streaming/stream.html', {'video': video})
