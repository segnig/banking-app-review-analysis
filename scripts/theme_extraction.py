import pandas as pd
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import List, Dict, Optional

class ReviewThematicAnalyzer:
    def __init__(self, theme_rules: Optional[Dict[str, List[str]]] = None):
        """Initialize the analyzer with optional custom theme rules"""
        self.nlp = spacy.load("en_core_web_sm")
        self.theme_rules = theme_rules or self._get_default_theme_rules()
        self.tfidf_vectorizer = None
        self.keywords = None
        
    @staticmethod
    def _get_default_theme_rules() -> Dict[str, List[str]]:
        """Optimized theme rules for preprocessed text (lemmatized, lowercase)"""
        return {
            # Core functionality (all lemmatized forms)
            'account_access': [
                'login', 'sign in', 'authenticate', 'biometric', 'face', 'touch',
                'password', 'pin', '2fa', 'two factor', 'verify', 'lock out',
                'session', 'timeout', 'account', 'recover', 'access', 'deny'
            ],
            
            'app_performance': [
                'crash', 'freeze', 'hang', 'lag', 'slow', 'perform', "good",
                "fast", "quick", "response", "smooth", "efficient",
                'bug', 'glitch', 'error', 'respond', 'unstable', 'load',
                'refresh', 'restart', 'close', 'memory', 'storage', "nice", 
                "great", "excellent", "awesome", "perfect", "love", "like"
                
            ],
            
            'transaction': [
                'transfer', 'send', 'money', 'receive', 'payment', 'pay',
                'bill', 'transaction', 'fail', 'decline', 'pending', 'delay',
                'instant', 'process', 'limit', 'amount', 'recipient',
                'schedule', 'recur', 'cancel', 'reverse', 'history'
            ],
            
            # User experience
            'ui_ux': [
                'interface', 'design', 'layout', 'navigate', 'menu',
                'button', 'icon', 'display', 'read', 'intuitive',
                'user friendly', 'complicate', 'confuse', 'modern', 'clutter'
            ],
            
            'security': [
                'secure', 'privacy', 'data', 'protect', 'encrypt',
                'fraud', 'scam', 'phish', 'hack', 'breach', 'leak',
                'permission', 'consent', 'track', 'biometric', 'authenticate'
            ],
            
            # Service aspects
            'customer_support': [
                'support', 'help', 'contact', 'assist', 'service',
                'respond', 'representative', 'wait', 'call', 'resolve',
                'email', 'chat', 'phone', 'escalate', 'complain'
            ],
            
            'notification': [
                'notify', 'alert', 'remind', 'message', 'inbox',
                'email', 'sms', 'push', 'sound', 'vibrate', 'frequent',
                'customize', 'turn off', 'mute', 'promo', 'market'
            ],
            
            # Account management
            'account_management': [
                'profile', 'set', 'prefer', 'personal', 'inform',
                'update', 'change', 'verify', 'document', 'id', 'address',
                'close account', 'delete', 'deactivate', 'reactivate'
            ],
            
            # Financial features
            'financial_tools': [
                'budget', 'spend', 'analyze', 'report', 'insight', 'trend',
                'save', 'goal', 'plan', 'forecast', 'category', 'tag',
                'receipt', 'scan', 'export', 'csv', 'excel', 'pdf'
            ],
            
            # Feature requests
            'feature_request': [
                'suggest', 'recommend', 'wish', 'want', 'need',
                'should', 'could', 'improve', 'enhance', 'add',
                'include', 'miss', 'future', 'roadmap', 'vote', 'request'
            ],
            
            # Integrations
            'integration': [
                'integrate', 'connect', 'link', 'partner', 'external',
                'google pay', 'apple pay', 'paypal', 'venmo', 'zelle',
                'plaid', 'quickbook', 'mint', 'other bank'
            ]
        }
    
    def preprocess(self, text: str) -> str:
        """Clean and lemmatize text"""
        doc = self.nlp(text.lower().strip())  
        tokens = [
            token.lemma_ for token in doc 
            if not token.is_stop 
            and not token.is_punct 
            and not token.is_space
            and len(token) > 2  
        ]
        return " ".join(tokens)
    
    def extract_keywords_tfidf(self, texts: List[str], max_features: int = 100) -> List[str]:
        """Extract keywords using TF-IDF"""
        self.tfidf_vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            max_features=max_features
        )
        tfidf_matrix = self.tfidf_vectorizer.fit_transform(texts)
        self.keywords = self.tfidf_vectorizer.get_feature_names_out()
        return self.keywords
    
    def extract_keywords_spacy(self, text: str) -> List[str]:
        """Extract keywords using spaCy's linguistic features"""
        doc = self.nlp(text)
        return [chunk.text for chunk in doc.noun_chunks] + [
            token.lemma_ for token in doc 
            if token.pos_ in ["NOUN", "ADJ"]
        ]
    
    def assign_theme(self, text: str) -> str:
        """Assign theme based on keyword matching"""
        for theme, keywords in self.theme_rules.items():
            if any(keyword in text for keyword in keywords):
                return theme
        return "Other"
    
    def analyze_reviews(
        self, 
        df: pd.DataFrame, 
        text_column: str = "review_text",
        sentiment_column: str = "sentiment_label",
        score_column: str = "sentiment_score"
    ) -> pd.DataFrame:
        """
        Process dataframe and add thematic analysis columns
        Returns dataframe with added columns: processed_text, theme
        """
        # Preprocess text
        df["processed_text"] = df[text_column].apply(self.preprocess)
        
        # Extract keywords (TF-IDF approach)
        self.extract_keywords_tfidf(df["processed_text"].tolist())
        
        # Assign themes
        df["theme"] = df["processed_text"].apply(self.assign_theme)
        
        return df
    
    def save_results(
        self, 
        df: pd.DataFrame, 
        output_path: str,
        columns: List[str] = [
            "review_text", 
            "sentiment_label", 
            "sentiment_score",
            "theme"
        ]
    ) -> None:
        """Save analysis results to CSV"""
        df[columns].to_csv(output_path, index=False)
    
    def get_theme_distribution(self, df: pd.DataFrame) -> pd.DataFrame:
        """Return percentage distribution of themes"""
        theme_counts = df["theme"].value_counts(normalize=True) * 100
        return theme_counts.reset_index().rename(
            columns={"index": "theme", "theme": "percentage"}
        )