import os
import subprocess
from django.shortcuts import render, redirect, get_object_or_404
from .models import Video
from .forms import VideoForm
from django.conf import settings
from django.http import JsonResponse

# Define multiple video resolutions
QUALITIES = {
    '1080p': '1920x1080',
    '720p': '1280x720',
    '480p': '854x480',
}

def generate_hls_variants(input_path, output_dir, ffmpeg_path):
    os.makedirs(output_dir, exist_ok=True)
    master_playlist_path = os.path.join(output_dir, 'index.m3u8')

    master_playlist_content = "#EXTM3U\n"

    for label, resolution in QUALITIES.items():
        stream_path = os.path.join(output_dir, f'{label}.m3u8')

        cmd = [
            ffmpeg_path,
            '-i', input_path,
            '-vf', f'scale={resolution}',
            '-c:a', 'aac',
            '-ar', '48000',
            '-c:v', 'h264',
            '-profile:v', 'main',
            '-crf', '20',
            '-sc_threshold', '0',
            '-g', '48',
            '-keyint_min', '48',
            '-hls_time', '10',
            '-hls_playlist_type', 'vod',
            '-b:v', '2500k' if label == '1080p' else '1500k' if label == '720p' else '800k',
            '-maxrate', '2500k' if label == '1080p' else '1600k' if label == '720p' else '900k',
            '-bufsize', '4000k',
            '-b:a', '128k',
            '-f', 'hls',
            stream_path
        ]

        subprocess.run(cmd, check=True)

        master_playlist_content += (
            f"#EXT-X-STREAM-INF:BANDWIDTH=2500000,RESOLUTION={resolution}\n{label}.m3u8\n"
        )

    with open(master_playlist_path, 'w') as f:
        f.write(master_playlist_content)

def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save()
            input_path = video.video_file.path
            output_dir = os.path.join(settings.MEDIA_ROOT, f'hls/{video.id}')
            ffmpeg_path = r'C:\Users\munju\Desktop\ffmpeg\bin\ffmpeg.exe'  # Full path to ffmpeg.exe

            try:
                generate_hls_variants(input_path, output_dir, ffmpeg_path)
            except FileNotFoundError:
                return render(request, 'streaming/upload.html', {
                    'form': form,
                    'error': 'FFmpeg not found. Please install it and set PATH or provide full path to ffmpeg.exe.'
                })
            except subprocess.CalledProcessError as e:
                return render(request, 'streaming/upload.html', {
                    'form': form,
                    'error': f'FFmpeg error: {e}'
                })

            video.hls_path = f'hls/{video.id}/index.m3u8'
            video.save()
            return JsonResponse({'message': 'Video uploaded and converted to multi-quality HLS!', 'video_id': video.id})
    else:
        form = VideoForm()
    return render(request, 'streaming/upload.html', {'form': form})

def stream_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    return render(request, 'streaming/stream.html', {'video': video})
