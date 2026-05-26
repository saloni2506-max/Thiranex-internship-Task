import pandas as pd

# Load dataset
df = pd.read_excel(r"C:\Users\desai\Downloads\Data_Cleaning_Dataset.xlsx")

print("Original Data:")
print(df)

# Remove duplicate rows
df = df.drop_duplicates()

# Fill missing attendance values with average
df['Attendance'] = df['Attendance'].fillna(df['Attendance'].mean())

# Convert Marks column to numeric
# Wrong data becomes NaN
df['Marks'] = pd.to_numeric(df['Marks'], errors='coerce')

# Fill missing/wrong marks with average
df['Marks'] = df['Marks'].fillna(df['Marks'].mean())

print("\nCleaned Data:")
print(df)

# Save cleaned data
df.to_excel("Cleaned_Data.xlsx", index=False)

print("\nData cleaning completed successfully!")