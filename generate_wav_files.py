import numpy as np
from scipy.io.wavfile import write

# Settings
sample_rate = 192000  # High sample rate to support >20kHz (192 kHz is common for pro audio)
duration = 10  # seconds
frequency = 25000  # 25 kHz (ultrasonic)

# Time array
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

# Generate sine wave
wave = 0.5 * np.sin(2 * np.pi * frequency * t)

# Convert to 16-bit PCM
audio = np.int16(wave * 32767)

# Save to .wav file
write("ultrasonic_25kHz.wav", sample_rate, audio)
