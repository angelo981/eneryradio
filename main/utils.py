import re
from urllib.parse import urlparse, parse_qs

def get_youtube_embed_url(url):
    """
    Convert various YouTube URL formats to the embed URL format.
    Supports:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    - https://www.youtube.com/embed/VIDEO_ID
    """
    if not url:
        return None
    
    # If it's already an embed URL, return as is
    if 'youtube.com/embed/' in url:
        return url
    
    # Pattern for standard YouTube URL
    youtube_regex = r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})'
    match = re.search(youtube_regex, url)
    if match:
        video_id = match.group(1)
        return f'https://www.youtube.com/embed/{video_id}'
    
    # Pattern for shortened YouTube URL
    youtu_be_regex = r'(?:https?://)?(?:www\.)?youtu\.be/([a-zA-Z0-9_-]{11})'
    match = re.search(youtu_be_regex, url)
    if match:
        video_id = match.group(1)
        return f'https://www.youtube.com/embed/{video_id}'
    
    # If no match found, return original URL
    return url
