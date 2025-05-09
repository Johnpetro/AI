from openai import OpenAI

client = OpenAI()
audio_file = open("voice.ogg", "rb")

transcription = client.audio.transcriptions.create(
    model="gpt-4o-transcribe", 
    file=audio_file, 
    response_format="text"
)

print(transcription.text)