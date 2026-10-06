import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import lfilter

# Load data
clean = np.loadtxt("Data/ecg_clean.txt")
noisy = np.loadtxt("Data/ecg_noisy.txt")

# Load FIR coefficients
coefficients = np.loadtxt(
    "Coefficients/fir_coefficients_float.txt"
)

# Apply FIR filter
filtered = lfilter(coefficients, 1.0, noisy)

# Save filtered ECG
np.savetxt(
    "Data/ecg_filtered.txt",
    filtered,
    fmt="%.8f"
)

print("FIR filtering completed")
print("Input samples:", len(noisy))
print("Output samples:", len(filtered))
print("Number of taps:", len(coefficients))

# Plot comparison
plt.figure(figsize=(12, 6))

plt.plot(clean, label="Clean ECG")
plt.plot(noisy, label="Noisy ECG")
plt.plot(filtered, label="Filtered ECG")

plt.xlabel("Sample")
plt.ylabel("Amplitude")
plt.title("ECG FIR Filtering")
plt.legend()
plt.grid()

plt.savefig(
    "Data/ecg_fir_comparison.png",
    dpi=150
)

print("Filtered ECG saved to:")
print("Data/ecg_filtered.txt")

print("Comparison plot saved to:")
print("Data/ecg_fir_comparison.png")