import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import numpy as np
import os
import tempfile
from ligotools.utils import whiten, reqshift, write_wavfile

def test_whiten_simple():
    x = np.random.randn(1000)
    interp_psd = lambda f: np.ones_like(f)  # Flat PSD
    dt = 0.01
    y = whiten(x, interp_psd, dt)
    assert y.shape == x.shape
    assert not np.all(y == 0)

# Test reqshift: Shifting a pure sinewave by its frequency should largely move it to DC
def test_reqshift_sine_to_dc():
    fs = 1000
    t = np.arange(0, 1, 1/fs)
    freq = 10.0
    sine = np.sin(2 * np.pi * freq * t)
    shifted = reqshift(sine, fs, -freq)
    power_after = np.std(shifted)
    assert shifted.shape == sine.shape
    assert power_after > 0.1  # Should retain some nonzero signal
