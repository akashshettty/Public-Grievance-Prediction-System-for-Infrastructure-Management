from loader import load_grievance_data, save_processed_data
from preprocess import preprocess_grievance_data


def main() -> None:
    raw_df = load_grievance_data("grievances_sample.csv")
    clean_df = preprocess_grievance_data(raw_df)
    output_path = save_processed_data(clean_df, "grievances_cleaned.csv")

    print("Raw shape:", raw_df.shape)
    print("Clean shape:", clean_df.shape)
    print("Saved cleaned data to:", output_path)


if __name__ == "__main__":
    main()
