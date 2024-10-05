import pandas as pd

def calculate_total_score_per_day(file_path: str, output_file_path: str):
    """
    Reads an Excel file containing article data, computes the total sentiment score per day, 
    and saves the result to a new Excel file.
    
    :param file_path: Path to the input Excel file.
    :param output_file_path: Path to the output Excel file where the result will be saved.
    """
    
    # Load the Excel file
    df = pd.read_excel(file_path)

    # Convert the 'sentiment' column to prediction values (-1 for negative, 0 for neutral, 1 for positive)
    sentiment_map = {'Negative': -1, 'Neutral': 0, 'Positive': 1}
    df['prediction'] = df['Sentiment'].map(sentiment_map)

    # Function to calculate total score for each group (day)
    def calculate_total_score(group):
        num_articles = len(group)
        total_score = (group['prediction'] * group['Score']).sum() / num_articles
        return pd.Series({'total_score': total_score})

    # Apply the calculation to each group (grouped by date)
    result_df = df.groupby('Date').apply(calculate_total_score).reset_index()

    # Save the result to a new Excel file
    result_df.to_excel(output_file_path, index=False)

    print(f"Total score per day has been calculated and saved to {output_file_path}")
    
# Example usage
# calculate_total_score_per_day('path/to/input.xlsx', 'path/to/output.xlsx')

calculate_total_score_per_day('hanmi_titles_1_year_with_sentiments_llm.xlsx', 'hanmi_1_year_total_scores_llm.xlsx')