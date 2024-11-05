# call_vonage.py
import requests
import json
import os
from dotenv import load_dotenv
import jwt  # pyjwt 라이브러리를 사용합니다.
import datetime

# 환경 변수 로드
load_dotenv()

# Vonage API 설정
VONAGE_APPLICATION_ID = os.getenv("VONAGE_APPLICATION_ID")
VONAGE_APPLICATION_PRIVATE_KEY_PATH = os.getenv("VONAGE_APPLICATION_PRIVATE_KEY_PATH")
TO_NUMBER = os.getenv("TO_NUMBER")
VONAGE_NUMBER = os.getenv("VONAGE_NUMBER")

# JWT 토큰 생성 함수
def get_vonage_token():
    private_key = open(VONAGE_APPLICATION_PRIVATE_KEY_PATH, 'r').read()
    payload = {
        "application_id": VONAGE_APPLICATION_ID,
        "iat": datetime.datetime.now(datetime.timezone.utc),  # UTC 시간으로 설정
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=10),
        "jti": "UNIQUE_JTI_ID"
    }
    token = jwt.encode(payload, private_key, algorithm="RS256")
    return token

# Vonage로 전화 걸기
def make_call():
    ncco = [
        {
            "action": "talk",
            "text": "안녕하세요, 상담을 시작합니다.",
            "language": "ko-KR"
        },
        {
            "action": "connect",
            "endpoint": [
                {
                    "type": "websocket",
                    "uri": "wss://e936-222-112-27-104.ngrok-free.app/ws",  # WebSocket URI 설정
                    "contentType": "audio/l16;rate=16000"
                }
            ]
        }
    ]

    url = "https://api.nexmo.com/v1/calls"
    headers = {
        "Authorization": f"Bearer {get_vonage_token()}",
        "Content-Type": "application/json"
    }
    data = {
        "to": [{"type": "phone", "number": TO_NUMBER}],
        "from": {"type": "phone", "number": VONAGE_NUMBER},
        "ncco": ncco
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 201:
        print("Call initiated:", response.json())
    else:
        print("Error initiating call:", response.status_code, response.text)

# 전화를 걸기
make_call()
