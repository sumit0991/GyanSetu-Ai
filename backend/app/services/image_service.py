import requests


class ImageService:
    @staticmethod
    def get_exam_diagram(topic):
        """
        Fetches a technical diagram from Wikimedia Commons.
        Includes error handling to return None if no high-quality match is found.
        """
        # Broaden the search: try "diagram" first, then just the topic name
        search_query = f"{topic} diagram"
        url = "https://commons.wikimedia.org/w/api.php"

        # Required for Wikimedia API access
        headers = {
            'User-Agent': 'Mini2StudyBot/1.0 (contact@example.com)'
        }

        # Step 1: Search for the file
        params = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srsearch": f"{search_query} -filetype:ogv",
            "srnamespace": 6,  # File namespace
            "srlimit": 1  # Get the most relevant match
        }

        try:
            response = requests.get(url, params=params, headers=headers, timeout=5).json()
            search_results = response.get("query", {}).get("search", [])

            # NOVELTY/ERROR HANDLING: If no result found, return None immediately.
            # This prevents the backend from generating an empty image box.
            if not search_results:
                print(f"ImageService: No technical diagram found for '{topic}'.")
                return None

            filename = search_results[0]["title"]

            # Step 2: Get the direct URL for the filename found
            info_params = {
                "action": "query",
                "format": "json",
                "prop": "imageinfo",
                "titles": filename,
                "iiprop": "url"
            }

            img_res = requests.get(url, params=info_params, headers=headers, timeout=5).json()
            pages = img_res.get("query", {}).get("pages", {})

            # Extract page ID safely
            page_id = next(iter(pages))
            if page_id == "-1":
                return None

            image_info = pages[page_id].get("imageinfo", [{}])[0]
            img_url = image_info.get("url")

            if not img_url:
                return None

            # SAFETY: Ensure URL is HTTPS to prevent mixed-content blocks in index.html
            img_url = img_url.replace("http://", "https://")

            return {
                "url": img_url,
                "title": filename.replace("File:", "").replace(".svg", "").replace(".png", "").replace(".jpg", "")
            }

        except Exception as e:
            # Silently fail and return None so the text generator can continue without an image
            print(f"Wikimedia Service Error: {e}")
            return None