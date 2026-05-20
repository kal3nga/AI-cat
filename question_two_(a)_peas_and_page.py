
"""
DNA Identification System
"""


print("DNA MATCHING SYSTEM")


peas = {
    "Performance": [
        "99.99% accuracy",
        "Under 24 hours per sample",
        "Low false positive rate"
    ],
    "Environment": [
        "DNA lab",
        "Reference database",
        "Cold storage"
    ],
    "Actuators": [
        "DNA sequencer",
        "Robot handler",
        "Database query"
    ],
    "Sensors": [
        "DNA reader",
        "Barcode scanner",
        "Temperature sensors"
    ]
}

page = {
    "Percepts": [
        "Raw DNA data",
        "Sample IDs",
        "Reference profiles"
    ],
    "Actions": [
        "Start sequencing",
        "Compare with database",
        "Generate report"
    ],
    "Goals": [
        "95% identification rate",
        "Zero false matches",
        "24 hour turnaround"
    ],
    "Environment": [
        "Victim samples",
        "Family references",
        "Lab facilities"
    ]
}

print("\nPEAS:")
for key, values in peas.items():
    print(f"\n{key}:")
    for v in values:
        print(f"  • {v}")

print("\n\nPAGE:")
for key, values in page.items():
    print(f"\n{key}:")
    for v in values:
        print(f"  • {v}")
