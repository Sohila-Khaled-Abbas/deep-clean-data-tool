import pandas as pd
import numpy as np
from scipy import stats
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
from sklearn.impute import SimpleImputer

class DeepClean:
    def __init__(self, df):
        """Initialize the cleaning tool with a copy of the dataframe."""
        self.df = df.copy()
        self.report = {}

    def remove_duplicates(self):
        """Removes exact duplicate rows."""
        before = len(self.df)
        self.df = self.df.drop_duplicates()
        self.report['duplicates_removed'] = before - len(self.df)
        return self.df

    def process_dates(self, date_columns=None):
        """Extracts features from timestamp columns."""
        cols = date_columns if date_columns else self.df.select_dtypes(include=['datetime64', 'object']).columns
        processed_count = 0
        
        for col in cols:
            try:
                temp_dates = pd.to_datetime(self.df[col], errors='coerce')
                if temp_dates.notnull().any():
                    self.df[col] = temp_dates
                    self.df[f'{col}_year'] = self.df[col].dt.year
                    self.df[f'{col}_month'] = self.df[col].dt.month
                    self.df[f'{col}_day'] = self.df[col].dt.day
                    self.df[f'{col}_dayofweek'] = self.df[col].dt.dayofweek
                    processed_count += 1
            except Exception:
                continue
                
        self.report['date_columns_processed'] = processed_count
        return self.df

    def handle_missing_values(self, strategy='mean', columns=None):
        """Imputes missing values in numeric columns."""
        cols_to_fix = columns if columns else self.df.select_dtypes(include=[np.number]).columns
        
        if len(cols_to_fix) == 0:
            self.report['missing_values_filled'] = 0
            return self.df
            
        missing_before = self.df[cols_to_fix].isnull().sum().sum()
        
        try:
            imputer = SimpleImputer(strategy=strategy, keep_empty_features=True)
            self.df[cols_to_fix] = imputer.fit_transform(self.df[cols_to_fix])
        except TypeError:
            imputer = SimpleImputer(strategy=strategy)
            valid_cols = [c for c in cols_to_fix if self.df[c].notnull().any()]
            if valid_cols:
                self.df[valid_cols] = imputer.fit_transform(self.df[valid_cols])
        
        self.report['missing_values_filled'] = int(missing_before)
        return self.df

    def handle_outliers(self, threshold=3.0):
        """Clips outliers using Z-score statistics."""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        outliers_count = 0
        
        for col in numeric_cols:
            if self.df[col].std() == 0 or self.df[col].isnull().all(): continue
            z_scores = np.abs(stats.zscore(self.df[col].dropna()))
            outlier_mask = z_scores > threshold
            outliers_count += outlier_mask.sum()
            
            upper = self.df[col].mean() + threshold * self.df[col].std()
            lower = self.df[col].mean() - threshold * self.df[col].std()
            self.df[col] = self.df[col].clip(lower=lower, upper=upper)
            
        self.report['outliers_clipped'] = int(outliers_count)
        return self.df

    def encode_categorical(self):
        """Converts object columns to numeric labels."""
        obj_cols = self.df.select_dtypes(include=['object']).columns
        le = LabelEncoder()
        
        for col in obj_cols:
            self.df[col] = le.fit_transform(self.df[col].astype(str))
            
        self.report['encoded_columns_count'] = len(obj_cols)
        return self.df

    def normalize_data(self, method='standard'):
        """Scales numeric features."""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) == 0:
            self.report['normalization_method'] = 'none'
            return self.df
            
        scaler = StandardScaler() if method == 'standard' else MinMaxScaler()
        self.df[numeric_cols] = scaler.fit_transform(self.df[numeric_cols])
        self.report['normalization_method'] = method
        return self.df

    def clean(self):
        """Runs the full pipeline in sequence."""
        self.remove_duplicates()
        self.process_dates()
        self.handle_missing_values()
        self.handle_outliers()
        self.encode_categorical()
        self.normalize_data()
        return self.df

    def get_summary(self):
        return self.report
