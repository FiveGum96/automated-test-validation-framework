import os
from datetime import datetime

import pandas as pd

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    PageBreak,
)


# --------------------------------------------------
# Grenzwerte
# --------------------------------------------------

VOLTAGE_MIN = 11.5
VOLTAGE_MAX = 12.5
CURRENT_MAX = 0.50
TEMPERATURE_MAX = 50.0


# --------------------------------------------------
# Messdaten einlesen
# --------------------------------------------------

input_file = "data/test_run_001.csv"

data = pd.read_csv(input_file)


# --------------------------------------------------
# Grenzwertverletzungen bestimmen
# --------------------------------------------------

voltage_failures = data[
    (data["voltage_v"] < VOLTAGE_MIN)
    | (data["voltage_v"] > VOLTAGE_MAX)
]

current_failures = data[
    data["current_a"] > CURRENT_MAX
]

temperature_failures = data[
    data["temperature_c"] > TEMPERATURE_MAX
]


# --------------------------------------------------
# PASS / FAIL bestimmen
# --------------------------------------------------

voltage_pass = voltage_failures.empty
current_pass = current_failures.empty
temperature_pass = temperature_failures.empty

test_results_boolean = [
    voltage_pass,
    current_pass,
    temperature_pass,
]

passed_tests = sum(test_results_boolean)
failed_tests = len(test_results_boolean) - passed_tests
total_tests = len(test_results_boolean)

overall_pass = all(test_results_boolean)


# --------------------------------------------------
# Messwerte bestimmen
# --------------------------------------------------

max_voltage = data["voltage_v"].max()
max_current = data["current_a"].max()
max_temperature = data["temperature_c"].max()


# --------------------------------------------------
# Verletzungszeiträume bestimmen
# --------------------------------------------------

if voltage_pass:
    voltage_violation = "-"
else:
    voltage_violation = (
        f"{voltage_failures['time_s'].min():.1f} s "
        f"to {voltage_failures['time_s'].max():.1f} s"
    )

if current_pass:
    current_violation = "-"
else:
    current_violation = (
        f"{current_failures['time_s'].min():.1f} s "
        f"to {current_failures['time_s'].max():.1f} s"
    )

if temperature_pass:
    temperature_violation = "-"
else:
    temperature_violation = (
        f"{temperature_failures['time_s'].min():.1f} s "
        f"to {temperature_failures['time_s'].max():.1f} s"
    )


# --------------------------------------------------
# PDF vorbereiten
# --------------------------------------------------

output_file = "reports/test_report.pdf"

document = SimpleDocTemplate(
    output_file,
    pagesize=A4,
    rightMargin=1.5 * cm,
    leftMargin=1.5 * cm,
    topMargin=1.5 * cm,
    bottomMargin=1.5 * cm,
)

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    "CustomTitle",
    parent=styles["Title"],
    fontSize=18,
    leading=22,
    alignment=TA_CENTER,
    spaceAfter=14,
)

section_style = ParagraphStyle(
    "SectionTitle",
    parent=styles["Heading2"],
    fontSize=13,
    leading=16,
    spaceBefore=8,
    spaceAfter=8,
)

normal_style = styles["Normal"]

elements = []


# --------------------------------------------------
# Seite 1 - Titel
# --------------------------------------------------

elements.append(
    Paragraph(
        "Automated Test Validation Report",
        title_style,
    )
)

project_data = [
    ["Project", "Automated Test Validation Framework"],
    ["Test Run", "TR-001"],
    ["Test Date", datetime.now().strftime("%d.%m.%Y")],
    ["Input File", input_file],
    ["Generated With", "Python"],
]

project_table = Table(
    project_data,
    colWidths=[4 * cm, 11 * cm],
)

project_table.setStyle(
    TableStyle(
        [
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.lightgrey),
            ("BACKGROUND", (0, 0), (0, -1), colors.whitesmoke),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]
    )
)

elements.append(project_table)

elements.append(Spacer(1, 0.6 * cm))


# --------------------------------------------------
# Test Summary
# --------------------------------------------------

elements.append(
    Paragraph(
        "Test Summary",
        section_style,
    )
)

overall_text = "PASS" if overall_pass else "FAIL"

summary_data = [
    ["Total Tests", str(total_tests)],
    ["Passed", str(passed_tests)],
    ["Failed", str(failed_tests)],
    ["Overall Result", overall_text],
]

summary_table = Table(
    summary_data,
    colWidths=[5 * cm, 4 * cm],
)

summary_style = [
    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
    ("ALIGN", (1, 0), (1, -1), "CENTER"),
    ("TOPPADDING", (0, 0), (-1, -1), 6),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
]

if overall_pass:
    summary_style.append(
        ("BACKGROUND", (1, 3), (1, 3), colors.lightgreen)
    )
