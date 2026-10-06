import numpy as np

FS = 360
Q = 15
SCALE = 2 ** Q

NUM_TAPS = 121

INPUT_FILE = "Data/ecg_noisy.txt"
COEFF_FILE = "Coefficients/fir_coefficients_q15.txt"
OUTPUT_FILE = "Data/ecg_filtered_fixed.txt"


# --------------------------------------------------
# Load data
# --------------------------------------------------

ecg = np.loadtxt(INPUT_FILE)

coefficients_q15 = np.loadtxt(
    COEFF_FILE,
    dtype=np.int16
)

print("===== INTEGER FIXED-POINT FIR =====")
print("Number of taps:", len(coefficients_q15))
print("Q format: Q1.15")
print("Input samples:", len(ecg))
print()


# --------------------------------------------------
# Convert ECG samples to signed 16-bit integers
# --------------------------------------------------

max_ecg = np.max(np.abs(ecg))

input_scale = 32767 / max_ecg

ecg_q15 = np.round(
    ecg * input_scale
).astype(np.int16)

print("Maximum ECG magnitude :", max_ecg)
print("Input scaling factor  :", input_scale)
print()


# --------------------------------------------------
# FIR filtering using integer arithmetic
# --------------------------------------------------

output_q15 = np.zeros(len(ecg_q15), dtype=np.int16)

# 64-bit accumulator models a wide FPGA accumulator.
for n in range(len(ecg_q15)):

    accumulator = np.int64(0)

    for k in range(NUM_TAPS):

        if n >= k:
            product = (
                np.int64(ecg_q15[n - k])
                * np.int64(coefficients_q15[k])
            )

            accumulator += product

    # Q15 × Q15 = Q30
    # Shift right by 15 to return to Q15
    output_value = accumulator >> Q

    # Saturate to signed 16-bit range
    if output_value > 32767:
        output_value = 32767

    elif output_value < -32768:
        output_value = -32768

    output_q15[n] = output_value


# --------------------------------------------------
# Convert back to floating point
# --------------------------------------------------

filtered = output_q15.astype(np.float64) / input_scale

np.savetxt(
    OUTPUT_FILE,
    filtered,
    fmt="%.10f"
)


# --------------------------------------------------
# 50 Hz verification
# --------------------------------------------------

N = len(ecg)

noisy_fft = np.fft.rfft(ecg)
filtered_fft = np.fft.rfft(filtered)

freq = np.fft.rfftfreq(N, 1 / FS)

noisy_mag = np.abs(noisy_fft) / N
filtered_mag = np.abs(filtered_fft) / N

index_50 = np.argmin(
    np.abs(freq - 50)
)

noisy_50 = noisy_mag[index_50]
filtered_50 = filtered_mag[index_50]

attenuation_db = 20 * np.log10(
    filtered_50 / noisy_50
)


# --------------------------------------------------
# Results
# --------------------------------------------------

print("===== FIXED-POINT RESULTS =====")
print(f"Noisy ECG 50 Hz       : {noisy_50:.10f}")
print(f"Integer FIR 50 Hz     : {filtered_50:.10f}")
print(f"50 Hz attenuation     : {attenuation_db:.2f} dB")

print()
print("Output saved to:")
print(OUTPUT_FILE)