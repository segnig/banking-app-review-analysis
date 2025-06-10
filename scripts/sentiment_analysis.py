from dotenv import load_dotenv
import os
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from typing import Dict, Optional
import requests

# Load environment variables
load_dotenv()

class SentimentAnalyzer:
    """
    A sentiment analysis class using DistilBERT model with Hugging Face transformers.
    Handles both local model inference and API-based analysis.
    """
    
    def __init__(self, model_name: str = "distilbert-base-uncased-finetuned-sst-2-english",
                 use_api: bool = False, neutral_threshold: float = 0.2):
        """
        Initialize the sentiment analyzer.
        
        Args:
            model_name: Name of the pre-trained model
            use_api: Whether to use Hugging Face API instead of local model
            neutral_threshold: Threshold for neutral classification (0-0.5)
        """
        self.model_name = model_name
        self.use_api = use_api
        self.neutral_threshold = neutral_threshold
        
        if not use_api:
            self._initialize_local_model()
        else:
            self._validate_api_token()
    
    def _initialize_local_model(self) -> None:
        """Initialize the local model and tokenizer"""
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
            self.classifier = pipeline(
                "sentiment-analysis",
                model=self.model,
                tokenizer=self.tokenizer
            )
        except Exception as e:
            raise RuntimeError(f"Failed to initialize local model: {str(e)}")
    
    def _validate_api_token(self) -> None:
        """Validate the Hugging Face API token"""
        self.hf_token = os.getenv("HF_TOKEN")
        if not self.hf_token:
            raise ValueError("HF_TOKEN not found in environment variables")
        
        self.api_url = f"https://api-inference.huggingface.co/models/{self.model_name}"
        self.headers = {"Authorization": f"Bearer {self.hf_token}"}
    
    def _call_api(self, text: str) -> Dict:
        """Make API call to Hugging Face inference endpoint"""
        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json={"inputs": text}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"API request failed: {str(e)}")
    
    def _classify_sentiment(self, result: Dict) -> Dict[str, float]:
        """
        Classify sentiment based on model output.
        
        Args:
            result: Dictionary containing 'label' and 'score'
            
        Returns:
            Dictionary with positive, negative, and neutral scores
        """
        label = result['label']
        score = result['score']
        positive = None
        
        # Handle potential typo in model output (POSITIVE vs POSITIVE)
        if label.upper() == "POSITIVE" or label.upper() == "POSITIVE":
            label = "POSITIVE"
            positive = score
        else:
            positive = 1 - score
        
        return positive
    
    def analyze(self, text: str) -> Dict[str, float]:
        """
        Analyze sentiment of the input text.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary with sentiment scores
        """
        if not text or not isinstance(text, str):
            raise ValueError("Input text must be a non-empty string")
        
        if self.use_api:
            api_result = self._call_api(text)
            # API returns different format, we take the first result
            result = api_result[0] if isinstance(api_result, list) else api_result
        else:
            result = self.classifier(text)[0]
        
        return self._classify_sentiment(result)
    
    def batch_analyze(self, texts: list) -> list:
        """
        Analyze sentiment for multiple texts.
        
        Args:
            texts: List of texts to analyze
            
        Returns:
            List of sentiment analysis results
        """
        if not isinstance(texts, list):
            raise ValueError("Input must be a list of strings")
            
        return [self.analyze(text) for text in texts]