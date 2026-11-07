import pandas as pd

# Load student dataset
df = pd.read_csv("data/students.csv")

# Display original dataset information
print("Original Dataset:")
print(df.head())

# Check missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Remove duplicate records
df = df.drop_duplicates()

# Handle missing numerical values
numeric_columns = df.select_dtypes(
    include=["number"]
).columns

df[numeric_columns] = df[numeric_columns].fillna(
    df[numeric_columns].mean()
)

# Handle missing categorical values
categorical_columns = df.select_dtypes(
    include=["object"]
).columns

for column in categorical_columns:
    df[column] = df[column].fillna(
        df[column].mode()[0]
    )

# Save processed dataset
df.to_csv(
    "data/processed_students.csv",
    index=False
)

print("\nData preprocessing completed successfully!")
print("Processed dataset saved in data folder.")