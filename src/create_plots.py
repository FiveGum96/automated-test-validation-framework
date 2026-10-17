import os

import matplotlib.pyplot as plt
import pandas as pd


# Grenzwerte
VOLTAGE_MIN = 11.5
VOLTAGE_MAX = 12.5
CURRENT_MAX = 0.50
TEMPERATURE_MAX = 50.0


# Messdaten einlesen
data = pd.read_csv("data/test_run_001.csv")


# Sicherstellen, dass der Zielordner existiert
os.makedirs("reports/plots", exist_ok=True)


# --------------------------------------------------
# Spannung
# --------------------------------------------------

plt.figure(figsize=(10, 5))

plt.plot(
    data["time_s"],
    data["voltage_v"],
    label="Measured Voltage"
)

plt.axhline(
    VOLTAGE_MAX,
    linestyle="--",
    label="Upper Limit"
)

plt.axhline(
    VOLTAGE_MIN,
    linestyle="--",
    label="Lower Limit"
)

plt.xlabel("Time [s]")
plt.ylabel("Voltage [V]")
plt.title("Voltage over Time")

plt.legend()
plt.grid()

plt.tight_layout()

plt.savefig(
    "reports/plots/voltage_plot.png"
)

plt.close()


# --------------------------------------------------
# Strom
# --------------------------------------------------

plt.figure(figsize=(10, 5))

plt.plot(
    data["time_s"],
    data["current_a"],
    label="Measured Current"
)

plt.axhline(
    CURRENT_MAX,
    linestyle="--",
    label="Current Limit"
)

plt.xlabel("Time [s]")
plt.ylabel("Current [A]")
plt.title("Current over Time")

plt.legend()
plt.grid()

plt.tight_layout()

plt.savefig(
    "reports/plots/current_plot.png"
)

plt.close()


# --------------------------------------------------
# Temperatur
# --------------------------------------------------

plt.figure(figsize=(10, 5))

plt.plot(
    data["time_s"],
    data["temperature_c"],
    label="Measured Temperature"
)

plt.axhline(
    TEMPERATURE_MAX,
    linestyle="--",
    label="Temperature Limit"
)

plt.xlabel("Time [s]")
plt.ylabel("Temperature [°C]")
plt.title("Temperature over Time")

plt.legend()
plt.grid()

plt.tight_layout()

plt.savefig(
    "reports/plots/temperature_plot.png"
)

plt.close()


print("Plots generated successfully.")