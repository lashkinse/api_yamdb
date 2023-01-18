import sqlite3
from datetime import datetime

import pandas as pandas
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Imports the data from the CSV files into the database"
    CSV_ROOT = "./static/data"
    DATABASE_PATH = "./db.sqlite3"

    USERS_TABLE = "users_user"
    TITLE_TABLE = "reviews_title"
    REVIEW_TABLE = "reviews_review"
    COMMENT_TABLE = "reviews_comment"
    CSV_TO_TABLE_MAP = (
        ("users.csv", USERS_TABLE),
        ("category.csv", "reviews_category"),
        ("genre.csv", "reviews_genre"),
        ("titles.csv", TITLE_TABLE),
        ("genre_title.csv", "reviews_genretitle"),
        ("comments.csv", COMMENT_TABLE),
        ("review.csv", "reviews_review"),
    )

    def fix_dataframe(self, df, table_name):
        """Fixes the dataframe so that it can be used in the database"""
        if table_name == self.USERS_TABLE:
            df = df.fillna("")
            df.insert(len(df.columns), "password", "")
            df.insert(len(df.columns), "is_superuser", 0)
            df.insert(len(df.columns), "is_staff", 0)
            df.insert(len(df.columns), "is_active", 1)
            df.insert(len(df.columns), "date_joined", datetime.now())
        if table_name == self.TITLE_TABLE:
            df.rename(columns={"category": "category_id"}, inplace=True)
        if table_name == self.REVIEW_TABLE or table_name == self.COMMENT_TABLE:
            df.rename(columns={"author": "author_id"}, inplace=True)
        return df

    def import_csv(self, csv_file, table_name):
        """Imports the data from the CSV file into the database"""
        try:
            conn = sqlite3.connect(self.DATABASE_PATH)
            df = pandas.read_csv(
                csv_file,
                encoding="utf-8",
            )
            df = self.fix_dataframe(df, table_name)
            df.to_sql(table_name, conn, if_exists="append", index=False)
            conn.close()
        except sqlite3.Error as e:
            print(e)
            return False
        return True

    def import_all_csv(self):
        """Imports the data from the CSV files into the database"""
        for csv_file, table_name in self.CSV_TO_TABLE_MAP:
            if self.import_csv(self.CSV_ROOT + "/" + csv_file, table_name):
                print(f"Successfully imported {csv_file}")
            else:
                print(f"Failed to import {csv_file}")

    def handle(self, *args, **options):
        print("Importing data...")
        self.import_all_csv()
        print("Finished importing data")
