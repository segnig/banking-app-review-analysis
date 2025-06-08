# SentimentAnalyzer

## Overview

The `SentimentAnalyzer` class provides sentiment analysis functionality using Hugging Face’s `distilbert-base-uncased-finetuned-sst-2-english` model. It supports both **local inference** using Transformers and **cloud-based inference** via Hugging Face API.

The class returns sentiment scores which can be mapped to `"positive"`, `"neutral"`, or `"negative"` labels based on defined thresholds.

---

## Features

- ✅ Local inference using Hugging Face Transformers
- ☁️ Optional API-based inference via Hugging Face Inference API
- 📈 Batch sentiment analysis
- 🔒 API token validation
- 🧠 Neutral classification threshold customization
- 🧪 Model inference error handling

---

## Requirements

Install dependencies:

```bash
pip install transformers torch requests python-dotenv
````

Optional `.env` file for API-based usage:

```
HF_TOKEN=your_huggingface_api_token
```

---

## Class: `SentimentAnalyzer`

### `__init__(model_name: str = "distilbert-base-uncased-finetuned-sst-2-english", use_api: bool = False, neutral_threshold: float = 0.2)`

Initializes the sentiment analyzer.

| Parameter           | Type    | Description                                      |
| ------------------- | ------- | ------------------------------------------------ |
| `model_name`        | `str`   | Name of the Hugging Face model to load           |
| `use_api`           | `bool`  | Use Hugging Face API instead of local model      |
| `neutral_threshold` | `float` | Margin (0–0.5) for classifying text as "neutral" |

---

### `analyze(text: str) -> float`

Analyzes the sentiment of a single input string and returns a score between 0 and 1.

| Return Value | Description                                                 |
| ------------ | ----------------------------------------------------------- |
| `float`      | Score > 0.7 = Positive, < 0.3 = Negative, otherwise Neutral |

**Raises**:

* `ValueError`: If input is not a non-empty string
* `RuntimeError`: If model or API call fails

**Example**:

```python
analyzer = SentimentAnalyzer()
score = analyzer.analyze("The app is fantastic!")
print(score)
```

---

### `batch_analyze(texts: List[str]) -> List[float]`

Performs sentiment analysis on a list of texts.

| Parameter | Type        | Description          |
| --------- | ----------- | -------------------- |
| `texts`   | `List[str]` | List of text strings |

| Return Value  | Description              |
| ------------- | ------------------------ |
| `List[float]` | List of sentiment scores |

**Raises**:

* `ValueError`: If input is not a list of strings

**Example**:

```python
texts = ["I love this!", "Worst app ever.", "Not bad"]
results = analyzer.batch_analyze(texts)
```

---

### `HF_TOKEN` for API Mode

To use the Hugging Face API:

1. Sign up at [Hugging Face](https://huggingface.co/)
2. Generate a token under your account settings
3. Create a `.env` file and add:

```env
HF_TOKEN=your_token_here
```

Then:

```python
analyzer = SentimentAnalyzer(use_api=True)
result = analyzer.analyze("Using the API is simple.")
```

---

## Sentiment Labeling Convention

You can convert the float score into labels like so:

```python
def sentiment_label(score):
    if score > 0.7:
        return "positive"
    elif score < 0.3:
        return "negative"
    else:
        return "neutral"
```

---

## Error Handling

* Handles model load failures gracefully
* Validates `.env` file for API mode
* Provides clean exception messages for debugging

---

## Example: CLI/Script Usage

```python
if __name__ == "__main__":
    analyzer = SentimentAnalyzer()
    
    text = "I love this app, but it crashes often."
    print("Single:", analyzer.analyze(text))
    
    batch = [
        "Excellent experience!",
        "Horrible design and slow performance.",
        "It was okay, nothing special."
    ]
    print("Batch:", analyzer.batch_analyze(batch))
    
    # Using API
    try:
        api_analyzer = SentimentAnalyzer(use_api=True)
        print("API result:", api_analyzer.analyze("Great weather today!"))
    except Exception as e:
        print("API failed:", e)
```

---

## File Structure (Recommended)

```
project/
│
├── scripts/
│   └── sentiment_analysis.py
│
├── data/
│   └── cleaned_reviews.csv
│
├── docs/
│   └── sentiment_analyzer.md
│
├── .env
└── requirements.txt
```

---

## License

MIT License or your preferred open-source license.