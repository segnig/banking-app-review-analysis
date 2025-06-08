import pandas as pd
from typing import List, Optional
import os
from datetime import datetime

class DataPreprocessor:
    """
    Enhanced class to preprocess and clean scraped Google Play Store review data.
    
    Args:
        input_file (str): Path to input CSV file
        output_file (str): Path to save cleaned data
        save (bool): Whether to save cleaned data (default: True)
        verbose (bool): Whether to print progress messages (default: True)
    """
    
    def __init__(
        self, 
        input_file: str, 
        output_file: str, 
        save: bool = True,
        verbose: bool = True
    ):
        self.input_file = input_file
        self.output_file = output_file
        self.save = save
        self.verbose = verbose
        
        # Validate input file exists
        self._validate_input_file()
        
        # Load and process data
        self.data = self._load_data()
        self.cleaned_data = self._preprocess()
        
        # Validate output directory if saving
        if self.save:
            self._validate_output_dir()
    
    def _print(self, message: str) -> None:
        """Helper method for conditional printing"""
        if self.verbose:
            print(message)
    
    def _validate_input_file(self) -> None:
        """Check if input file exists before processing"""
        if not os.path.exists(self.input_file):
            raise FileNotFoundError(f"Input file not found: {self.input_file}")
    
    def _validate_output_dir(self) -> None:
        """Ensure output directory exists"""
        output_dir = os.path.dirname(self.output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            self._print(f"Created output directory: {output_dir}")
    
    def _load_data(self) -> pd.DataFrame:
        """
        Load data from CSV file with robust error handling.
        
        Returns:
            pd.DataFrame: Loaded data or empty DataFrame on error
        """
        try:
            self._print(f"Loading data from {self.input_file}")
            data = pd.read_csv(self.input_file)
            
            if data.empty:
                self._print("Warning: Loaded an empty DataFrame")
            else:
                self._print(f"Successfully loaded {len(data)} records")
                
            return data
            
        except pd.errors.EmptyDataError:
            self._print(f"Warning: File {self.input_file} is empty")
            return pd.DataFrame()
        except Exception as e:
            self._print(f"Error loading data: {str(e)}")
            return pd.DataFrame()
    
    def _preprocess(self) -> pd.DataFrame:
        """
        Clean and transform the data with comprehensive preprocessing.
        
        Returns:
            pd.DataFrame: Cleaned and processed data
        """
        if self.data.empty:
            self._print("Warning: No data to preprocess")
            return pd.DataFrame()
            
        try:
            data_frame = self.data.copy()
            self._print("Starting data preprocessing")
            
            # Record initial stats
            initial_count = len(data_frame)
            
            # 1. Handle missing values
            data_frame.dropna(inplace=True)
            missing_dropped = initial_count - len(data_frame)
            self._print(f"Dropped {missing_dropped} records with missing values")
            
            # 2. Remove duplicates
            data_frame.drop_duplicates(inplace=True)
            duplicates_dropped = initial_count - missing_dropped - len(data_frame)
            self._print(f"Dropped {duplicates_dropped} duplicate records")
            
            # 3. Normalize dates with better format handling
            data_frame['at'] = pd.to_datetime(
                data_frame['at'], 
                errors='coerce',
                format='mixed'  # Handles multiple date formats
            )
            
            # Remove records with invalid dates
            invalid_dates = data_frame['at'].isna().sum()
            if invalid_dates > 0:
                data_frame = data_frame[data_frame['at'].notna()]
                self._print(f"Dropped {invalid_dates} records with invalid dates")
            
            # 4. Standardize column names (only existing columns)
            column_map = {
                'userName': 'user_name',
                'content': 'review',
                'score': 'rating',
                'thumbsUpCount': 'thumbs_up_count',
                'at': 'date',
                'app_id': 'app_id',
                'replyContent': 'developer_reply',
                'repliedAt': 'developer_reply_date'
            }
            
            # Only rename columns that exist
            data_frame.rename(
                columns={k: v for k, v in column_map.items() if k in data_frame.columns},
                inplace=True
            )
            
            # 5. Extract and clean app names
            data_frame['app_name'] = data_frame['app_id'].apply(
                lambda x: x.split('.')[-2].title() if isinstance(x, str) else 'Unknown'
            )
            
            # 6. Clean text data
            if 'review' in data_frame.columns:
                data_frame['review'] = (
                    data_frame['review']
                    .str.strip()
                    .replace(r'\s+', ' ', regex=True)
                )
            
            # 7. Select final features (only those available)
            possible_features = [
                'app_id', 'app_name', 'user_name', 'review', 'rating',
                'thumbs_up_count', 'date', 'developer_reply', 'developer_reply_date'
            ]
            features = [f for f in possible_features if f in data_frame.columns]
            
            # Save if requested
            if self.save:
                try:
                    data_frame[features].to_csv(self.output_file, index=False)
                    self._print(f"Successfully saved {len(data_frame)} records to {self.output_file}")
                except Exception as e:
                    self._print(f"Failed to save data: {str(e)}")
            
            return data_frame[features]
            
        except Exception as e:
            self._print(f"Error during preprocessing: {str(e)}")
            return pd.DataFrame()
    
    def get_cleaned_data(self) -> pd.DataFrame:
        """
        Get the cleaned and processed data.
        
        Returns:
            pd.DataFrame: The cleaned data
        """
        return self.cleaned_data
    
    
    def _filter_english_content(self, data_frame: pd.DataFrame) -> pd.DataFrame:
        """
        Filter reviews to keep only those with English content.
        
        Args:
            data_frame (pd.DataFrame): DataFrame containing reviews
        
        Returns:
            pd.DataFrame: Filtered DataFrame with only English reviews
        """
        if 'review' not in data_frame.columns:
            return data_frame
        
        # Simple heuristic to filter English content
        is_english = data_frame['review'].str.contains(r'^[\x00-\x7F]+$', na=False)
        filtered_data = data_frame[is_english]
        
        self._print(f"Filtered down to {len(filtered_data)} English reviews")
        return filtered_data