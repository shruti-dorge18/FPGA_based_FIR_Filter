import numpy as np

INPUT_FILE = "Coefficients/fir_coefficients_float.txt"
OUTPUT_FILE = "Coefficients/fir_coefficients_q15.txt"

Q = 15
SCALE = 2 ** Q

# Load floating-point coefficients
coefficients = np.loadtxt(INPUT_FILE)

# Convert to Q1.15
coefficients_q15 = np.round(coefficients * SCALE).astype(np.int16)

# Save integer coefficients
np.savetxt(
    OUTPUT_FILE,
    coefficients_q15,
    fmt="%d"
)

print("===== Q1.15 COEFFICIENT CONVERSION =====")
print("Number of coefficients:", len(coefficients))
print("Q format: Q1.15")
print("Scale factor:", SCALE)
print()

for i, (floating, fixed) in enumerate(
    zip(coefficients, coefficients_q15)
):
    reconstructed = fixed / SCALE

    print(
        f"h[{i:3d}] = "
        f"{floating: .12f}  ->  "
        f"{fixed:6d}  ->  "
        f"{reconstructed: .12f}"
    )

print()
print("Fixed-point coefficients saved to:")
print(OUTPUT_FILE)