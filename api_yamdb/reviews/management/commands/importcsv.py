import csv

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from api_yamdb import settings
from reviews.models import Category, Comment, Genre, Review, Title, GenreTitle

User = get_user_model()


class Command(BaseCommand):
    help = "Imports the data from the CSV files into the database"

    @staticmethod
    def import_users_from_csv():
        """Imports the users from the CSV file into the database"""
        with open(settings.CSV_FILES_DIR / "users.csv", "rt") as f:
            f.readline()
            reader = csv.reader(f, dialect="excel")
            for row in reader:
                User.objects.create(
                    id=row[0],
                    username=row[1],
                    email=row[2],
                    role=row[3],
                    bio=row[4],
                    first_name=row[5],
                    last_name=row[6],
                )

    @staticmethod
    def import_categories_from_csv():
        """Imports the categories from the CSV file into the database"""
        with open(settings.CSV_FILES_DIR / "category.csv", "rt") as f:
            f.readline()
            reader = csv.reader(f, dialect="excel")
            for row in reader:
                Category.objects.create(
                    id=row[0],
                    name=row[1],
                    slug=row[2],
                )

    @staticmethod
    def import_comments_from_csv():
        """Imports the comments from the CSV file into the database"""
        with open(settings.CSV_FILES_DIR / "comments.csv", "rt") as f:
            f.readline()
            reader = csv.reader(f, dialect="excel")
            for row in reader:
                Comment.objects.create(
                    id=row[0],
                    review=Review.objects.get(id=row[1]),
                    text=row[2],
                    author=User.objects.get(id=row[3]),
                    pub_date=row[4],
                )

    @staticmethod
    def import_genres_from_csv():
        """Imports the genres from the CSV file into the database"""
        with open(settings.CSV_FILES_DIR / "genre.csv", "rt") as f:
            f.readline()
            reader = csv.reader(f, dialect="excel")
            for row in reader:
                Genre.objects.create(
                    id=row[0],
                    name=row[1],
                    slug=row[2],
                )

    @staticmethod
    def import_titles_from_csv():
        """Imports the titles from the CSV file into the database"""
        with open(settings.CSV_FILES_DIR / "titles.csv", "rt") as f:
            f.readline()
            reader = csv.reader(f, dialect="excel")
            for row in reader:
                Title.objects.create(
                    id=row[0],
                    name=row[1],
                    year=row[2],
                    category=Category.objects.get(id=row[3]),
                )

    @staticmethod
    def import_reviews_from_csv():
        """Imports the reviews from the CSV file into the database"""
        with open(settings.CSV_FILES_DIR / "review.csv", "rt") as f:
            f.readline()
            reader = csv.reader(f, dialect="excel")
            for row in reader:
                Review.objects.create(
                    id=row[0],
                    title=Title.objects.get(id=row[1]),
                    text=row[2],
                    author=User.objects.get(id=row[3]),
                    score=row[4],
                    pub_date=row[5],
                )

    @staticmethod
    def import_genre_titles_from_csv():
        """Imports the genre titles from the CSV file into the database"""
        with open(settings.CSV_FILES_DIR / "genre_title.csv", "rt") as f:
            f.readline()
            reader = csv.reader(f, dialect="excel")
            for row in reader:
                GenreTitle.objects.create(
                    id=row[0],
                    title=Title.objects.get(id=row[1]),
                    genre=Genre.objects.get(id=row[2]),
                )

    def handle(self, *args, **options):
        try:
            self.import_users_from_csv()
            self.import_categories_from_csv()
            self.import_titles_from_csv()
            self.import_reviews_from_csv()
            self.import_genres_from_csv()
            self.import_comments_from_csv()
            self.import_genre_titles_from_csv()
        except Exception as e:
            self.stdout.write(self.style.ERROR(e))
            raise e
        self.stdout.write(
            self.style.SUCCESS("CSV data was successfully imported!")
        )
