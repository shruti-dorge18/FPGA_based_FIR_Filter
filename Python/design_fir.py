import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import firls

FS = 360
NUM_TAPS = 121

# FIR notch filter
bands = [
    0, 47,
    49, 51,
    53, 180
]

desired = [
    1, 1,
    0, 0,
    1, 1
]

coefficients = firls(
    NUM_TAPS,
    bands,
    desired,
    fs=FS
)

# Save coefficients
np.savetxt(
    "Coefficients/fir_coefficients_float.txt",
    coefficients,
    fmt="%.12f"
)

print("===== FIR COEFFICIENTS =====")
for i, coeff in enumerate(coefficients):
    print(f"h[{i:2d}] = {coeff:.12f}")

print()
print("Number of taps:", NUM_TAPS)
print("Sampling frequency:", FS, "Hz")

# Frequency response
frequency = np.linspace(0, FS / 2, 4096)

from scipy.signal import freqz

frequency, response = freqz(
    coefficients,
    worN=4096,
    fs=FS
)

magnitude_db = 20 * np.log10(
    np.maximum(np.abs(response), 1e-12)
)

plt.figure(figsize=(12, 5))
plt.plot(frequency, magnitude_db)
plt.axvline(50, linestyle="--", label="50 Hz")
plt.axhline(-3, linestyle="--", label="-3 dB")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude (dB)")
plt.title("61-Tap FIR Notch Filter Frequency Response")
plt.xlim(0, 180)
plt.ylim(-100, 5)
plt.grid()
plt.legend()

plt.savefig(
    "Data/fir_frequency_response.png",
    dpi=150
)

print()
print("Frequency response saved to:")
print("Data/fir_frequency_response.png")