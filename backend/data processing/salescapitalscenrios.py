import matplotlib.pyplot as plt

# Define all 10 scenarios with names and values
scenarios = {
    "Scenario 1: Steady Growth, Then Plateau": [1.2, 1.5, 1.9, 2.3, 2.7, 2.7, 2.7, 2.7, 2.7, 2.7],
    "Scenario 2: Continuous Decline": [1.35, 1.2, 1.05, 0.9, 0.75, 0.65, 0.55, 0.45, 0.35, 0.3],
    "Scenario 3: Boom Then Bust": [1.3, 1.6, 2.0, 2.4, 2.5, 2.5, 2.5, 2.1, 1.7, 1.3],
    "Scenario 4: Delayed Growth": [1.0, 1.0, 1.2, 1.5, 1.9, 2.2, 2.4, 2.6, 2.7, 2.8],
    "Scenario 5: Reinvestment Dip Then Growth": [1.3, 1.5, 1.6, 1.3, 1.0, 1.8, 2.2, 2.4, 2.5, 2.6],
    "Scenario 6: Exponential Growth": [1.0, 1.2, 1.5, 1.9, 2.4, 3.0, 3.7, 4.5, 5.4, 6.4],
    "Scenario 7: Step-Change Improvement": [1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0],
    "Scenario 8: Low and Flat": [1.0] * 10,
    "Scenario 9: Mid-Growth, Then Maturity": [1.1, 1.3, 1.6, 1.9, 2.1, 2.2, 2.2, 2.2, 2.2, 2.2],
    "Scenario 10: W-Shaped Recovery": [1.4, 1.2, 1.0, 1.5, 2.0, 2.2, 2.1, 1.8, 2.0, 2.3]
}

# Plot each scenario in separate charts (useful when memory issues arise)
for name, values in scenarios.items():
    plt.figure(figsize=(8, 4))
    plt.plot(range(1, 11), values, marker='o', linestyle='-', color='teal')
    plt.title(name)
    plt.xlabel("Year")
    plt.ylabel("Sales/Capital")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
