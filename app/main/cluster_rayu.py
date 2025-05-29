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

def cluster_data_rayu(df_rayu_manis):
    customer_data_rayu = df_rayu_manis[['No. Cust', 'Customer', 'No. WA']].copy()
    customer_data_rayu = customer_data_rayu.drop_duplicates()
    customer_data_rayu = customer_data_rayu.dropna()
    customer_data_rayu = customer_data_rayu.drop_duplicates(subset=['No. Cust'])
    
    df_rayu_manis['Tanggal'] = pd.to_datetime(df_rayu_manis['Tanggal'], errors='coerce')

    df_rayu_manis['Recency'] = (max(df_rayu_manis['Tanggal']) - df_rayu_manis['Tanggal']).dt.days

    recency_rayu_manis = df_rayu_manis.groupby('No. Cust')['Recency'].min().reset_index()

    frequency_rayu_manis = df_rayu_manis.groupby('No. Cust')['Qty'].count().reset_index()
    frequency_rayu_manis.columns = ['No. Cust', 'Frequency']

    df_rayu_manis['Total Harga'] = pd.to_numeric(df_rayu_manis['Total Harga'], errors='coerce')
    monetary_rayu_manis = df_rayu_manis.groupby('No. Cust')['Total Harga'].sum().reset_index()
    monetary_rayu_manis.columns = ['No. Cust', 'Monetary']

    rfm_rayu_manis = pd.merge(recency_rayu_manis, frequency_rayu_manis, on='No. Cust', how='inner')
    rfm_rayu_manis = pd.merge(rfm_rayu_manis, monetary_rayu_manis, on='No. Cust', how='inner')
    rfm_rayu_manis.columns = ['No. Cust', 'Recency', 'Frequency', 'Monetary']

    rfm_rayu_manis['Frequency_log'] = np.log1p(rfm_rayu_manis['Frequency'])
    rfm_rayu_manis['Monetary_log'] = np.log1p(rfm_rayu_manis['Monetary'])
    
    rfm_rayu_manis = normalize(rfm_rayu_manis, 'Recency')
    rfm_rayu_manis = normalize(rfm_rayu_manis, 'Frequency_log')
    rfm_rayu_manis = normalize(rfm_rayu_manis, 'Monetary_log')

    rfm_rayu_manis_normalized = rfm_rayu_manis[['No. Cust', 'Recency_normalized', 'Frequency_log_normalized', 'Monetary_log_normalized']].copy()
    rfm_rayu_manis_normalized.columns = ['No. Cust', 'Recency_normalized', 'Frequency_normalized', 'Monetary_normalized']

    k = 2  

    np.random.seed(42)
    centroids_with_cust = rfm_rayu_manis_normalized[['No. Cust', 'Recency_normalized', 'Frequency_normalized', 'Monetary_normalized']].sample(n=k, random_state=42)

    centroids = centroids_with_cust[['Recency_normalized', 'Frequency_normalized', 'Monetary_normalized']].values



    max_iterations = 100 
    features = ['Recency_normalized', 'Frequency_normalized', 'Monetary_normalized']

    for iteration in range(max_iterations):
        data_points = rfm_rayu_manis_normalized[features].values
        rfm_rayu_manis_normalized['Cluster'] = assign_to_centroids(data_points, centroids)

        new_centroids = calculate_new_centroids(rfm_rayu_manis_normalized, 'Cluster', features)
    
        if np.array_equal(new_centroids, centroids):  
            print(f"Convergence reached after {iteration + 1} iterations.")
            break

        centroids = new_centroids  

    rfm_rayu_manis_normalized['Cluster'] = assign_to_centroids(data_points, centroids)

    present_data1 = {
        "clusters": [],
        "centroids": []
    }

    for _, row in rfm_rayu_manis_normalized.iterrows():
        cluster_point = {
            "x": row["Recency_normalized"],
            "y": row["Frequency_normalized"],
            "z": row["Monetary_normalized"],
            "cluster": int(row["Cluster"]) if not pd.isna(row["Cluster"]) else None,
        }

        cluster_point = {k: (v if not pd.isna(v) else None) for k, v in cluster_point.items()}
        
        if not (pd.isna(cluster_point["x"]) or pd.isna(cluster_point["y"]) or pd.isna(cluster_point["z"]) or pd.isna(cluster_point["cluster"])):
            present_data1["clusters"].append(cluster_point)

    for i, centroid in enumerate(centroids):
        centroid_data1 = {
            "x": centroid[0],
            "y": centroid[1],
            "z": centroid[2],
            "label": f"Centroid {i}"
        }

        centroid_data1 = {k: (v if not pd.isna(v) else None) for k, v in centroid_data1.items()}
        
        present_data1["centroids"].append(centroid_data1)

    with open(os.path.join(os.getcwd(), "app", "static", "data", "present_rm.json"), "w") as json_file1:
        json.dump(present_data1, json_file1, indent=4)

    cluster_counts_rm = rfm_rayu_manis_normalized['Cluster'].value_counts().sort_index().to_dict()

    with open(os.path.join(os.getcwd(), "app", "static", "data", "cluster_rm.json"), "w") as json_file3:
        json.dump(cluster_counts_rm, json_file3, indent=4)

        
    merged_data_rm = pd.merge(customer_data_rayu, rfm_rayu_manis_normalized, left_on='No. Cust', right_on='No. Cust', how='inner')

# Convert 'No. WA' to WhatsApp links
    merged_data_rm['No. WA'] = merged_data_rm['No. WA'].astype(str).apply(
    lambda x: 'https://wa.me/62' + x[1:] if x.startswith('0') else 'https://wa.me/' + x
)

# Convert to list of dicts
    merged_data_list_rm = merged_data_rm.to_dict(orient="records")

# Save to JSON
    with open(os.path.join(os.getcwd(), "app", "static", "data", "merged_rm.json"), "w") as json_file5:
        json.dump(merged_data_list_rm, json_file5, indent=4)