import requests
import replicate
import requests
import os
import string
import random
from dotenv import load_dotenv


load_dotenv()
SERVER_URL = os.getenv("PRIVATE_SERVER_URL")
MODEL_URL = os.getenv("MODEL_URL")


def __generate_session_id():
    characters = string.ascii_letters + string.digits
    session_key = ''.join(random.choice(characters) for _ in range(8))
    print(session_key)
    return session_key


def upload_files(file_paths=[f"inputs/{file}" for file in os.listdir("inputs")]):
    if len(file_paths) == 0:
        quit("No files found.")

    session_id = __generate_session_id()
    url = f"{SERVER_URL}/upload/{session_id}"

    files = [('file', (open(file_path, 'rb')))
             for file_path in file_paths]
    print(files)
    response = requests.post(url, files=files)

    print(response.text)
    print(response.json())
    return session_id


def run_and_download(session_id, voice_name, video_topic, content_type, key_points):
    os.environ["REPLICATE_API_TOKEN"] = os.getenv("REPLICATE")
    output = replicate.run(
        MODEL_URL,
        input={
            "session_id": session_id,
            "voice_name": voice_name,
            "video_topic": video_topic,
            "content_type": content_type,
            "key_points": key_points,
        }
    )
    print(output)
    r = requests.get(output)
    with open(f"outputs/{session_id}.mp4", "wb") as file:
        file.write(r.content)


if __name__ == "__main__":
    while True:
        try:
            with open("inputs/video.mp4") as file:
                pass
            break
        except:
            input("""Place your input video as 'video.mp4' and
audio (for voice cloning; optional if voice is already cloned)
as 'audio.wav' in inputs folder then press 'enter': """)

    voice_name = input(
        "Enter voice_name (default 'josh'; press 'enter' for default): ")
    video_topic = input("Enter video_topic: ")
    content_type = input("Enter content_type: ")
    key_points = input("Enter key_points: ")

    if voice_name == "":
        voice_name = "josh"

    session_id = upload_files()

    run_and_download(session_id, voice_name, video_topic,
                     content_type, key_points)
