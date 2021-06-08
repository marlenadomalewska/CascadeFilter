import pyaudio
import numpy as np
import time
import json

import scipy.signal as signal

p = pyaudio.PyAudio()

CHANNELS = 1
RATE = 44100

with open('hk1.json') as f:
     h1 = json.load(f)
     print(h1)
with open('hk2.json') as f:
     h2 = json.load(f)
     print(h2)
with open('hk3.json') as f:
     h3 = json.load(f)
     print(h3)

h1mian = h1.pop()
h1licz = h1.pop()
h2mian = h2.pop()
h2licz = h2.pop()
h3mian = h3.pop()
h3licz = h3.pop()

h1m3 = h1mian.pop()
h1m2 = h1mian.pop()
h1m1 = h1mian.pop()
h1li3 = h1licz.pop()
h1li2 = h1licz.pop()
h1li1 = h1licz.pop()

h2m3 = h2mian.pop()
h2m2 = h2mian.pop()
h2m1 = h2mian.pop()
h2li3 = h2licz.pop()
h2li2 = h2licz.pop()
h2li1 = h2licz.pop()

h3m3 = h3mian.pop()
h3m2 = h3mian.pop()
h3m1 = h3mian.pop()
h3li3 = h3licz.pop()
h3li2 = h3licz.pop()
h3li1 = h3licz.pop()

##h1licz = np.array([h1li1, h1li2, h1li3])
##h1mian = np.array([h1m1, h1m2, h1m3])
##
##h2licz = np.array([h2li1, h2li2, h2li3])
##h2mian = np.array([h2m1, h2m2, h2m3])
##
##h3licz = np.array([h3li1, h3li2, h3li3])
##h3mian = np.array([h3m1, h3m2, h3m3])

h1licz = np.array([h1li3, h1li2, h1li1])
h1mian = np.array([h1m3, h1m2, h1m1])

h2licz = np.array([h2li3, h2li2, h2li1])
h2mian = np.array([h2m3, h2m2, h2m1])

h3licz = np.array([h3li3, h3li2, h3li1])
h3mian = np.array([h3m3, h3m2, h3m1])

     
def callback(in_data, frame_count, time_info, flag):
    # using Numpy to convert to array for processing
    # audio_data = np.fromstring(in_data, dtype=np.float32)
    # return in_data, pyaudio.paContinue
        #print(in_data)
    in_data_after_conversion = np.frombuffer(in_data, dtype='<f4')
    #print("AFTER CONVERISON")
#    print("indata")
#    print(in_data_after_conversion)

    filtr_h1 = signal.lfilter(h1licz, h1mian, in_data_after_conversion, axis=0)
    filtr_h2 = signal.lfilter(h2licz, h2mian, filtr_h1, axis=0)
    data_filtered = signal.lfilter(h3licz, h3mian, filtr_h2, axis=0)

#   print("filtered")
#   print(data_filtered)
    return np.float32(data_filtered).tobytes(), pyaudio.paContinue



#############
stream = p.open(format=pyaudio.paFloat32,
                channels=CHANNELS,
                rate=RATE,
                output=True,
                input=True,
                stream_callback=callback)

stream.start_stream()

while stream.is_active():
    time.sleep(20)
    stream.stop_stream()
    print("Stream is stopped")

stream.close()

p.terminate()
