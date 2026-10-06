import numpy as np
import matplotlib.pyplot as plt

FS = 360

# Load ECG signals
clean = np.loadtxt("Data/ecg_clean.txt")
noisy = np.loadtxt("Data/ecg_noisy.txt")

N = len(clean)

# FFT
clean_fft = np.fft.rfft(clean)
noisy_fft = np.fft.rfft(noisy)

freq = np.fft.rfftfreq(N, 1 / FS)

# Magnitude spectrum
clean_mag = np.abs(clean_fft) / N
noisy_mag = np.abs(noisy_fft) / N

# Find frequency with maximum magnitude
clean_peak = freq[np.argmax(clean_mag[1:]) + 1]
noisy_peak = freq[np.argmax(noisy_mag[1:]) + 1]

print("Sampling frequency:", FS, "Hz")
print("Number of samples:", N)
print("Clean ECG peak frequency:", clean_peak, "Hz")
print("Noisy ECG peak frequency:", noisy_peak, "Hz")

# Find magnitude around 50 Hz
index_50 = np.argmin(np.abs(freq - 50))

print("Magnitude at 50 Hz:")
print("Clean ECG :", clean_mag[index_50])
print("Noisy ECG :", noisy_mag[index_50])

# Plot spectrum
plt.figure(figsize=(12, 5))

plt.plot(freq, clean_mag, label="Clean ECG")
plt.plot(freq, noisy_mag, label="Noisy ECG")

plt.xlim(0, 100)
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.title("ECG Frequency Spectrum")
plt.legend()
plt.grid()

plt.savefig("Data/ecg_fft.png", dpi=150)

print("FFT plot saved as Data/ecg_fft.png")