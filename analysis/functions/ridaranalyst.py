# analysis/utils.py
import pandas as pd

def create_frequency_table(data):
    if not data:
        return None
    df = pd.DataFrame(data)
    result_df = pd.DataFrame(columns=['Question', 'Response', 'Frequency'])
    for col in df.columns:
        if col == 'question':
            continue
        response_counts = df[col].value_counts().reset_index()
        response_counts.columns = ['Response', 'Frequency']
        response_counts['Frequency'] = response_counts.apply(
            lambda row: f"{row['Frequency']} ({(row['Frequency'] / len(df)) * 100:.2f}%)", axis=1
        )
        response_counts['Question'] = df['question'].iloc[0]
        result_df = pd.concat([result_df, response_counts], ignore_index=True)
    return result_df.to_dict(orient='records')


def analyse_question(data):
    if not data:
        return None
    df = pd.DataFrame(data)
    result_df = pd.DataFrame(columns=['Question', 'Response'])
    for index, row in df.iterrows():
        question = row['question']
        for col in df.columns:
            if col == 'question':
                continue
            response = row[col]
            result_df = pd.concat([result_df, pd.DataFrame({'Question': [question], 'Response': [response]})], ignore_index=True)
    return result_df.to_dict(orient='records')
