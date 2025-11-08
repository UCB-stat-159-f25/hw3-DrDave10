import numpy as np
import scipy.signal
from scipy.io import wavfile
import matplotlib.pyplot as plt


def whiten(strain, interp_psd, dt):
    Nt = len(strain)
    freqs = np.fft.rfftfreq(Nt, dt)
    freqs1 = np.linspace(0, 2048, Nt // 2 + 1)

    # whitening: transform to freq domain, divide by asd, then transform back, 
    # taking care to get normalization right.
    hf = np.fft.rfft(strain)
    norm = 1./np.sqrt(1./(dt*2))
    white_hf = hf / np.sqrt(interp_psd(freqs)) * norm
    white_ht = np.fft.irfft(white_hf, n=Nt)
    return white_ht


def write_wavfile(filename,fs,data):
    d = np.int16(data/np.max(np.abs(data)) * 32767 * 0.9)
    wavfile.write(filename,int(fs), d)


def reqshift(data,fshift=100,sample_rate=4096):
    """Frequency shift the signal by constant
    """
    x = np.fft.rfft(data)
    T = len(data)/float(sample_rate)
    df = 1.0/T
    nbins = int(fshift/df)
    # print T,df,nbins,x.real.shape
    y = np.roll(x.real,nbins) + 1j*np.roll(x.imag,nbins)
    y[0:nbins]=0.
    z = np.fft.irfft(y)
    return z


def plot_psd(frequencies, psd_values, label=None, plottype='png', path='figures/'):
    """Plot and save a PSD plot to the given directory."""
    plt.figure(figsize=(8,4))
    plt.loglog(frequencies, psd_values, label=label)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Power Spectral Density')
    plt.title('Power Spectral Density')
    if label is not None:
        plt.legend()
    plt.grid(True, which='both', ls='--')
    plt.tight_layout()
    filename = f'{path}psd_plot.{plottype}'
    plt.savefig(filename)
    plt.close()

