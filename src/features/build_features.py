import pandas as pd
import numpy as np


def impute_rare_titles(df: pd.DataFrame, tresh: int = 100) -> pd.DataFrame:
    """Substitutes rare titles with closest ones by Elo
    Parameters:
    thresh: threshold for title to be considered as rare
    """

    for color in ['White', 'Black']:
        title_column_name = f'{color}Title'
        elo_column_name = f'{color}Elo'

        titles_dict = df[title_column_name].value_counts().to_dict()
        to_impute_titles = [
            title for title in titles_dict if titles_dict[title] < tresh]
        base_titles = [
            title for title in titles_dict if titles_dict[title] >= tresh]

        title_averages = df.groupby(title_column_name)[elo_column_name].mean()
        to_impute_averages = title_averages[to_impute_titles]
        base_title_averages = title_averages[base_titles]

        imputation_dict = {}

        for title in to_impute_titles:
            title_avg = to_impute_averages[title]
            imputation_dict[title] = min(
                base_title_averages.items(), key=lambda x: abs(x[1]-title_avg))[0]

        imputation_dict.update({k: k for k in base_titles})

        df[title_column_name] = df[title_column_name].map(imputation_dict)

    return df


def make_otb_feature(df: pd.DataFrame) -> pd.DataFrame:
    """Make a categorical variable: Online vs Otb game"""
    domains = ['.com', '.org']
    online_sites = [item for item in df['Site'].unique() if np.array(
        [domain in item for domain in domains]).any()]

    df['Otb'] = df['Site'].apply(
        lambda site: 'Online' if site in online_sites else 'OTB')
    return df
