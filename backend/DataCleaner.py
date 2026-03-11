import pandas as pd
import re

def clean_dataset(input_path, output_path):
    # Load the dataset
    try:
        df = pd.read_csv(input_path)
    except FileNotFoundError:
        print(f"Error: File not found at {input_path}")
        return

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Handle missing values (example: drop rows with missing values)
    df = df.dropna()

    # Standardize text columns
    for column in df.select_dtypes(include=['object']).columns:
        df[column] = df[column].str.lower().str.strip()
        df[column] = df[column].apply(lambda x: re.sub(r'[^a-zA-Z0-9\s]', '', x) if isinstance(x, str) else x)

    # Save the cleaned dataset
    df.to_csv(output_path, index=False)
    print(f"Cleaned dataset saved to {output_path}")

if __name__ == "__main__":
    input_file = "../data/DataSet.csv"
    output_file = "../data/Cleaned_DataSet.csv"
    clean_dataset(input_file, output_file)