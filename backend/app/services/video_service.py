import requests
from backend.app.core.config import settings


class VideoService:
    @staticmethod
    def get_curated_video(topic: str, subject: str):
        # API Key should be in your .env or settings
        api_key = settings.YOUTUBE_API_KEY
        query = f"{subject} {topic} educational tutorial"

        url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            "part": "snippet",
            "q": query,
            "type": "video",
            "maxResults": 1,  # Get the top curated result
            "relevanceLanguage": "en",
            "key": api_key
        }

        try:
            response = requests.get(url, params=params).json()
            if "items" in response and len(response["items"]) > 0:
                video_id = response["items"][0]["id"]["videoId"]
                return {
                    "url": f"https://www.youtube.com/embed/{video_id}",
                    "title": response["items"][0]["snippet"]["title"]
                }
        except Exception as e:
            print(f"YouTube API Error: {e}")
        return None