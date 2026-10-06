import wfdb
import numpy as np
import matplotlib.pyplot as plt

FS = 360
NUM_SAMPLES = 3600

record = wfdb.rdrecord(
    "100",
    pn_dir="mitdb",
    sampto=NUM_SAMPLES
)

ecg = record.p_signal[:, 0]

print("Sampling frequency:", record.fs)
print("Number of samples:", len(ecg))
print("Signal:", record.sig_name[0])

np.savetxt(
    "Data/ecg_clean.txt",
    ecg,
    fmt="%.8f"
)

time = np.arange(len(ecg)) / FS

plt.figure(figsize=(12, 4))
plt.plot(time, ecg)
plt.xlabel("Time (seconds)")
plt.ylabel("Amplitude")
plt.title("Clean ECG - MIT-BIH Record 100")
plt.grid()
plt.show()