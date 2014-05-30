from __future__ import division

import os, yaml
import numpy as np
from scipy.integrate import simps, trapz
import scipy.io.wavfile as wv
from scipy.interpolate import interp1d
from matplotlib import mlab
from matplotlib import pyplot
from scipy.signal import hann, fftconvolve

from PyQt4.QtGui import QImage

VERBOSE = True

with open(os.path.join(os.path.dirname(os.path.dirname(__file__)),'settings.conf'), 'r') as yf:
    config = yaml.load(yf)
print 'loaded config', config
mphone_sensitivity = config['microphone_sensitivity']

def calc_db(peak, cal_peak=None):
    u""" 
    Converts voltage difference into decibels : 20*log10(peak/cal_peak)
    If calpeak not provided uses microphone sensitivity value from config file
    """
    try:
        if cal_peak:
            pbdB = 20 * np.log10(peak/cal_peak)
        else:
            pbdB = 94 + (20.*np.log10((peak/np.sqrt(2))/mphone_sensitivity))
    except ZeroDivisionError:
        print u'attempted division by zero:'
        print u'peak {}, caldb {}, calpeak {}'.format(peak, caldb, cal_peak)
        pbdB = np.nan
    return pbdB

def calc_noise(fft_vector, ix1,ix2):
    fft_slice = fft_vector[ix1:ix2]
    area = trapz(fft_slice)
    return area

def calc_spectrum(signal,rate):
    """Return the spectrum and frequency indexes for real-valued input signal"""
    npts = len(signal)
    npts = npts - (npts % 2) # for odd length signals
    freq = np.arange((npts/2)+1)/(npts/rate)
    #print('freq len ', len(freq))

    sp = np.fft.rfft(signal)/npts
    #print('sp len ', len(sp))
    return freq, abs(sp)

def get_peak(y, idx, atfrequency=None):
    """ 
    Find the peak value for the input vector
    :param y: data vector
    :type y: numpy.ndarray
    :param idx: index values for y
    :type y: numpy.ndarray
    :returns: (int, int) peak value and the value of the index it was found at
    """
    if atfrequency is None:
        maxidx = y.argmax(axis=0)
        f = idx[maxidx]
        spec_peak = np.amax(y)
    else:
        f = atfrequency
        spec_peak = y[idx==f]
    return spec_peak, f

def make_tone(freq,db,dur,risefall,samplerate, caldb=100, calv=0.1):
    """
    Produce a pure tone signal 

    :param freq: Frequency of the tone to be produced (Hz)
    :type freq: int
    :param db: Intensity of the tone in dB SPL
    :type db: int
    :param dur: duration (seconds)
    :type dur: float
    :param risefall: linear rise fall of (seconds)
    :type risefall: float
    :param samplerate: generation frequency of tone (Hz)
    :type samplerate: int
    :param caldb: Reference intensity (dB SPL). Together with calv, provides a reference point for what intensity equals what output voltage level
    :type caldb: int
    :param calv: Reference voltage (V). Together with caldb, provides a reference point for what intensity equals what output voltage level
    :type calv: float
    :returns: tone, timevals -- the signal and the time index values
    """
    npts = dur * samplerate
    try:
        amp = (10 ** ((db-caldb)/20)*calv)

        if VERBOSE:
            print("current dB: {}, fs: {}, current frequency: {} kHz, AO Amp: {:.6f}".format(db, samplerate, freq/1000, amp))
            print("cal dB: {}, V at cal dB: {}".format(caldb, calv))
    
        tone = amp * np.sin((freq*dur) * np.linspace(0, 2*np.pi, npts))
                  
        print 'tone max', np.amax(tone)  
        if risefall > 0:
            rf_npts = int(risefall * samplerate)
            # print('amp {}, freq {}, npts {}, rf_npts {}'.format(amp,freq,npts,rf_npts))
            wnd = hann(rf_npts*2) # cosine taper
            tone[:rf_npts] = tone[:rf_npts] * wnd[:rf_npts]
            tone[-rf_npts:] = tone[-rf_npts:] * wnd[rf_npts:]

        timevals = np.arange(npts)/samplerate

    except:
        print("WARNING: Unable to produce tone")
        tone = np.zeros(npts)
        timevals = np.arange(npts)/samplerate
        raise

    return tone, timevals


