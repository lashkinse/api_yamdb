import sqlite3
from os import listdir
from os.path import isfile, join

import pandas as pandas
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Imports the data from the CSV files into the database"
    CSV_ROOT = "./static/data"
    DATABASE_PATH = "./db.sqlite3"

    def import_csv(self, csv_file, table_name):
        """
        Imports the data from the CSV file into the database
        """
        try:
            conn = sqlite3.connect(self.DATABASE_PATH)
            df = pandas.read_csv(csv_file)
            df.to_sql(table_name, conn, if_exists="replace", index=False)
            conn.close()
        except sqlite3.Error as e:
            print(e)
            return False
        return True

    def import_csv_files(self):
        """
        Imports the data from the CSV files into the database
        """
        csv_files = [
            f for f in listdir(self.CSV_ROOT) if isfile(join(self.CSV_ROOT, f))
        ]
        for csv_file in csv_files:
            table_name = csv_file.replace(".csv", "")
            if self.import_csv(self.CSV_ROOT + "/" + csv_file, table_name):
                print(f"Successfully imported {csv_file}")
            else:
                print(f"Failed to import {csv_file}")

    def handle(self, *args, **options):
        print("Importing data...")
        self.import_csv_files()
        print("Finished importing data")
