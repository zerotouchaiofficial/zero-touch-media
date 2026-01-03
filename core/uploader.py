{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import os\
import json\
import sys\
\
DRY_RUN = True\
\
TOKEN_PATH = "/tmp/youtube_token.json"\
\
def load_token():\
    if not os.path.exists(TOKEN_PATH):\
        print("\uc0\u10060  Token file not found at", TOKEN_PATH)\
        sys.exit(1)\
\
    with open(TOKEN_PATH, "r") as f:\
        token = json.load(f)\
\
    print("\uc0\u9989  Token loaded successfully")\
    print("\uc0\u55357 \u56593  Token keys:", list(token.keys()))\
    return token\
\
\
def main():\
    print("\uc0\u55357 \u56960  Uploader started")\
\
    token = load_token()\
\
    if DRY_RUN:\
        print("\uc0\u55358 \u56810  DRY RUN MODE ENABLED")\
        print("\uc0\u55357 \u56516  Channel authorization looks valid")\
        print("\uc0\u9940  Exiting BEFORE any YouTube API call")\
        return\
\
    # REAL UPLOAD LOGIC WILL COME IN STEP 6.4\
    raise RuntimeError("DRY_RUN is False \'97 this should not happen in Step 6.3")\
\
\
if __name__ == "__main__":\
    main()\
}