def spectrogram(source, nfft=512, overlap=90, window='hanning', caldb=93, calv=2.83):
    """
    Produce a matrix of spectral intensity, uses matplotlib's specgram
    function. Output is in dB scale.

    :param source: filename of audiofile, or samplerate and vector of audio signal
    :type source: str or (int, numpy.ndarray)
    :param nfft: size of nfft window to use
    :type nfft: int
    :param overlap: percent overlap of window
    :type overlap: number
    :param window: Type of window to use, choices are hanning, hamming, blackman, bartlett or none (rectangular)
    :type window: string
    :returns: spec -- 2D array of intensities, freqs -- yaxis labels, bins -- time bin labels, duration -- duration of signal
    """
    if isinstance(source, basestring):
        try:
            sr, wavdata = wv.read(source)
        except:
            print u"Problem reading wav file"
            raise
        wavdata = wavdata.astype(float)
    else:
        sr, wavdata = source
        
    #truncate to nears ms
    duration = float(len(wavdata))/sr
    desired_npts = int((np.trunc(duration*1000)/1000)*sr)
    wavdata = wavdata[:desired_npts]
    duration = len(wavdata)/sr

    rms = np.sqrt(np.mean(pow(wavdata,2))) / np.sqrt(2)
    print 'spec rms', rms
    # normalize
    # if np.max(abs(wavdata)) != 0:
    #     wavdata = wavdata/np.max(abs(wavdata))

    if window == 'hanning':
        winfnc = mlab.window_hanning
    elif window == 'hamming':
        winfnc = np.hamming(nfft)
    elif window == 'blackman':
        winfnc = np.blackman(nfft)
    elif window == 'bartlett':
        winfnc = np.bartlett(nfft)
    elif window == None or window == 'none':
        winfnc = mlab.window_none

    noverlap = int(nfft*(float(overlap)/100))

    Pxx, freqs, bins = mlab.specgram(wavdata, NFFT=nfft, Fs=sr, noverlap=noverlap,
                                     pad_to=nfft*2, window=winfnc, detrend=mlab.detrend_none,
                                     sides='default', scale_by_freq=False)

    # convert to db scale for display
    spec = 20. * np.log10(Pxx) + caldb
    
    # inf values prevent spec from drawing in pyqtgraph
    # ... so set to miniumum value in spec?
    # would be great to have spec in db SPL, and set any -inf to 0
    spec[np.isneginf(spec)] = np.nan
    spec[np.isnan(spec)] = np.nanmin(spec)

    return spec, freqs, bins, duration

def smooth(x, window_len=99, window='hanning'):
    """smooth the data using a window with requested size.
    
    This method is based on the convolution of a scaled window with the signal.
    The signal is prepared by introducing reflected copies of the signal 
    (with the window size) in both ends so that transient parts are minimized
    in the begining and end part of the output signal.
    
    input:
        x: the input signal 
        window_len: the dimension of the smoothing window; should be an odd integer

    output:
        the smoothed signal
        
    example:

    t=linspace(-2,2,0.1)
    x=sin(t)+randn(len(t))*0.1
    y=smooth(x)
    
    see also: 
    
    numpy.hanning, numpy.hamming, numpy.bartlett, numpy.blackman, numpy.convolve
    scipy.signal.lfilter

    Based from Scipy Cookbook
    """

    if x.ndim != 1:
        raise ValueError, "smooth only accepts 1 dimension arrays."

    if x.size < window_len:
        raise ValueError, "Input vector needs to be bigger than window size."


    if window_len < 3:
        return x
    if window_len % 2 == 0:
        window_len +=1

    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman', 'kaiser']:
        raise ValueError, "Window is one of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'"


    s=np.r_[x[window_len-1:0:-1],x,x[-1:-window_len:-1]]
    if window == 'flat': #moving average
        w = np.ones(window_len,'d')
    elif window == 'kaiser':
        w = np.kaiser(window_len,4)
    else:
        w = eval('np.'+window+'(window_len)')

    y = np.convolve(w/w.sum(),s,mode='valid')
    return y[window_len/2-1:len(y)-window_len/2]


def convolve_filter(signal, impulse_response):
    """
    Convovle the two input signals, if impulse_response is None,
    returns the unaltered signal
    """
    if impulse_response is not None:
        # print 'interpolated calibration'#, self.calibration_frequencies
        adjusted_signal = fftconvolve(signal, impulse_response)
        adjusted_signal = adjusted_signal[len(impulse_response)/2:len(adjusted_signal)-len(impulse_response)/2 + 1]
        return adjusted_signal
    else:
        return signal


