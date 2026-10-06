import numpy as np

PYTHON_FILE = "Data/ecg_filtered_fixed.txt"
VERILOG_FILE = "Data/ecg_filtered_verilog.txt"

# Same input scaling used by fixed_point_fir.py
MAX_ECG = 1.145
INPUT_SCALE = 32767 / MAX_ECG

# Python fixed-point output is stored as floating point.
python_float = np.loadtxt(PYTHON_FILE)

# Convert Python reference back to the exact 16-bit representation
python_output = np.round(
    python_float * INPUT_SCALE
).astype(np.int16)

# Verilog output is already signed 16-bit integers.
verilog_output = np.loadtxt(
    VERILOG_FILE,
    dtype=np.int16
)

print("===== RTL vs PYTHON COMPARISON =====")
print("Python samples :", len(python_output))
print("RTL samples    :", len(verilog_output))
print()

if len(python_output) != len(verilog_output):
    print("ERROR: Number of samples does not match.")
    exit()

difference = (
    verilog_output.astype(np.int32)
    - python_output.astype(np.int32)
)

absolute_difference = np.abs(difference)

print(
    "Maximum absolute difference:",
    np.max(absolute_difference)
)

print(
    "Mean absolute difference   :",
    np.mean(absolute_difference)
)

print(
    "Matching samples           :",
    np.sum(difference == 0)
)

print(
    "Different samples          :",
    np.sum(difference != 0)
)

print()

mismatch_indices = np.where(difference != 0)[0]

if len(mismatch_indices) == 0:

    print("PASS: RTL output is bit-exact with Python.")

else:

    print("First mismatches:")

    for i in mismatch_indices[:10]:
        print(
            f"sample {i}: "
            f"Python={python_output[i]}, "
            f"RTL={verilog_output[i]}, "
            f"difference={difference[i]}"
        )

    print()
    print("FAIL: RTL output does not exactly match Python.")