import pandas as pd

from src.validation import (
    check_voltage,
    check_current,
    check_temperature,
)


# Messdaten einlesen
data = pd.read_csv("data/test_run_001.csv")


# Grenzwertverletzungen bestimmen
voltage_failures = data[
    ~data["voltage_v"].apply(check_voltage)
]

current_failures = data[
    ~data["current_a"].apply(check_current)
]

temperature_failures = data[
    ~data["temperature_c"].apply(check_temperature)
]


# PASS / FAIL bestimmen
voltage_pass = voltage_failures.empty
current_pass = current_failures.empty
temperature_pass = temperature_failures.empty


# Maximalwerte bestimmen
max_voltage = data["voltage_v"].max()
max_current = data["current_a"].max()
max_temperature = data["temperature_c"].max()


# Ergebnisse ausgeben
print("AUTOMATED TEST VALIDATION")
print("-" * 50)

print(
    f"TC-001 Voltage Range Test: "
    f"{'PASS' if voltage_pass else 'FAIL'}"
)

if not voltage_pass:
    print(
        f"  Violation from "
        f"{voltage_failures['time_s'].min():.1f} s "
        f"to {voltage_failures['time_s'].max():.1f} s"
    )


print(
    f"TC-002 Current Limit Test: "
    f"{'PASS' if current_pass else 'FAIL'}"
)

if not current_pass:
    print(
        f"  Violation from "
        f"{current_failures['time_s'].min():.1f} s "
        f"to {current_failures['time_s'].max():.1f} s"
    )


print(
    f"TC-003 Temperature Limit Test: "
    f"{'PASS' if temperature_pass else 'FAIL'}"
)

if not temperature_pass:
    print(
        f"  Violation from "
        f"{temperature_failures['time_s'].min():.1f} s "
        f"to {temperature_failures['time_s'].max():.1f} s"
    )


print("-" * 50)

print(f"Maximum Voltage: {max_voltage:.2f} V")
print(f"Maximum Current: {max_current:.2f} A")
print(f"Maximum Temperature: {max_temperature:.2f} °C")

print("-" * 50)

overall_pass = (
    voltage_pass
    and current_pass
    and temperature_pass
)

print(
    f"Overall Result: "
    f"{'PASS' if overall_pass else 'FAIL'}"
)