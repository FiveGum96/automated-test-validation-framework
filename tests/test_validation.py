from src.validation import (
    check_voltage,
    check_current,
    check_temperature,
)


# --------------------------------------------------
# Voltage Tests
# --------------------------------------------------

def test_voltage_normal_value_passes():
    assert check_voltage(12.0) is True


def test_voltage_too_high_fails():
    assert check_voltage(13.0) is False


def test_voltage_too_low_fails():
    assert check_voltage(11.0) is False


def test_voltage_upper_boundary_passes():
    assert check_voltage(12.5) is True


def test_voltage_lower_boundary_passes():
    assert check_voltage(11.5) is True


# --------------------------------------------------
# Current Tests
# --------------------------------------------------

def test_current_normal_value_passes():
    assert check_current(0.35) is True


def test_current_limit_passes():
    assert check_current(0.50) is True


def test_current_too_high_fails():
    assert check_current(0.65) is False


# --------------------------------------------------
# Temperature Tests
# --------------------------------------------------

def test_temperature_normal_value_passes():
    assert check_temperature(32.0) is True


def test_temperature_limit_passes():
    assert check_temperature(50.0) is True


def test_temperature_too_high_fails():
    assert check_temperature(58.0) is False