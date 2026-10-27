from __future__ import annotations

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score

from app.ml.preprocessing import clean_dataset


from sklearn.impute import SimpleImputer


def train_clustering(df: pd.DataFrame):
    df = clean_dataset(df)
    cluster_features = ['age_years', 'traffic_density', 'average_load', 'structural_score', 'maintenance_count', 'days_since_maintenance', 'previous_failures', 'usage_intensity']
    X_raw = df[cluster_features]
    imputer = SimpleImputer(strategy='median')
    X = imputer.fit_transform(X_raw)

    df_sample = df.iloc[:5000].copy() if len(df) > 5000 else df
    X_sample = X[:5000] if len(X) > 5000 else X
    silhouettes = []
    eval_sample_size = min(2000, len(X_sample))
    for k in range(2, 6):
        model = KMeans(n_clusters=k, random_state=42, n_init=3)
        labels_sub = model.fit_predict(X_sample)
        score = silhouette_score(X_sample, labels_sub, sample_size=eval_sample_size, random_state=42)
        silhouettes.append((k, score))

    best_k = max(silhouettes, key=lambda item: item[1])[0]
    best_k = min(max(best_k, 3), 5)
    final_model = KMeans(n_clusters=best_k, random_state=42, n_init=5)
    labels = final_model.fit_predict(X_sample)
    pca = PCA(n_components=2, random_state=42)
    pca_result = pca.fit_transform(X_sample)

    cluster_summary = []
    for cluster in range(best_k):
        mask = labels == cluster
        values = df_sample.loc[mask, cluster_features]
        cluster_summary.append({
            'cluster_id': int(cluster),
            'size': int(mask.sum()),
            'average_age_years': round(float(values['age_years'].mean()), 2),
            'average_traffic_density': round(float(values['traffic_density'].mean()), 2),
            'average_structural_score': round(float(values['structural_score'].mean()), 2),
            'average_days_since_maintenance': round(float(values['days_since_maintenance'].mean()), 2),
            'average_previous_failures': round(float(values['previous_failures'].mean()), 2),
            'average_usage_intensity': round(float(values['usage_intensity'].mean()), 2),
        })

    description_map = {0: 'Healthy Infrastructure', 1: 'Moderate Risk Infrastructure', 2: 'Critical Infrastructure'}
    for item in cluster_summary:
        item['description'] = description_map.get(item['cluster_id'], 'Managed Asset Group')

    return {
        'model': final_model,
        'pca': pca,
        'pca_points': pca_result[:1000].tolist(),
        'labels': labels[:1000].tolist(),
        'selected_k': best_k,
        'silhouette_values': [{'k': k, 'silhouette_score': round(float(s), 4)} for k, s in silhouettes],
        'cluster_summary': cluster_summary,
    }
