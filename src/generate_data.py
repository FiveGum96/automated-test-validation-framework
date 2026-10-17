import numpy as np
import pandas as pd

np.random.seed(42)

samples = 500

time = np.arange(samples) * 0.1

voltage = np.random.normal(12.0, 0.1, samples)
current = np.random.normal(0.35, 0.03, samples)
temperature = np.random.normal(32.0, 2.0, samples)

# Absichtlich eingebaute Fehler
voltage[150:160] = 12.8
current[280:290] = 0.65
temperature[400:420] = 58.0

data = pd.DataFrame({
    "time_s": time,
    "voltage_v": voltage,
    "current_a": current,
    "temperature_c": temperature
})

data.to_csv("data/test_run_001.csv", index=False)

print("Test data generated successfully.")