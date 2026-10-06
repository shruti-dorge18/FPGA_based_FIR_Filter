import numpy as np
import matplotlib.pyplot as plt

FS = 360
F_NOISE = 50
NOISE_AMPLITUDE = 0.2

# Load clean ECG
ecg = np.loadtxt("Data/ecg_clean.txt")

# Time axis
t = np.arange(len(ecg)) / FS

# Generate 50 Hz power-line interference
noise = NOISE_AMPLITUDE * np.sin(2 * np.pi * F_NOISE * t)

# Add noise to ECG
ecg_noisy = ecg + noise

# Save noisy ECG
np.savetxt(
    "Data/ecg_noisy.txt",
    ecg_noisy,
    fmt="%.8f"
)

print("Sampling frequency:", FS, "Hz")
print("Noise frequency:", F_NOISE, "Hz")
print("Noise amplitude:", NOISE_AMPLITUDE)
print("Number of samples:", len(ecg_noisy))

# Plot clean and noisy ECG
plt.figure(figsize=(12, 6))

plt.plot(t, ecg, label="Clean ECG")
plt.plot(t, ecg_noisy, label="Noisy ECG")

plt.xlabel("Time (seconds)")
plt.ylabel("Amplitude")
plt.title("ECG with 50 Hz Power-Line Interference")
plt.legend()
plt.grid()

plt.savefig("Data/ecg_noise_comparison.png", dpi=150)