import os
import json
import time
import requests
import azure.cognitiveservices.speech as speechsdk
from django.http import JsonResponse
from django.conf import settings
from django.core.files.storage import default_storage
from chat.models import TempChatFile
print(os.getenv("SPEECH_KEY"))
WaveHeader16K16BitMono = bytes([82, 73, 70, 70, 78, 128, 0, 0, 87, 65, 86, 69, 102, 109, 116, 32, 18,
                               0, 0, 0, 1, 0, 1, 0, 128, 62, 0, 0, 0, 125, 0, 0, 2, 0, 16, 0, 0, 0, 100, 97, 116, 97, 0, 0, 0, 0])


def get_chunk(audio_source, chunk_size=1):
    # audio_source2 = default_storage.open(audio_source1, 'rb')
    yield WaveHeader16K16BitMono
    # return audio_source.read()
    while True:
        time.sleep(chunk_size / 32000)  # to simulate human speaking rate
        chunk = audio_source.read(chunk_size)
        # print(audio_source.size)
        if not chunk:
            print('chunk not found')
            break
        yield chunk


def get_token():
    headers = {
        'Ocp-Apim-Subscription-Key': os.getenv("SPEECH_KEY")
    }
    response = requests.get(
        "https://eastus.api.cognitive.microsoft.com/sts/v1.0/issueToken", headers=headers)
    access_token = str(response.text)
    return access_token


def get_text(file):
    headers = {
        'Ocp-Apim-Subscription-Key': os.getenv("SPEECH_KEY"),
        # 'Transfer-Encoding': 'chunked',
        'Content-Type': 'audio/wav',
        'Expect': '100-continue',
        'Accept': 'application/json;text/xml',
        'Connection': 'Keep-Alive',
    }
    response = requests.post(
        "https://eastus.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1?language=en-US", headers=headers,
        data=get_chunk(file))
    if response.ok:
        # print(response.json())
        # return response.json()
        print(response.content)
        print(json.loads(response.text))
        return json.loads(response.text).get("DisplayText", "")
        # return "Hahahh"
    else:
        print('failed')
        print(response.status_code)


def speech_recognition(request):
    speech_config = speechsdk.SpeechConfig(subscription=os.getenv(
        "SPEECH_KEY"), region=os.getenv("SPEECH_REGION"))
    speech_config.speech_recognition_language = "en-US"
    new_temp_file = TempChatFile.objects.create(file=request.FILES.get('file'))
    file = default_storage.open(os.path.join(
        settings.MEDIA_ROOT, new_temp_file.file.url.replace('/media/', '')), 'rb')
    data = get_text(file)
    file.close()
    # print('data', request.POST, request.FILES)
    # print(request.POST.get('audio_file'))
    # print(request.FILES)
    # return JsonResponse(data={}, status=200)
    # file_loc = new_temp_file.file.url.split('/')[-1]
    # print(file_loc)
    # audio_config = speechsdk.audio.AudioConfig(filename=file_loc)
    # speech_recognizer = speechsdk.SpeechRecognizer(
    #     speech_config=speech_config, audio_config=audio_config)
    # speech_recognition_result = speech_recognizer.recognize_once_async().get()

    # if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
    #     print("Recognized: {}".format(speech_recognition_result.text))
    # elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
    #     print("No speech could be recognized: {}".format(
    #         speech_recognition_result.no_match_details))
    # elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
    #     cancellation_details = speech_recognition_result.cancellation_details
    #     print("Speech Recognition canceled: {}".format(
    #         cancellation_details.reason))
    #     if cancellation_details.reason == speechsdk.CancellationReason.Error:
    #         print("Error details: {}".format(
    #             cancellation_details.error_details))
    #         print("Did you set the speech resource key and region values?")
    return JsonResponse(data={'message': data}, status=200)
