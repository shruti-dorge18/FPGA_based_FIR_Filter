import numpy as np
from scipy.signal import freqz

FS = 360

clean = np.loadtxt("Data/ecg_clean.txt")
noisy = np.loadtxt("Data/ecg_noisy.txt")
filtered = np.loadtxt("Data/ecg_filtered.txt")

N = len(clean)

# FFT
clean_fft = np.fft.rfft(clean)
noisy_fft = np.fft.rfft(noisy)
filtered_fft = np.fft.rfft(filtered)

freq = np.fft.rfftfreq(N, 1 / FS)

clean_mag = np.abs(clean_fft) / N
noisy_mag = np.abs(noisy_fft) / N
filtered_mag = np.abs(filtered_fft) / N

# Find 50 Hz bin
index_50 = np.argmin(np.abs(freq - 50))

clean_50 = clean_mag[index_50]
noisy_50 = noisy_mag[index_50]
filtered_50 = filtered_mag[index_50]

print("===== 50 Hz COMPONENT =====")
print(f"Clean ECG   : {clean_50:.10f}")
print(f"Noisy ECG   : {noisy_50:.10f}")
print(f"Filtered ECG: {filtered_50:.10f}")

# Attenuation
attenuation_db = 20 * np.log10(filtered_50 / noisy_50)

print()
print(f"50 Hz attenuation: {attenuation_db:.2f} dB")

# FIR frequency response
coefficients = np.loadtxt(
    "Coefficients/fir_coefficients_float.txt"
)

frequency, response = freqz(
    coefficients,
    worN=4096,
    fs=FS
)

index_response_50 = np.argmin(
    np.abs(frequency - 50)
)

filter_gain_50 = abs(response[index_response_50])

filter_gain_db = 20 * np.log10(
    max(filter_gain_50, 1e-12)
)

print()
print("===== FIR RESPONSE =====")
print(f"Filter gain at 50 Hz: {filter_gain_db:.2f} dB")