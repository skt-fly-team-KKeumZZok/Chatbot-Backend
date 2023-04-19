import os
import sys
import urllib.request

def texttospeech(text):
    client_id = "ahce7hh5it"
    client_secret = "Y4oL5wkWpTbaIDVVrgjCxHSFwT8XVPeeihINQEBo"
    data = "speaker=nhajun&volume=0&speed=0&pitch=0&format=mp3&text=" + text;
    url = "https://naveropenapi.apigw.ntruss.com/tts-premium/v1/tts"
    request = urllib.request.Request(url)
    request.add_header("X-NCP-APIGW-API-KEY-ID", client_id)
    request.add_header("X-NCP-APIGW-API-KEY", client_secret)
    response = urllib.request.urlopen(request, data=data.encode('utf-8'))
    rescode = response.getcode()
    if(rescode==200):
        print("TTS Send to front")
        response_body = response.read()
        return response_body
    else:
        print("Error Code: " + rescode)
        return None


