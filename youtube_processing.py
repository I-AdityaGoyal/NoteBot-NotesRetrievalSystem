from youtube_transcript_api import YouTubeTranscriptApi
import re

def extract_text_from_youtube(video_url):
    video_id = re.search(r"(?<=v=)[^&#]+", video_url)
    if not video_id:
        return ""
    
    video_id = video_id.group(0)
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text = " ".join([item['text'] for item in transcript])
        return text
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        return ""
