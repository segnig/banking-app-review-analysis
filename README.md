# Google Play Store Reviews Preprocessor

![Python](https://img.shields.io/badge/python-3.7%2B-blue)
![Pandas](https://img.shields.io/badge/pandas-1.0%2B-brightgreen)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A robust data preprocessing pipeline for cleaning and transforming raw Google Play Store reviews using the `DataPreprocessor` class.

## Features

- 🧹 **Automatic Data Cleaning**: Handles missing values and duplicates
- 📅 **Date Standardization**: Converts timestamps to datetime objects
- 🔤 **Text Filtering**: Identifies English content via ASCII detection
- 📛 **Column Standardization**: Consistent naming conventions
- 📦 **Metadata Extraction**: Derives app names from package IDs
- 💾 **Configurable Output**: Flexible saving options

## Installation

1. Clone the repository:
```bash
git clone https://github.com/segnig/playstore-reviews-preprocessor.git
cd playstore-reviews-preprocessor
```

2. Install dependencies:
```bash
pip install pandas numpy
```

## Usage

### Basic Implementation
```python
from preprocessor import DataPreprocessor

# Initialize with default settings
processor = DataPreprocessor(
    input_file="raw_reviews.csv",
    output_file="clean_reviews.csv"
)

# Access cleaned data
clean_data = processor.cleaned_data
```

### Advanced Configuration
```python
processor = DataPreprocessor(
    input_file="raw_data.csv",
    output_file="processed/clean_data.csv",
    save=True,            # Auto-save results
    verbose=True          # Show progress messages
)
```

## Methodology

### Data Processing Pipeline
1. **Data Loading**  
   - Validates input file existence
   - Handles various CSV formats with error checking

2. **Initial Cleaning**  
   ```python
   data_frame.dropna(inplace=True)       # Remove empty entries
   data_frame.drop_duplicates(inplace=True)  # Eliminate duplicates
   ```

3. **Column Standardization**  
   Standardizes column names using mapping:
   ```python
   {
       'userName': 'user_name',
       'content': 'review',
       'score': 'rating',
       'thumbsUpCount': 'thumbs_up_count',
       'at': 'date'
   }
   ```

4. **English Content Filtering**  
   Uses ASCII character detection:
   ```python
   data_frame['review'].str.contains(r'^[\x00-\x7F]+$', na=False)
   ```

5. **App Name Extraction**  
   Derives names from package IDs:
   ```python
   data_frame['app_id'].apply(lambda x: x.split('.')[-2])
   ```

## Output Specification

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| user_name | str | Reviewer display name | "JohnDoe123" |
| review | str | Review text content | "Great app!" |
| rating | int | Star rating (1-5) | 5 |
| thumbs_up_count | int | Helpful votes count | 24 |
| date | datetime | Review timestamp | 2023-05-15 14:30:00 |
| app_id | str | Full package ID | "com.example.app" |
| app_name | str | Extracted app name | "app" |

## Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Segni Girma - your.segnigirma11@gmail.com  
Project Link: [https://github.com/segnig/playstore-reviews-preprocessor](https://github.com/segnig/playstore-reviews-preprocessor)
```

Key features of this README:
1. **Modern Formatting**: Uses badges and clean headers
2. **Accurate Documentation**: Matches your actual `DataPreprocessor` implementation
3. **Visual Examples**: Includes code blocks and tables
4. **Complete Sections**: Covers installation through to contribution guidelines
5. **Consistent Terminology**: Uses your exact method and variable names