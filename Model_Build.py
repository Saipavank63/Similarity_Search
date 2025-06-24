import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
from typing import List
import os

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Create the full path to the CSV file
csv_path = os.path.join(current_dir, 'Final_cleaned_dataset.csv')

df = pd.read_csv(csv_path)

df2 = pd.get_dummies(df, columns=['brand'])


def calculate_similarity(product_attributes, all_attributes):
    scaler = StandardScaler()
    all_attributes_scaled = scaler.fit_transform(all_attributes)
    product_attributes_scaled = scaler.transform(
        product_attributes.reshape(1, -1))
    similarity_scores = cosine_similarity(
        product_attributes_scaled, all_attributes_scaled).flatten()
    return similarity_scores


def find_similar_products(product_id: str, num_similar: int) -> List[str]:
    product = df2[df2['uniq_id'] == product_id].iloc[0]
    product_attributes = product.drop(labels=['uniq_id']).values
    all_attributes = df2.drop(columns=['uniq_id']).values
    similarity_score = calculate_similarity(product_attributes, all_attributes)
    similarity_df = pd.DataFrame({
        'uniq_id': df2['uniq_id'],
        'similarity_score': similarity_score,
        'rating': df2['rating']
    })
    similarity_df = similarity_df.sort_values(
        by=['similarity_score', 'rating'], ascending=[False, False])
    similarity_df = similarity_df[similarity_df['uniq_id'] != product_id]
    similar_product_ids = similarity_df.head(num_similar)['uniq_id'].tolist()

    return similar_product_ids
