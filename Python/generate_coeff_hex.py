import numpy as np

INPUT_FILE = "Coefficients/fir_coefficients_q15.txt"
OUTPUT_FILE = "Coefficients/fir_coefficients_q15.hex"

coefficients = np.loadtxt(
    INPUT_FILE,
    dtype=np.int16
)

with open(OUTPUT_FILE, "w") as f:
    for coeff in coefficients:
        value = int(coeff) & 0xFFFF
        f.write(f"{value:04X}\n")

print("===== VERILOG COEFFICIENT FILE =====")
print("Number of coefficients:", len(coefficients))
print("Output:", OUTPUT_FILE)

print()
print("First 5 coefficients:")
for coeff in coefficients[:5]:
    print(f"{int(coeff):6d} -> {int(coeff) & 0xFFFF:04X}")

print()
print("Last 5 coefficients:")
for coeff in coefficients[-5:]:
    print(f"{int(coeff):6d} -> {int(coeff) & 0xFFFF:04X}")