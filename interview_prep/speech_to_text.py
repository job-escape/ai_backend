
from django.core.files.uploadedfile import InMemoryUploadedFile
from google.cloud import speech


def generate_transcription(file: InMemoryUploadedFile):
    """Generates transcription of an audio file using Google Cloud."""
    with file.open("rb") as f:
        audio = speech.RecognitionAudio(content=f.read())

    config = speech.RecognitionConfig(
        # encoding,
        # sample_rate_hertz
        language_code="en-US",
        enable_automatic_punctuation=True,
        model="latest_short"
    )

    client = speech.SpeechClient()
    response = client.recognize(config=config, audio=audio)
    return response.results.pop(0).alternatives.pop(0).transcript
