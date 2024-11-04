import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


# data
df = pd.read_excel(r"C:\Users\aswin\OneDrive\Desktop\medication_dosage_data.xlsx")

# Display
print(df)


xtrain = df['Medication Dosage'].values

# logit
for i in range(len(df)):
    totalPatients = df.loc[i, 'Total Patients']
    curedPatients = df.loc[i, 'Cured']
    pcure = curedPatients / totalPatients
    odds = pcure / (1 - pcure)
    logit = np.log(odds)

    df.loc[i, 'logits'] = logit

# Display logit
print(df)


numerator = 0
denominator = 0
x_mean = np.mean(df['Medication Dosage'])
y_mean = np.mean(df['logits'])

# slope
for index, row in df.iterrows():
    xi = row['Medication Dosage']
    yi = row['logits']
    numerator += (xi - x_mean) * (yi - y_mean)
    denominator += (xi - x_mean) ** 2

b1 = numerator / denominator
b0 = y_mean - (b1 * x_mean)

# Print slope
print(b1, b0)


for i in range(len(df)):
    xi = df.loc[i, 'Medication Dosage']
    y = sigmoid(b1 * xi + b0)

    print("prob", y)
    df.loc[i, 'predicted_probability'] = y

    if y > 0.5:
        print("cured")
    else:
        print("Not cured")

# Plotting
plt.figure(figsize=(10, 6))

plt.scatter(df['Medication Dosage'], df['predicted_probability'], color='blue', label='Predicted Probability')

plt.scatter(df['Medication Dosage'], df['Cured'] / df['Total Patients'], color='red', label='Actual Cure Rate',
            alpha=0.5)

x_values = np.linspace(df['Medication Dosage'].min(), df['Medication Dosage'].max(), 100)
y_values = sigmoid(b0 + b1 * x_values)
plt.plot(x_values, y_values, color='green', label='Decision Boundary (p=0.5)')

plt.xlabel('Medication Dosage')
plt.ylabel('Probability of Cure')
plt.title('Logistic Regression Decision Boundary')

plt.axhline(0.5, color='gray', linestyle='--')

plt.legend()
plt.grid(True)

# Display
plt.show()
