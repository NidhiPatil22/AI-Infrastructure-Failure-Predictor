from __future__ import annotations

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

CATEGORICAL_COLUMNS = ['asset_type', 'zone', 'material']


def add_engineered_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['infrastructure_age'] = df['age_years']
    df['maintenance_frequency'] = df['maintenance_count'] / df['age_years'].replace(0, 1)
    df['inspection_gap'] = df['days_since_inspection']
    df['failure_history_score'] = df['previous_failures'] / df['age_years'].replace(0, 1)
    df['maintenance_delay_score'] = df['days_since_maintenance'] / 30.0
    df['environmental_stress'] = (df['annual_rainfall'] / 1000.0) + ((df['average_temperature'] - 20) / 10.0)
    df['load_stress'] = (df['traffic_density'] / 10.0) + (df['average_load'] / 60.0)
    df['overall_condition_score'] = (df['structural_score'] * 0.6) + ((100 - df['corrosion_level']) * 0.4)
    df['overall_condition_score'] = df['overall_condition_score'].clip(0, 100)
    return df


COLUMN_MAPPINGS_50K = {
    'latitude_approx': 'latitude',
    'longitude_approx': 'longitude',
    'age_years_synthetic': 'age_years',
    'structural_score_synthetic': 'structural_score',
    'corrosion_level_synthetic': 'corrosion_level',
    'traffic_density_synthetic': 'traffic_density',
    'annual_rainfall_mm_synthetic': 'annual_rainfall',
    'average_temperature_c_synthetic': 'average_temperature',
    'maintenance_count_synthetic': 'maintenance_count',
    'days_since_maintenance_synthetic': 'days_since_maintenance',
    'days_since_inspection_synthetic': 'days_since_inspection',
    'previous_failures_synthetic': 'previous_failures',
    'usage_intensity_synthetic': 'usage_intensity',
    'material_synthetic': 'material',
    'failure_label_synthetic': 'failure',
    'remaining_useful_life_days_synthetic': 'remaining_useful_life_days',
}

LOCALITY_TO_ZONE = {
    'Wakad': 'West', 'Nigdi': 'North', 'Viman Nagar': 'East', 'Pashan': 'West',
    'Koregaon Park': 'East', 'Bhosari': 'North', 'Kondhwa': 'South', 'Katraj': 'South',
    'Budhwar Peth': 'Central', 'Pune Station': 'Central', 'Dighi': 'North', 'Hinjawadi': 'West',
    'Chinchwad': 'North', 'Shivajinagar': 'Central', 'Mundhwa': 'East', 'Dhanori': 'East',
    'Deccan Gymkhana': 'Central', 'Pune University': 'Central', 'Balewadi': 'West',
    'Anand Nagar': 'South', 'Bavdhan': 'West', 'Warje': 'West', 'Aundh': 'West',
    'Wanowrie': 'South', 'Khadki': 'Central', 'Baner': 'West', 'Hadapsar': 'East',
    'Pimpri': 'North', 'Kharadi': 'East', 'Yerawada': 'East', 'Bibwewadi': 'South',
    'Ambegaon': 'South', 'Sadashiv Peth': 'Central', 'Camp': 'Central', 'Swargate': 'Central',
    'Kothrud': 'West',
}


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """Cleans raw dataset by mapping internal schema columns, removing duplicates,
    and computing row-level physical deterioration features.

    Zero-Data-Leakage Design:
    Missing value imputation and numerical scaling are deferred to scikit-learn
    ColumnTransformer pipelines fitted strictly on training partitions.
    """
    df = df.copy()

    # Map raw 50K columns to canonical model names if present
    rename_dict = {orig: target for orig, target in COLUMN_MAPPINGS_50K.items() if orig in df.columns}
    if rename_dict:
        df = df.rename(columns=rename_dict)

    if 'corrosion_level' in df.columns and df['corrosion_level'].max() <= 1.0:
        df['corrosion_level'] = (df['corrosion_level'] * 100.0).round(1)

    if 'traffic_density' in df.columns and df['traffic_density'].max() <= 1.0:
        df['traffic_density'] = (df['traffic_density'] * 100.0).round(1)

    if 'average_load' not in df.columns and 'usage_intensity' in df.columns:
        df['average_load'] = (df['usage_intensity'] * 100.0).round(1)
    elif 'average_load' not in df.columns:
        df['average_load'] = 60.0

    if 'remaining_useful_life' not in df.columns and 'remaining_useful_life_days' in df.columns:
        df['remaining_useful_life'] = (df['remaining_useful_life_days'] / 365.25).round(2)

    if 'zone' not in df.columns:
        if 'locality' in df.columns:
            df['zone'] = df['locality'].map(lambda loc: LOCALITY_TO_ZONE.get(loc, 'Central'))
        else:
            df['zone'] = 'Central'

    if 'material' not in df.columns:
        df['material'] = 'Bituminous'
    else:
        df['material'] = df['material'].astype(str).str.capitalize()

    if 'asset_type' in df.columns:
        df['asset_type'] = df['asset_type'].replace({
            'road_segment': 'Road Segment',
            'bridge_approach': 'Bridge Approach',
            'culvert_approach': 'Culvert Approach',
        })

    df = df.drop_duplicates().reset_index(drop=True)
    df = add_engineered_features(df)
    return df


def build_preprocessor(X: pd.DataFrame):
    numeric_features = [col for col in X.columns if col not in CATEGORICAL_COLUMNS]
    categorical_transformer = Pipeline([
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore')),
    ])
    numeric_transformer = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler()),
    ])

    preprocessor = ColumnTransformer([
        ('cat', categorical_transformer, CATEGORICAL_COLUMNS),
        ('num', numeric_transformer, numeric_features),
    ])
    return preprocessor
