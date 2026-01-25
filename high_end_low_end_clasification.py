import psutil
import platform

def classify_device():
    score = 0
    cores = psutil.cpu_count(logical=False)
    freq = psutil.cpu_freq().max
    ram = psutil.virtual_memory().total / (1024**3)
    arch = platform.machine()

    score += 1 if cores <= 4 else 2 if cores <= 8 else 3
    score += 1 if freq < 1800 else 2 if freq < 2800 else 3
    score += 1 if ram <= 4 else 2 if ram < 16 else 3
    score += 1 if "arm" in arch.lower() else 3

    if score <= 7: return "LOW-END"
    elif score <= 11: return "MID-RANGE"
    else: return "HIGH-END"
