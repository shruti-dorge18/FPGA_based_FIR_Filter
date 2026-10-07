import numpy as np
import matplotlib.pyplot as plt

FS = 360
INPUT_SCALE = 28617.467248908295

NOISY_FILE = "Data/ecg_noisy_fixed.txt"
RTL_FILE = "Data/ecg_filtered_verilog.txt"

# Load fixed-point signals
noisy = np.loadtxt(NOISY_FILE, dtype=np.int16)
rtl = np.loadtxt(RTL_FILE, dtype=np.int16)

# Convert back to approximately original ECG scale
noisy = noisy / INPUT_SCALE
rtl = rtl / INPUT_SCALE

N = len(noisy)

# FFT
noisy_fft = np.abs(np.fft.rfft(noisy))
rtl_fft = np.abs(np.fft.rfft(rtl))

freq = np.fft.rfftfreq(N, 1 / FS)

# Find 50 Hz bin
idx_50 = np.argmin(np.abs(freq - 50))

noisy_50 = noisy_fft[idx_50] / N
rtl_50 = rtl_fft[idx_50] / N

attenuation = 20 * np.log10(rtl_50 / noisy_50)

print("===== RTL FIR FREQUENCY VERIFICATION =====")
print(f"Samples              : {N}")
print(f"Sampling frequency   : {FS} Hz")
print(f"50 Hz bin            : {freq[idx_50]:.2f} Hz")
print()
print(f"Noisy ECG 50 Hz      : {noisy_50:.10f}")
print(f"RTL FIR 50 Hz        : {rtl_50:.10f}")
print(f"50 Hz attenuation    : {attenuation:.2f} dB")

# Plot
plt.figure(figsize=(10, 5))

plt.plot(freq, noisy_fft / N, label="Noisy ECG")
plt.plot(freq, rtl_fft / N, label="RTL FIR Output")

plt.xlim(0, 100)
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.title("RTL FIR Filter – 50 Hz Noise Suppression")
plt.grid()
plt.legend()

plt.savefig("Data/rtl_fir_fft_comparison.png", dpi=150)
plt.show()