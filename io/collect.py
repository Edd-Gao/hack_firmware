#!usr/bin/env python  
#coding=utf-8  
  
import numpy as np  
from pyaudio import PyAudio,paInt16  
from datetime import datetime  
import wave  
import requests
import json
import os
  
#define of params  
NUM_SAMPLES = 2000
framerate = 8000  
channels = 1
sampwidth = 2  
#record time  
TIME = 10  
  
def save_wave_file(filename, data):  
    '''''save the date to the wav file'''  
    wf = wave.open(filename, 'wb')  
    wf.setnchannels(channels)  
    wf.setsampwidth(sampwidth)  
    wf.setframerate(framerate)  
    wf.writeframes("".join(data))  
    wf.close()  

  
def record_wave():  
    #open the input of wave  
    pa = PyAudio()  
    stream = pa.open(format = paInt16, channels = 1,  
                    rate = framerate, input = True,  
                    frames_per_buffer = NUM_SAMPLES)  
    save_buffer = []  
    # 记录是否录音结束
    isEnd = True 
    # 记录是否count
    # isCount = False

    while True:  
        #read NUM_SAMPLES sampling data  
        string_audio_data = stream.read(NUM_SAMPLES)

        wave_data = np.fromstring(string_audio_data, dtype=np.short)
        wave_data.shape = -1, 2
        wave_data = wave_data.T
        print len(wave_data[0])
        print np.mean(np.abs(wave_data[0]))

        if np.mean(np.abs(wave_data[0])) > 1800:
            save_buffer.append(string_audio_data) 
            print len(save_buffer)
            isEnd = False
        else:
            isEnd = True


        if len(save_buffer) != 0 and isEnd == True:
            filename = datetime.now().strftime("%Y-%m-%d_%H_%M_%S")+".wav"  
            save_wave_file(filename, save_buffer)

            files = {'voice': open(filename, 'rb')}
            resp = requests.post("http://127.0.0.1:5000/upload_voice", files=files)
            print resp.content
            json_resp = json.loads(resp.content)
            if json_resp['code'] == 0:
                r = requests.get("http://127.0.0.1:5000/voice/"+json_resp['save_file_name'], stream=True)
                with open("temp.wav", "wb") as f:
                    f.write(r.raw.read())
                os.popen2('play ' + 'temp.wav')
                #resp_f = wave.open(r"./temp.wav", "r")
                #say(resp_f)
            

            save_buffer = []  
            print filename, "saved"  

        print '.'  

      
if __name__ == "__main__":
    record_wave()

