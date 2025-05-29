import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import json
import os

def normalize(df, column):
    min_val = df[column].min()
    max_val = df[column].max()
    df[column + '_normalized'] = (df[column] - min_val) / (max_val - min_val)
    return df

def assign_to_centroids(data, centroids):
   distances = np.linalg.norm(data[:, np.newaxis] - centroids, axis=2)
   return np.argmin(distances, axis=1)

def calculate_new_centroids(df, cluster_column, features):
   return df.groupby(cluster_column)[features].mean().values

def cluster_data(df):
    df_cleaned = df[df['No. Cust'] != 'A1001']
    customer_data = df_cleaned[['No. Cust', 'Customer', 'No. WA']].copy()
    customer_data_cleaned = customer_data.drop_duplicates()
    customer_data_cleaned = customer_data.dropna()
    customer_data_cleaned = customer_data_cleaned.drop_duplicates(subset=['No. Cust'])
    
    df_cleaned = df_cleaned.copy()
    df_cleaned.loc[:, 'Tanggal'] = pd.to_datetime(df_cleaned['Tanggal'], errors='coerce', format='%d %B %Y')
    df_cleaned.loc[:, 'Recency'] = max(df_cleaned['Tanggal']) - df_cleaned['Tanggal']
    recency = df_cleaned.groupby('No. Cust')['Recency'].min()
    recency = recency.reset_index()

    recency['Recency'] = pd.to_timedelta(recency['Recency'])

    recency['Recency'] = recency['Recency'].dt.days

    frequency = df_cleaned.groupby('No. Cust')['Qty'].count()
    frequency = frequency.reset_index()
    frequency.columns = ['No. Cust', 'Frequency']


    df_cleaned['Total Harga'] = pd.to_numeric(df_cleaned['Total Harga'], errors='coerce')
    rfm_monetary = df_cleaned.groupby('No. Cust')['Total Harga'].sum().reset_index()
    rfm_monetary.columns = ['No. Cust', 'Monetary']

    rfm = pd.merge(frequency, recency, on='No. Cust', how='inner')
    rfm = pd.merge(rfm, rfm_monetary, on='No. Cust', how='inner')
    rfm.columns = ['No. Cust', 'Recency', 'Frequency', 'Monetary']

    rfm['Recency_log'] = np.log1p(rfm['Recency']) 
    rfm['Monetary_log'] = np.log1p(rfm['Monetary'])

    rfm = normalize(rfm, 'Recency_log')
    rfm = normalize(rfm, 'Frequency')
    rfm = normalize(rfm, 'Monetary_log')

    
    rfm_normalized = rfm[['No. Cust', 'Recency_log_normalized', 'Frequency_normalized', 'Monetary_log_normalized']].copy()
    rfm_normalized.columns = ['No. Cust', 'Recency_normalized', 'Frequency_normalized', 'Monetary_normalized']

    k = 2

    np.random.seed(42)
    centroids_with_cust = rfm_normalized[['No. Cust', 'Recency_normalized', 'Frequency_normalized', 'Monetary_normalized']].sample(n=k, random_state=42)

    centroids = centroids_with_cust[['Recency_normalized', 'Frequency_normalized', 'Monetary_normalized']].values



    max_iterations = 100
    features = ['Recency_normalized', 'Frequency_normalized', 'Monetary_normalized']

    for iteration in range(max_iterations):
        data_points = rfm_normalized[features].values
        rfm_normalized['Cluster'] = assign_to_centroids(data_points, centroids)

        new_centroids = calculate_new_centroids(rfm_normalized, 'Cluster', features)

        if np.array_equal(new_centroids, centroids):
            print(f"Convergence reached after {iteration + 1} iterations.")
            break

        centroids = new_centroids

    rfm_normalized['Cluster'] = assign_to_centroids(data_points, centroids)

    present_data = {
        "clusters": [],
        "centroids": []
    }

    for _, row in rfm_normalized.iterrows():
        cluster_point = {
            "x": row["Recency_normalized"],
            "y": row["Frequency_normalized"],
            "z": row["Monetary_normalized"],
            "cluster": int(row["Cluster"]) if not pd.isna(row["Cluster"]) else None,
        }

        cluster_point = {k: (v if not pd.isna(v) else None) for k, v in cluster_point.items()}
        
        if not (pd.isna(cluster_point["x"]) or pd.isna(cluster_point["y"]) or pd.isna(cluster_point["z"]) or pd.isna(cluster_point["cluster"])):
            present_data["clusters"].append(cluster_point)

    for i, centroid in enumerate(centroids):
        centroid_data = {
            "x": centroid[0],
            "y": centroid[1],
            "z": centroid[2],
            "label": f"Centroid {i}"
        }

        centroid_data = {k: (v if not pd.isna(v) else None) for k, v in centroid_data.items()}
        
        present_data["centroids"].append(centroid_data)

    with open(os.path.join(os.getcwd(), "app", "static", "data", "present.json"), "w") as json_file:
        json.dump(present_data, json_file, indent=4)

    cluster_counts = rfm_normalized['Cluster'].value_counts().sort_index().to_dict()

    with open(os.path.join(os.getcwd(), "app", "static", "data", "cluster.json"), "w") as json_file2:
        json.dump(cluster_counts, json_file2, indent=4)

    # Merge data
    merged_data = pd.merge(customer_data_cleaned, rfm_normalized, left_on='No. Cust', right_on='No. Cust', how='inner')

# Convert 'No. WA' to WhatsApp links
    merged_data['No. WA'] = merged_data['No. WA'].astype(str).apply(
    lambda x: 'https://wa.me/62' + x[1:] if x.startswith('0') else 'https://wa.me/' + x
    )

# Convert to list of dicts
    merged_data_list = merged_data.to_dict(orient="records")

# Save to JSON
    with open(os.path.join(os.getcwd(), "app", "static", "data", "merged.json"), "w") as json_file4:
        json.dump(merged_data_list, json_file4, indent=4)