def calc_impulse_response(genrate, fresponse, frequencies, frange, truncation_factor=64):
    """
    Calculate filter kernel from attenuation vector.
    Attenuation vector should represent magnitude frequency response of system
    :param genrate: The generation samplerate at which the test signal was played
    :type genrate: int
    :param fresponse: Frequency response of the system, i.e. relative attenuations of frequencies
    :type fresponse: numpy.ndarray
    :param frequencies: corresponding frequencies for the fresponse
    :type frequencies: numpy.ndarray
    :param frange: the min and max frequencies for which the filter kernel will affect
    :type frange: (int, int)
    :param truncation_factor: the factor by which to reduce the size of the impluse repsonse. e.g. a factor of 4 will produce an impulse response that is 1/4 the length of the input signal.
    :type truncation_factor: int
    :returns: numpy.ndarray -- the impulse response
    """

    freq = frequencies
    max_freq = genrate/2+1

    attenuations = np.zeros_like(fresponse)
    # add extra points for windowing
    winsz = 0.05 # percent
    lowf = max(0, frange[0] - (frange[1] - frange[0])*winsz)
    highf = min(frequencies[-1], frange[1] + (frange[1] - frange[0])*winsz)

    f0 = (np.abs(freq-lowf)).argmin()
    f1 = (np.abs(freq-highf)).argmin()
    fmax = (np.abs(freq-max_freq)).argmin()
    attenuations[f0:f1] = fresponse[f0:f1]*tukey(len(fresponse[f0:f1]), winsz)
    freq_response = 10**((attenuations).astype(float)/20)

    freq_response = freq_response[:fmax]

    impulse_response = np.fft.irfft(freq_response)
    
    # rotate to create causal filter, and truncate
    impulse_response = np.roll(impulse_response, len(impulse_response)//2)

    # truncate
    impulse_response = impulse_response[(len(impulse_response)//2)-(len(impulse_response)//truncation_factor//2):(len(impulse_response)//2)+(len(impulse_response)//truncation_factor//2)]
    
    # should I also window the impulse response - by how much?
    impulse_response = impulse_response * tukey(len(impulse_response), 0.05)

    return impulse_response

def calc_attenuation_curve(signal, resp, fs, calf, smooth_pts=99):
    """
    Calculate an attenuation roll-off curve, from a signal and its recording

    :param signal: ouput signal delivered to the generation hardware
    :type signal: numpy.ndarray    
    :param resp: recording of given signal, as recieved from microphone
    :type resp: numpy.ndarray
    :param fs: input and output samplerate (should be the same)
    :type fs: int
    :param smooth_pts: amount of averaging to use on the result
    :type smooth_pts: int
    :returns: numpy.ndarray -- attenuation vector
    """
    # remove dc offset
    resp = resp - np.mean(resp)

    y = resp
    x = signal

    # convert time signals to frequency domain
    Y = np.fft.rfft(y)
    X = np.fft.rfft(x)

    # take the magnitude of signals
    Ymag = np.sqrt(Y.real**2 + Y.imag**2) # equivalent to abs(Y)
    Xmag = np.sqrt(X.real**2 + X.imag**2)

    # convert to decibel scale
    YmagdB = 20 * np.log10(Ymag)
    XmagdB = 20 * np.log10(Xmag)

    # now we can substract to get attenuation curve
    diffdB = XmagdB - YmagdB

    # may want to smooth results here?
    diffdB = smooth(diffdB, smooth_pts)

    # frequencies present in calibration spectrum
    npts = len(y)
    fq = np.arange(npts/2+1)/(float(npts)/fs)

    # shift by the given calibration frequency to align attenutation
    # with reference point set by user
    diffdB -= diffdB[fq == calf]

    return diffdB

def bb_calibration(signal, resp, fs, frange):
    """Given original signal and recording, spits out a calibrated signal"""
    # remove dc offset from recorded response (synthesized orignal shouldn't have one)
    dc = np.mean(resp)
    resp = resp - dc

    npts = len(signal)
    f0 = np.ceil(frange[0]/(float(fs)/npts))
    f1 = np.floor(frange[1]/(float(fs)/npts))

    y = resp
    # y = y/np.amax(y) # normalize
    Y = np.fft.rfft(y)

    x = signal
    # x = x/np.amax(x) # normalize
    X = np.fft.rfft(x)

    H = Y/X

    # still issues warning because all of Y/X is executed to selected answers from
    # H = np.where(X.real!=0, Y/X, 1)
    # H[:f0].real = 1
    # H[f1:].real = 1
    # H = smooth(H)

    A = X / H

    return np.fft.irfft(A)


def multiply_frequencies(signal, fs, frange, calfqs, calvals):
    """Given a vector of dB attenuations, adjust signal by 
       multiplication in the frequency domain"""
    pad_factor = 1.2
    npts = len(signal)

    X = np.fft.rfft(signal,  n=int(len(signal)*pad_factor))

    f = np.arange(len(X))/(float(npts)/fs*pad_factor)
    f0 = (np.abs(f-frange[0])).argmin()
    f1 = (np.abs(f-frange[1])).argmin()

    cal_func = interp1d(calfqs, calvals)
    frange = f[f0:f1]
    Hroi = cal_func(frange)
    H = np.zeros((len(X),))
    H[f0:f1] = Hroi

    H = smooth(H)

    H = 10**((H).astype(float)/20)

    # Xadjusted = X.copy()
    # Xadjusted[f0:f1] *= H
    # Xadjusted = smooth(Xadjusted)

    Xadjusted = X*H

    signal_calibrated = np.fft.irfft(Xadjusted)
    return signal_calibrated[:len(signal)]


def tukey(winlen, alpha):
    """
    Generate a tukey (tapered cosine) window
    :param winlen: length of the window, in samples
    :type winlen: int
    :param alpha: proportion of the window to be tapered. 
    0 = rectangular window
    1.0 = hann window
    :type alpha: float
    """
    taper = hann(winlen*alpha)
    rect = np.ones(winlen-len(taper) + 1)
    win = fftconvolve(taper, rect)
    win = win / np.amax(win)
    return win