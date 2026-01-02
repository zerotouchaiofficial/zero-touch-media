import json
from pathlib import Path

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

ROOT = Path(__file__).resolve().parents[1]
CREDENTIALS_PATH = ROOT / "auth" / "client_secret.json"
TOKEN_PATH = ROOT / "auth" / "youtube_token.json"


def main():
    if not CREDENTIALS_PATH.exists():
        raise FileNotFoundError(
            "client_secret.json not found in auth/"
        )

    flow = InstalledAppFlow.from_client_secrets_file(
        CREDENTIALS_PATH,
        SCOPES,
    )

    creds = flow.run_local_server(port=8080, prompt="consent")

    with open(TOKEN_PATH, "w") as f:
        json.dump(
            {
                "token": creds.token,
                "refresh_token": creds.refresh_token,
                "token_uri": creds.token_uri,
                "client_id": creds.client_id,
                "client_secret": creds.client_secret,
                "scopes": creds.scopes,
            },
            f,
            indent=2,
        )

    # sanity check
    youtube = build("youtube", "v3", credentials=creds)
    youtube.channels().list(
        part="snippet",
        mine=True
    ).execute()

    print("✅ YouTube OAuth token created successfully")


if __name__ == "__main__":
    main()
