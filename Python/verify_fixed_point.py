import numpy as np
from scipy.signal import lfilter

FS = 360
Q = 15
SCALE = 2 ** Q

# Load signals
clean = np.loadtxt("Data/ecg_clean.txt")
noisy = np.loadtxt("Data/ecg_noisy.txt")

# Load Q1.15 coefficients
coefficients_q15 = np.loadtxt(
    "Coefficients/fir_coefficients_q15.txt",
    dtype=np.int16
)

# Reconstruct floating-point coefficients
coefficients_fixed = coefficients_q15.astype(np.float64) / SCALE

# Apply fixed-point coefficients using floating-point arithmetic.
# This isolates coefficient quantization effects.
filtered_fixed = lfilter(
    coefficients_fixed,
    1.0,
    noisy
)

# FFT
N = len(noisy)

noisy_fft = np.fft.rfft(noisy)
filtered_fft = np.fft.rfft(filtered_fixed)

freq = np.fft.rfftfreq(N, 1 / FS)

noisy_mag = np.abs(noisy_fft) / N
filtered_mag = np.abs(filtered_fft) / N

# Find 50 Hz bin
index_50 = np.argmin(np.abs(freq - 50))

noisy_50 = noisy_mag[index_50]
filtered_50 = filtered_mag[index_50]

attenuation_db = 20 * np.log10(
    filtered_50 / noisy_50
)

print("===== FIXED-POINT FIR VALIDATION =====")
print("Number of taps:", len(coefficients_q15))
print("Q format: Q1.15")
print("Scale factor:", SCALE)
print()

print(f"Noisy ECG 50 Hz     : {noisy_50:.10f}")
print(f"Fixed FIR 50 Hz     : {filtered_50:.10f}")
print(f"50 Hz attenuation   : {attenuation_db:.2f} dB")

print()
print("===== COEFFICIENT CHECK =====")

max_error = np.max(
    np.abs(
        np.loadtxt(
            "Coefficients/fir_coefficients_float.txt"
        ) - coefficients_fixed
    )
)

print(f"Maximum coefficient error: {max_error:.10f}")