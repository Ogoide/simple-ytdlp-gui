from yt_dlp import YoutubeDL

# Check if the provided url is valid and active
def check_url_video(url):
    """
    Tries extracting the information about the video, without downloading
    Should the process fail, it's an indication the video doesn't exist
    """
    ydl = YoutubeDL({'quiet': True, 'no_warnings': True})

    try:
        info = ydl.extract_info(url, download=False)
        return True
    except Exception:
        return False

def get_video_info(url):
    ydl = YoutubeDL({'quiet': True, 'no_warnings': True})
    info = ydl.extract_info(url, download=False)
    return info

def check_formats(url):
    ydl = YoutubeDL({'quiet': True, 'no_warnings': True, 'check_formats': 'selected'})

def download(url, media_type, format, path):
    if media_type == 'Video':
        if format == 'MP4':
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'outtmpl': f'{path}/%(title)s.%(ext)s',
                'nomtime': True
            }
        elif format == 'WEBM':
            ydl_opts = {
                'format': f'bestvideo[ext={'webm'}]+bestaudio{'webm'}/best{'webm'}/best',
                'outtmpl': f'{path}/%(title)s.%(ext)s',
                'nomtime': True
            }
    elif media_type == 'Audio':
        ydl_opts = {
            'format': f'{format.lower()}/bestaudio/best',
            'postprocessors': [{  # Extract audio using ffmpeg
                'key': 'FFmpegExtractAudio',
                'preferredcodec': f'{format.lower()}',
            }],
            'outtmpl': f'{path}/%(title)s.%(ext)s',
            'nomtime': True
        }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])




