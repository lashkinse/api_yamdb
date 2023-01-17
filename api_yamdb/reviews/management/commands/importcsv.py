import sqlite3
from datetime import datetime

import pandas as pandas
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Imports the data from the CSV files into the database"
    CSV_ROOT = "./static/data"
    DATABASE_PATH = "./db.sqlite3"

    USERS_TABLE = "users_user"
    CSV_TO_TABLE_MAP = (
        ("category.csv", "reviews_category"),
        ("genre.csv", "reviews_genre"),
        ("titles.csv", "reviews_title"),
        ("users.csv", USERS_TABLE),
    )

    @staticmethod
    def fix_users_df(df):
        df = df.fillna("")
        df.insert(len(df.columns), "password", "")
        df.insert(len(df.columns), "is_superuser", 0)
        df.insert(len(df.columns), "is_staff", 0)
        df.insert(len(df.columns), "is_active", 1)
        df.insert(len(df.columns), "date_joined", datetime.now())
        return df

    def import_csv(self, csv_file, table_name):
        """
        Imports the data from the CSV file into the database
        """
        try:
            conn = sqlite3.connect(self.DATABASE_PATH)
            df = pandas.read_csv(
                csv_file,
                encoding="utf-8",
            )
            if table_name == self.USERS_TABLE:
                df = self.fix_users_df(df)
            df.to_sql(table_name, conn, if_exists="append", index=False)
            conn.close()
        except sqlite3.Error as e:
            print(e)
            return False
        return True

    def import_all_csv(self):
        """
        Imports the data from the CSV files into the database
        """
        for csv_file, table_name in self.CSV_TO_TABLE_MAP:
            if self.import_csv(self.CSV_ROOT + "/" + csv_file, table_name):
                print(f"Successfully imported {csv_file}")
            else:
                print(f"Failed to import {csv_file}")

    def handle(self, *args, **options):
        print("Importing data...")
        self.import_all_csv()
        print("Finished importing data")
