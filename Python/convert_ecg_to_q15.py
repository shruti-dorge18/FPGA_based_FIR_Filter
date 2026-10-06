import numpy as np

INPUT_FILE = "Data/ecg_noisy.txt"
OUTPUT_FILE = "Data/ecg_noisy_fixed.txt"

ecg = np.loadtxt(INPUT_FILE)

max_ecg = np.max(np.abs(ecg))

input_scale = 32767 / max_ecg

ecg_q15 = np.round(
    ecg * input_scale
).astype(np.int16)

np.savetxt(
    OUTPUT_FILE,
    ecg_q15,
    fmt="%d"
)

print("===== ECG Q15 CONVERSION =====")
print("Input samples :", len(ecg))
print("Maximum ECG   :", max_ecg)
print("Scale factor  :", input_scale)

print()
print("First 10 samples:")

for i in range(10):
    print(
        f"{ecg[i]: .8f} -> {ecg_q15[i]}"
    )

print()
print("Output:")
print(OUTPUT_FILE)