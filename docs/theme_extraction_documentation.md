## 📊 Thematic Analysis: ReviewThematicAnalyzer Class

This section defines a reusable class `ReviewThematicAnalyzer` that performs **keyword-based thematic analysis** on user reviews using TF-IDF, spaCy, and rule-based keyword matching.

---

### 🔧 Class: `ReviewThematicAnalyzer`

#### Purpose:
To categorize user reviews into actionable **themes** by:
- Preprocessing review text (cleaning + lemmatization)
- Extracting significant keywords using **TF-IDF** or **spaCy**
- Assigning a theme to each review based on predefined keyword rules

---

### 🧱 Key Components

#### `__init__()`
- Initializes:
  - spaCy language model (`en_core_web_sm`)
  - Optional custom theme rules or defaults
  - TF-IDF vectorizer and placeholder for keywords

#### `_get_default_theme_rules()`
- Provides a **dictionary of predefined themes** and their associated keywords.
- Covers 10+ banking-relevant themes including:
  - `account_access`, `app_performance`, `transaction`
  - `ui_ux`, `customer_support`, `security`
  - `notification`, `account_management`
  - `financial_tools`, `feature_request`, `integration`

---

### 🧹 Preprocessing

#### `preprocess(text)`
- Converts text to lowercase
- Lemmatizes words
- Removes stopwords, punctuation, and short tokens
- Returns clean, lemmatized string (ready for analysis)

---

### 🔑 Keyword Extraction

#### `extract_keywords_tfidf(texts)`
- Applies **TF-IDF vectorization** to a list of texts
- Extracts top `n` most important unigrams and bigrams (default = 100)

#### `extract_keywords_spacy(text)`
- Uses spaCy to extract **noun chunks** and **important tokens** (nouns, adjectives)

---

### 🧠 Thematic Labeling

#### `assign_theme(text)`
- For each cleaned review, checks whether any of the rule-based keywords appear
- Returns the **first matching theme**
- Falls back to `"Other"` if no keywords match

---

### 🧪 Review Analysis Pipeline

#### `analyze_reviews(df)`
- Preprocesses reviews in a given DataFrame
- Extracts TF-IDF keywords from all reviews
- Assigns a theme label to each review
- Adds new columns: `processed_text`, `theme`

---

### 💾 Exporting & Summary

#### `save_results(df, output_path)`
- Saves results (with columns like `review_text`, `sentiment_label`, `sentiment_score`, `theme`) to a CSV file

#### `get_theme_distribution(df)`
- Returns a **percentage distribution** of all identified themes (normalized frequency)

---

### 📝 Example Output Columns

| Column Name        | Description                             |
|--------------------|-----------------------------------------|
| `review_text`       | Original user review                   |
| `sentiment_label`   | Sentiment category (positive, negative, neutral) |
| `sentiment_score`   | Model confidence score (0 to 1)         |
| `processed_text`    | Cleaned and lemmatized review text     |
| `theme`             | Assigned thematic category             |

---

### 🛠️ Libraries Used
- `spaCy` – Linguistic processing, lemmatization, POS tagging
- `sklearn.feature_extraction.TfidfVectorizer` – Keyword extraction
- `pandas` – Data manipulation

---

This class allows for flexible, scalable thematic grouping of user reviews to support better understanding of recurring issues and user feedback for digital banking platforms.