# Grenzwerte
VOLTAGE_MIN = 11.5
VOLTAGE_MAX = 12.5
CURRENT_MAX = 0.50
TEMPERATURE_MAX = 50.0


def check_voltage(value):
    return VOLTAGE_MIN <= value <= VOLTAGE_MAX


def check_current(value):
    return value <= CURRENT_MAX


def check_temperature(value):
    return value <= TEMPERATURE_MAX