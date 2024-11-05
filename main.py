from fastapi import FastAPI, WebSocket
from google.cloud import speech
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# Google Cloud 인증 파일 경로 설정
credential_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credential_path

app = FastAPI()
client = speech.SpeechClient()  # Google Cloud Speech-to-Text 클라이언트 설정

# 음성 데이터를 텍스트로 변환하는 함수
def transcribe_audio(audio_data):
    audio = speech.RecognitionAudio(content=audio_data)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,  # LINEAR16로 설정
        sample_rate_hertz=16000,
        language_code="ko-KR",
        enable_automatic_punctuation=True  # 자동 구두점 추가
    )
    response = client.recognize(config=config, audio=audio)
    for result in response.results:
        return result.alternatives[0].transcript
    return "음성을 인식할 수 없습니다."

# WebSocket 엔드포인트 설정
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("WebSocket 연결이 수립되었습니다.")

    audio_buffer = b""  # 수신한 오디오 데이터를 모아둘 버퍼

    try:
        while True:
            # Vonage로부터 음성 데이터 수신
            audio_data = await websocket.receive()

            if isinstance(audio_data, dict):
                if 'bytes' in audio_data:
                    audio_bytes = audio_data['bytes']
                    audio_buffer += audio_bytes  # 버퍼에 데이터 추가

                    # 버퍼가 충분히 쌓이면 텍스트로 변환
                    if len(audio_buffer) >= 10000:  # 최소 10KB 이상일 때 변환 시도
                        print("버퍼 크기:", len(audio_buffer))
                        # 파일로 저장하여 확인
                        with open("received_audio.wav", "wb") as f:
                            f.write(audio_buffer)

                        text = transcribe_audio(audio_buffer)
                        print("변환된 텍스트:", text)
                        await websocket.send_text(text)
                        audio_buffer = b""  # 버퍼 초기화

                elif 'type' in audio_data and audio_data['type'] == 'websocket.disconnect':
                    print("연결 종료 요청 수신:", audio_data)
                    break  # WebSocket 연결 종료
            else:
                print("오류: 예상치 않은 데이터 형식 수신:", type(audio_data))
                break  # 예상치 못한 데이터 형식이므로 종료

    except Exception as e:
        print("오류 발생:", e)
    finally:
        try:
            await websocket.close()
        except RuntimeError:
            pass
        print("WebSocket 연결이 종료되었습니다.")
