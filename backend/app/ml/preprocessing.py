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


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df.drop_duplicates().reset_index(drop=True)

    for col in ['age_years', 'traffic_density', 'average_load', 'annual_rainfall', 'average_temperature',
                'maintenance_count', 'days_since_maintenance', 'days_since_inspection', 'structural_score',
                'corrosion_level', 'previous_failures', 'usage_intensity']:
        if col in df.columns:
            q1 = df[col].quantile(0.25)
            q3 = df[col].quantile(0.75)
            iqr = q3 - q1
            lower = q1 - 1.5 * iqr
            upper = q3 + 1.5 * iqr
            df[col] = df[col].clip(lower=lower, upper=upper)

    for col in df.columns:
        if pd.api.types.is_object_dtype(df[col]):
            mode = df[col].mode()
            df[col] = df[col].fillna(mode.iloc[0] if not mode.empty else 'Unknown')
        else:
            df[col] = df[col].fillna(df[col].median())

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
