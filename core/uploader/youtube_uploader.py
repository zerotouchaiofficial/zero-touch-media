import base64, pickle
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def upload_video(video_path, title, description):
    token = base64.b64decode(
        __import__("os").environ["YOUTUBE_TOKEN_BASE64"]
    )
    creds = pickle.loads(token)

    youtube = build("youtube", "v3", credentials=creds)

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": description,
                "tags": ["shorts"],
                "categoryId": "22"
            },
            "status": {
                "privacyStatus": "public",
                "selfDeclaredMadeForKids": False
            }
        },
        media_body=MediaFileUpload(
            video_path,
            mimetype="video/mp4",
            resumable=True
        )
    )

    response = request.execute()
    return response["id"]

