import psycopg2
from psycopg2 import sql
from psycopg2.extras import DictCursor
from typing import Optional, Dict, List

class CleanedDataToDatabase:
    def __init__(self, dbname: str, username: str, password: str, host: str = "localhost", port: str = "5432"):
        self.connection_params = {
            'dbname': dbname,
            'user': username,
            'password': password,
            'host': host,
            'port': port
        }
        self.connection = None
        self.cursor = None

    def _create_connection(self) -> None:
        """Establish database connection with error handling"""
        try:
            self.connection = psycopg2.connect(**self.connection_params)
            self.connection.autocommit = False  # Use transactions explicitly
            self.cursor = self.connection.cursor(cursor_factory=DictCursor)
            print("Successfully connected to database")
        except psycopg2.Error as e:
            raise ConnectionError(f"Database connection failed: {e}")

    def _close_connection(self) -> None:
        """Safely close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Connection closed")

    def create_reviews_table(self) -> None:
        """Create the Reviews table if it doesn't exist"""
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS Reviews (
            review_id VARCHAR(100) PRIMARY KEY,
            app_id VARCHAR(100) NOT NULL,
            app_name VARCHAR(100) NOT NULL,
            user_name VARCHAR(50),
            review TEXT,
            rating NUMERIC(2,1) NOT NULL CHECK (rating >= 1 AND rating <= 5),
            thumbs_up_count INTEGER DEFAULT 0 CHECK (thumbs_up_count >= 0),
            date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        CREATE INDEX IF NOT EXISTS idx_reviews_app_id ON Reviews(app_id);
        """
        try:
            self._create_connection()
            self.cursor.execute(create_table_sql)
            self.connection.commit()
            print("Reviews table created successfully")
        except psycopg2.Error as e:
            self.connection.rollback()
            raise RuntimeError(f"Failed to create table: {e}")
        finally:
            self._close_connection()

    def insert_review(self, review_data: Dict) -> bool:
        """Insert a single review record"""
        insert_sql = """
        INSERT INTO Reviews (review_id, app_id, app_name, user_name, review, rating, thumbs_up_count)
        VALUES (%(review_id)s, %(app_id)s, %(app_name)s, %(user_name)s, %(review)s, %(rating)s, %(thumbs_up_count)s)
        ON CONFLICT (review_id) DO NOTHING;
        """
        try:
            self._create_connection()
            self.cursor.execute(insert_sql, review_data)
            self.connection.commit()
            return self.cursor.rowcount > 0
        except psycopg2.Error as e:
            self.connection.rollback()
            raise RuntimeError(f"Insert failed: {e}")
        finally:
            self._close_connection()

    def batch_insert_reviews(self, reviews: List[Dict]) -> int:
        """Insert multiple reviews efficiently"""
        insert_sql = """
        INSERT INTO Reviews (review_id, app_id, app_name, user_name, review, rating, thumbs_up_count)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (review_id) DO NOTHING;
        """
        try:
            self._create_connection()
            records = [
                (r['review_id'], r['app_id'], r['app_name'], 
                 r.get('user_name'), r.get('review'), r['rating'], 
                 r.get('thumbs_up_count', 0))
                for r in reviews
            ]
            self.cursor.executemany(insert_sql, records)
            self.connection.commit()
            return self.cursor.rowcount
        except psycopg2.Error as e:
            self.connection.rollback()
            raise RuntimeError(f"Batch insert failed: {e}")
        finally:
            self._close_connection()
            
    def insert_banks(self, banks_data: List[Dict]) -> int:
        """Insert multiple banks"""
        insert_sql = """
        INSERT INTO banks (bank_id, bank_name, website_url, app_store_id)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (bank_id) DO NOTHING;
        """
        try:
            self._create_connection()
            data = [
                (bank['bank_id'], bank['bank_name'], 
                bank['website_url'], bank['app_store_id'])
                for bank in banks_data
            ]
            self.cursor.executemany(insert_sql, data)
            self.connection.commit()
            print(f"Inserted/updated {self.cursor.rowcount} banks")
            return self.cursor.rowcount
        except Exception as e:
            self.connection.rollback()
            raise RuntimeError(f"Bank insert failed: {str(e)}")
        finally:
            self._close_connection()