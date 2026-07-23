import numpy as np

# This code will generate a sinusoidal wave form and descretize it in either 8 or 32
# data points. The more datapoints, the more qubits required to encode. 

def generate_eeg_signal_8(sampling_rate=128, duration=0.0625): 
    """ 
    Generates a synthetic EEG signal combining 7 Hz and 15 Hz oscillations, 
    and returns 8 normalized amplitude data points. 
    """ 
    # 128 Hz sampling rate for 0.0625 seconds gives exactly 8 points 
    t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False) 
     
    # Simulate an organic brainwave (7 Hz wave + 15 Hz wave) 
    wave_7hz = np.sin(2 * np.pi * 7 * t) 
    wave_15hz = np.sin(2 * np.pi * 15 * t) 
    raw_signal = wave_7hz + wave_15hz 
     
    # AMPLITUDE ENCODING REQUIREMENT: Vector must be normalized (sum of squares = 1) 
    norm_factor = np.linalg.norm(raw_signal) 
    normalized_signal = raw_signal / norm_factor 
     
    return t, raw_signal, normalized_signal,  wave_7hz, wave_15hz

def generate_eeg_signal_32(sampling_rate=512, duration=0.0625): 
    """ 
    Generates a synthetic EEG signal combining 7 Hz and 15 Hz oscillations, 
    and returns 32 normalized amplitude data points for 5-qubit state initialization. 
    """ 
    # 512 Hz sampling rate for 0.0625 seconds gives exactly 32 points 
    num_points = int(sampling_rate * duration)
    t = np.linspace(0, duration, num_points, endpoint=False) 
     
    # Simulate an organic brainwave (7 Hz wave + 15 Hz wave) 
    wave_7hz = np.sin(2 * np.pi * 7 * t) 
    wave_15hz = np.sin(2 * np.pi * 15 * t) 
    raw_signal = wave_7hz + wave_15hz 
     
    # AMPLITUDE ENCODING REQUIREMENT: Vector must be normalized (sum of squares = 1) 
    norm_factor = np.linalg.norm(raw_signal) 
    normalized_signal = raw_signal / norm_factor 
     
    return t, raw_signal, normalized_signal,  wave_7hz, wave_15hz

def generate_eeg_signal_128(sampling_rate=512, duration=0.25):
    """
    Generates a synthetic EEG signal combining 7 Hz and 15 Hz oscillations,
    and returns 128 normalized amplitude data points for 7-qubit state initialization.
    """

    # 512 Hz sampling rate for 0.25 seconds gives exactly 128 points
    num_points = int(sampling_rate * duration)
    t = np.linspace(0, duration, num_points, endpoint=False)

    # Simulate an organic brainwave (7 Hz + 15 Hz)
    wave_7hz = np.sin(2 * np.pi * 7 * t)
    wave_15hz = np.sin(2 * np.pi * 15 * t)
    raw_signal = wave_7hz + wave_15hz

    # Normalize for amplitude encoding
    norm_factor = np.linalg.norm(raw_signal)
    normalized_signal = raw_signal / norm_factor

    return t, raw_signal, normalized_signal,  wave_7hz, wave_15hz