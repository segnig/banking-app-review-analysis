from google_play_scraper import reviews, app, Sort
import pandas as pd
from typing import List, Dict
import os
import time
from tqdm import tqdm
import json


class ScrapeReview:
    def __init__(
        self,
        app_ids: List[str] = [],
        save: bool = False,
        output_dir: str = "../data",
        scrape_metadata: bool = False,
        max_retries: int = 3,
        delay: float = 2.0
    ):
        """
        Initialize the ScrapeReview instance.
        
        Args:
            app_ids: List of app IDs to scrape reviews for
            save: Whether to save the scraped data
            output_dir: Directory to save the data
            scrape_metadata: Whether to scrape app metadata
            max_retries: Maximum number of retries for failed requests
            delay: Delay between requests in seconds
        """
        self.app_ids = app_ids
        self.save = save
        self.output_dir = output_dir
        self.scrape_metadata = scrape_metadata
        self.max_retries = max_retries
        self.delay = delay
        self.metadata = {}
        
        if self.save:
            os.makedirs(self.output_dir, exist_ok=True)
        
        self.data = self._scrape_all_data()
        
        if self.scrape_metadata:
            self.metadata = self._scrape_metadata()
            if self.save:
                self._save_metadata()

    def _scrape_single_app(
        self,
        app_id: str,
        count: int = 5000,
        country: str = "us",
        lang: str = "en",
        sort: Sort = Sort.NEWEST,
    ) -> pd.DataFrame:
        """
        Scrape reviews for a single app.
        
        Args:
            app_id: App ID to scrape
            count: Number of reviews to scrape
            country: Country code for reviews
            lang: Language for reviews
            sort: Sort order for reviews
            
        Returns:
            DataFrame containing scraped reviews
        """
        attempts = 0
        last_exception = None
        
        while attempts < self.max_retries:
            try:
                result, _ = reviews(
                    app_id=app_id,
                    country=country,
                    lang=lang,
                    count=count,
                    sort=sort,
                )
                
                df = pd.DataFrame(result)
                df['app_id'] = app_id
                return df
                
            except Exception as e:
                attempts += 1
                last_exception = e
                print(f"Attempt {attempts} failed for {app_id}: {str(e)}")
                time.sleep(self.delay * attempts)
        
        print(f"Failed to scrape {app_id} after {self.max_retries} attempts. Last error: {str(last_exception)}")
        return pd.DataFrame()

    def _scrape_all_data(
        self,
        count: int = 5000,
        country: str = "us",
        lang: str = "en",
        sort: Sort = Sort.NEWEST,
    ) -> pd.DataFrame:
        """
        Scrape reviews for all app IDs.
        
        Args:
            count: Number of reviews to scrape per app
            country: Country code for reviews
            lang: Language for reviews
            sort: Sort order for reviews
            
        Returns:
            Combined DataFrame of all reviews
        """
        all_data = pd.DataFrame()
        
        if not self.app_ids:
            print("Warning: No app IDs provided")
            return all_data
        
        print(f"Scraping reviews for {len(self.app_ids)} apps...")
        
        for app_id in tqdm(self.app_ids, desc="Scraping apps"):
            df = self._scrape_single_app(
                app_id=app_id,
                count=count,
                country=country,
                lang=lang,
                sort=sort,
            )
            
            if not df.empty:
                all_data = pd.concat([all_data, df], ignore_index=True)
            else:
                print(f"No reviews scraped for {app_id}")
            
            time.sleep(self.delay)
        
        if self.save and not all_data.empty:
            filename = "raw_reviews.csv"
            filepath = os.path.join(self.output_dir, filename)
            
            try:
                all_data[['reviewId', 'userName', 'content', 'score', 'thumbsUpCount', 'at', 'app_id']].to_csv(filepath, index=False)
                print(f"Data saved to {filepath}")
                
                json_filepath = os.path.join(self.output_dir, "raw_reviews.json")
                all_data[['reviewId', 'userName', 'content', 'score', 'thumbsUpCount', 'at', 'app_id']].to_json(json_filepath, orient="records", indent=4)
                print(f"Data also saved as JSON to {json_filepath}")
                
            except Exception as e:
                print(f"Error saving data: {str(e)}")
        
        return all_data

    def _scrape_metadata(self) -> Dict[str, Dict]:
        """
        Scrape metadata for all app IDs.
        
        Returns:
            Dictionary of metadata for each app
        """
        metadata = {}
        
        if not self.app_ids:
            return metadata
            
        print("Scraping app metadata...")
        
        for app_id in tqdm(self.app_ids, desc="Scraping metadata"):
            try:
                result = app(app_id)
                metadata[app_id] = result
                time.sleep(self.delay)
            except Exception as e:
                print(f"Failed to scrape metadata for {app_id}: {str(e)}")
                metadata[app_id] = {"error": str(e)}
        
        return metadata

    def _save_metadata(self):
        """Save the scraped metadata to a file."""
        if not self.metadata:
            return
            
        filename = "metadata.json"
        filepath = os.path.join(self.output_dir, filename)
        
        try:
            with open(filepath, "w") as f:
                json.dump(self.metadata, f, indent=2)
            print(f"Metadata saved to {filepath}")
        except Exception as e:
            print(f"Error saving metadata: {str(e)}")

    def get_reviews(self) -> pd.DataFrame:
        """Get the scraped reviews DataFrame."""
        return self.data[['reviewId', 'userName', 'content', 'score', 'thumbsUpCount', 'at', 'app_id']]

    def get_metadata(self) -> Dict[str, Dict]:
        """Get the scraped metadata dictionary."""
        return self.metadata