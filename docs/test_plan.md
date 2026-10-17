# Automated Test Validation Framework
## Test Plan

### TC-001 - Voltage Range Test

Requirement:
REQ-001

Objective:
Verify that the system voltage remains within the allowed range.

Input:
Voltage measurement data from test_run_001.csv

Expected Result:
All voltage values shall remain between 11.5 V and 12.5 V.

Evaluation:
PASS if all values are within the allowed range.
FAIL if at least one value is outside the allowed range.


### TC-002 - Current Limit Test

Requirement:
REQ-002

Objective:
Verify that the system current does not exceed the maximum allowed value.

Input:
Current measurement data from test_run_001.csv

Expected Result:
The current shall not exceed 0.50 A.

Evaluation:
PASS if all current values are less than or equal to 0.50 A.
FAIL if at least one value exceeds 0.50 A.


### TC-003 - Temperature Limit Test

Requirement:
REQ-003

Objective:
Verify that the system temperature does not exceed the maximum allowed value.

Input:
Temperature measurement data from test_run_001.csv

Expected Result:
The temperature shall not exceed 50 °C.

Evaluation:
PASS if all temperature values are less than or equal to 50 °C.
FAIL if at least one value exceeds 50 °C.