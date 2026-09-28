import librosa as lb
import numpy as np
import matplotlib.pyplot as ply
import soundfile as sf
import noisereduce as nr
original_path = ""
background_noise_path = ""
snare_path = ""
hihat_path = ""
kick_path = ""
final_path = ""
original,sr = lb.load(original_path,sr = 48000,offset=0.2)
hiss ,hsr = lb.load(background_noise_path,sr = 48000)
file = nr.reduce_noise(y = original,sr= 48000,y_noise=hiss,stationary=True,prop_decrease=0.85)
#file = original
# file = file[:]*2
# print(file)
# sf.write(r"C:\Users\icefo\OneDrive\Desktop\recording12s.wav",file,48000,)

# print(np.shape(file))
# print(np.max(file))
# print(np.mean(file))
# print(np.sort(file)[-1:-100:-1])
# tap_frames = lb.onset.onset_detect(y=file,sr=sr,backtrack=False,delta = 0.1)
# print("TAP + ",tap_frames)
# taptime = lb.frames_to_time(tap_frames,sr=sr)
# tapsample = lb.frames_to_samples(tap_frames)
# ply.figure(figsize=(10,4))
# lb.display.waveshow(file,sr=sr)
# ply.vlines(taptime,ymin=file.min(),ymax=file.max(),color='r',linestyle= '--')
# ply.title("Waveform")
# ply.xlabel("TIME")
# ply.ylabel("AMPLITUDE")
# ply.show()
# snaref,ssr = lb.load(r"C:\Users\icefo\OneDrive\Desktop\snare.wav",sr=48000)
# print("SNARE SHAPE = ",np.shape(snaref)) #57193
# fcopy = file.copy()
# for tap in tapsample:
#     tap_area = file[tap: tap +720]
#     tap_velocity = np.max(np.abs(tap_area)) * 3.2


#     if tap+57193 < len(file):
#         fcopy[tap:tap+57193] = snaref*tap_velocity
#     else:
#         fcopy[tap:] = (snaref*tap_velocity)[:len(file)-tap]    
# sf.write(r"C:\Users\icefo\OneDrive\Desktop\final.wav",fcopy,48000)

##Frequency
# stft_mat = lb.stft(file)
# stft_db = lb.amplitude_to_db(np.abs(stft_mat),ref=np.max(stft_mat))
# ply.figure(figsize=(10,5))
# lb.display.specshow(stft_db,sr=48000,x_axis='time',y_axis='linear',cmap = 'magma')
# ply.title("FREQ Spectogram")
# ply.xlabel("TIME")
# ply.ylabel("Frequency")
# ply.show()























print(np.shape(file))
print(np.max(file))
print(np.mean(file))
print(np.sort(file)[-1:-100:-1])
tap_frames = lb.onset.onset_detect(y=file,sr=sr,backtrack=False,delta = 0.1)
print("TAP frames = ",tap_frames)
taptime = lb.frames_to_time(tap_frames,sr=sr)
tapsample = lb.frames_to_samples(tap_frames)
ply.figure(figsize=(10,4))
lb.display.waveshow(file,sr=sr)
ply.vlines(taptime,ymin=file.min(),ymax=file.max(),color='r',linestyle= '--')
ply.title("Waveform")
ply.xlabel("TIME")
ply.ylabel("AMPLITUDE")
ply.show()
snaref,ssr = lb.load(snare_path,sr=48000)
kickf,ksr = lb.load(kick_path,sr=48000)
hatf,hsr = lb.load(hihat_path,sr=48000)
print("SNARE SHAPE = ",np.shape(snaref)) #57193
print("kick SHAPE = ",np.shape(kickf)) #58849
print("hat SHAPE = ",np.shape(hatf))#42468
fcopy = file.copy()


stft = np.abs(lb.stft(file))
print(np.shape(stft))


frequencies = lb.fft_frequencies(sr=48000)
bassf = (frequencies >= 20) & (frequencies < 350)
midf = (frequencies >= 350) & (frequencies < 6000)
trebf = (frequencies >= 6000) & (frequencies < 20000)
bas5 = 0
mid5 = 0
treb5 = 0
bass_energy = 0
mid_energy = 0
treble_energy = 0


bcounter = 0
mcounter = 0
tcounter = 0
for tap in tapsample:
    tap_area = file[tap: tap +720]
    frame_idx = lb.samples_to_frames(np.arange(tap,tap + 720))
    # if frame_idx >= stft.shape[1]:
    #     frame_idx = stft.shape[1] - 1
    for frame in frame_idx:
        frame_energy = stft[:,frame]    
        basst = np.sum(frame_energy[bassf])
        midt = np.sum(frame_energy[midf])
        trebt = np.sum(frame_energy[trebf])
        total_energy = basst + midt + trebt
        bass_energy =   bass_energy + (basst/total_energy)*100
        mid_energy =    mid_energy + (midt/total_energy)*100
        treble_energy = treble_energy + (trebt/total_energy)*100
    tap_velocity = np.max(np.abs(tap_area)) * 3.2
    

    if bass_energy > mid_energy and bass_energy > treble_energy:
        bcounter+=1
        if tap+58849 < len(file):
            fcopy[tap:tap+58849] = kickf*tap_velocity
        else:
            fcopy[tap:] = (kickf*tap_velocity)[:len(file)-tap]
    elif mid_energy >bass_energy and mid_energy > treble_energy:
            mcounter+=1
            if tap+42468 < len(file):
                fcopy[tap:tap+42468] = hatf*tap_velocity
            else:
                fcopy[tap:] = (hatf*tap_velocity)[:len(file)-tap]    
    else:
        tcounter+=1
        if tap+57193 < len(file):
            fcopy[tap:tap+57193] = snaref*tap_velocity
        else:
            fcopy[tap:] = (snaref*tap_velocity)[:len(file)-tap]    
    bass_energy,mid_energy,treble_energy = 0,0,0        
sf.write(final_path,fcopy,48000)
print(bcounter,mcounter,tcounter)