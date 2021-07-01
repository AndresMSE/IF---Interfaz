#!/usr/bin/env python
# coding: utf-8

# In[1]:


import scipy as sc
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

def eeg_plot(s,ti,tf,xlim1,xlim2):
    plt.figure(figsize=(20,6))
    N = len(s)
    fm = int(1/0.002)
    sig_time =N/fm
    time = np.linspace(0,sig_time,N)
    time_cut = time[int(ti*fm):int(tf*fm)]
    s_cut = s[int(ti*fm):int(tf*fm)] #señal en el tiempo deseado en uV
    plt.plot(time_cut,s_cut,'blue')
    plt.xlabel('Tiempo [s]',fontsize=20)
    plt.ylabel('Amplitud [$\mu V$]',fontsize=20)
    plt.title(f'Señal EEG t = [{ti},{tf}]',fontsize=22)
    plt.ylim(xlim1,xlim2)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    return
def FFT(signal,freqm,xlim):
    N = len(signal)
    T = 1.0/freqm
    signal_fft = sc.fft.fft(signal)
    frequen = sc.fft.fftfreq(N, T)[:N//2]
    plt.figure(figsize=(20,6))
    plt.plot(frequen, 2.0/N * np.abs(signal_fft[:N//2]),c='red')
    plt.xlabel('$Frecuencia [Hz]$')
    plt.ylabel('Potencia')
    plt.xlim([0.1,xlim])
    #plt.ylim([0,1])
    plt.grid()
    plt.title('Transformada de Fourier')
    plt.show()
    return
def morlet(fecx,wide,freqm):
    frecm=freqm
    twav = np.linspace(-2,2,frecm*4)
    #Sine wave
    com_sin = np.exp(1j*2*np.pi*fecx*twav)
    #Gauss wave
    sigma = wide/(2*np.pi*fecx)
    gauss_c = np.exp(-twav**2/(2*sigma**2))
    #Normalization
    A_sigma = 1/(np.sqrt(sigma*np.sqrt(np.pi)))
    #Morlet wavelet
    wavelet = com_sin*gauss_c
    return wavelet

def MRA(sig,fi,ff,freq_int,wavelet,freqm):
    #vect freq var
    range_cycles = [1,10] #barrido de número de ciclos
    delta = ff-fi #intervalo de frecuencias de descomposición
    num_frq = int(delta*(1/freq_int)) # número de frecuencias en que se descompone
    vfrec = np.linspace(fi,ff,num_frq) #vector de frecuencias
    num_cycles =np.logspace(np.log10(range_cycles[0]), np.log10(range_cycles[-1]),num_frq) #vector de ciclos
    #Preparation
    n,m = len(sig),len(wavelet(vfrec[0],range_cycles[0],freqm))
    p = n+m-1
    k = num_frq
    half_wav = int(np.floor(m/2))
    matrx_pad = np.zeros([k,p])
    sig_fft = sc.fft.fft(np.pad(sig,(0,p-n+1),'constant'))
    #Convolution
    conv_mat = np.zeros([k,n])
    aux_vec = []
    for i in range(k):
        wave = np.pad(wavelet(vfrec[i],num_cycles[i],freqm), (0,n),'constant')
        wave_fft = sc.fft.fft(wave) 
        wave_fft = wave_fft / wave_fft.max()
        conv_res_prim = np.multiply(sig_fft,wave_fft)
        conv_res = abs(sc.fft.ifft(conv_res_prim))**2 #resultado 
        conv_res = conv_res[half_wav:-half_wav] #recorte del padding
        for j in range(n):
            conv_mat[i][j] = conv_res[j]
    return conv_mat