else:
    summary_style.append(
        ("BACKGROUND", (1, 3), (1, 3), colors.lightcoral)
    )

summary_style.append(
    ("FONTNAME", (1, 3), (1, 3), "Helvetica-Bold")
)

summary_table.setStyle(
    TableStyle(summary_style)
)

elements.append(summary_table)

elements.append(Spacer(1, 0.7 * cm))


# --------------------------------------------------
# Testergebnis-Tabelle
# --------------------------------------------------

elements.append(
    Paragraph(
        "Test Results",
        section_style,
    )
)

table_data = [
    [
        "Test Case",
        "Requirement",
        "Measured",
        "Allowed Limit",
        "Violation",
        "Result",
    ],
    [
        "TC-001",
        "REQ-001",
        f"{max_voltage:.2f} V",
        "11.50 - 12.50 V",
        voltage_violation,
        "PASS" if voltage_pass else "FAIL",
    ],
    [
        "TC-002",
        "REQ-002",
        f"{max_current:.2f} A",
        "<= 0.50 A",
        current_violation,
        "PASS" if current_pass else "FAIL",
    ],
    [
        "TC-003",
        "REQ-003",
        f"{max_temperature:.2f} °C",
        "<= 50.00 °C",
        temperature_violation,
        "PASS" if temperature_pass else "FAIL",
    ],
]

result_table = Table(
    table_data,
    colWidths=[
        2.2 * cm,
        2.2 * cm,
        2.4 * cm,
        3.0 * cm,
        3.0 * cm,
        2.0 * cm,
    ],
)

result_table.setStyle(
    TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ]
    )
)

for row in range(1, 4):

    result = table_data[row][5]

    if result == "PASS":
        result_color = colors.lightgreen
    else:
        result_color = colors.lightcoral

    result_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (5, row),
                    (5, row),
                    result_color,
                ),
                (
                    "FONTNAME",
                    (5, row),
                    (5, row),
                    "Helvetica-Bold",
                ),
            ]
        )
    )

elements.append(result_table)

elements.append(Spacer(1, 0.7 * cm))


# --------------------------------------------------
# Measurement Summary
# --------------------------------------------------

elements.append(
    Paragraph(
        "Measurement Summary",
        section_style,
    )
)

measurement_data = [
    ["Maximum Voltage", f"{max_voltage:.2f} V"],
    ["Maximum Current", f"{max_current:.2f} A"],
    ["Maximum Temperature", f"{max_temperature:.2f} °C"],
]

measurement_table = Table(
    measurement_data,
    colWidths=[6 * cm, 4 * cm],
)

measurement_table.setStyle(
    TableStyle(
        [
            ("GRID", (0, 0), (-1, -1), 0.4, colors.lightgrey),
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]
    )
)

elements.append(measurement_table)


# --------------------------------------------------
# Seite 2 - Voltage + Current
# --------------------------------------------------

elements.append(PageBreak())

elements.append(
    Paragraph(
        "Measurement Analysis",
        styles["Heading1"],
    )
)

elements.append(Spacer(1, 0.4 * cm))

elements.append(
    Paragraph(
        "Voltage over Time",
        section_style,
    )
)

voltage_plot = "reports/plots/voltage_plot.png"

if os.path.exists(voltage_plot):
    elements.append(
        Image(
            voltage_plot,
            width=17 * cm,
            height=8.5 * cm,
        )
    )

elements.append(Spacer(1, 0.5 * cm))

elements.append(
    Paragraph(
        "Current over Time",
        section_style,
    )
)

current_plot = "reports/plots/current_plot.png"

if os.path.exists(current_plot):
    elements.append(
        Image(
            current_plot,
            width=17 * cm,
            height=8.5 * cm,
        )
    )


# --------------------------------------------------
# Seite 3 - Temperature
# --------------------------------------------------

elements.append(PageBreak())

elements.append(
    Paragraph(
        "Temperature Analysis",
        styles["Heading1"],
    )
)

elements.append(Spacer(1, 1.0 * cm))

temperature_plot = "reports/plots/temperature_plot.png"

if os.path.exists(temperature_plot):
    elements.append(
        Image(
            temperature_plot,
            width=18 * cm,
            height=9 * cm,
        )
    )

elements.append(Spacer(1, 0.8 * cm))

elements.append(
    Paragraph(
        (
            f"Maximum measured temperature: "
            f"<b>{max_temperature:.2f} °C</b><br/>"
            f"Allowed maximum temperature: "
            f"<b>{TEMPERATURE_MAX:.2f} °C</b><br/>"
            f"Violation period: "
            f"<b>{temperature_violation}</b>"
        ),
        normal_style,
    )
)


# --------------------------------------------------
# PDF erzeugen
# --------------------------------------------------

document.build(elements)

print(
    f"PDF test report created successfully: "
    f"{output_file}"
)