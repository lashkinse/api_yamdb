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
            obj_list = []
            for row in csv.reader(f, dialect="excel"):
                obj_list.append(
                    User(
                        id=row[0],
                        username=row[1],
                        email=row[2],
                        role=row[3],
                        bio=row[4],
                        first_name=row[5],
                        last_name=row[6],
                    ),
                )
        User.objects.bulk_create(obj_list)

    @staticmethod
    def import_categories_from_csv():
        """Imports the categories from the CSV file into the database"""
        with open(settings.CSV_FILES_DIR / "category.csv", "rt") as f:
            f.readline()
            obj_list = []
            for row in csv.reader(f, dialect="excel"):
                obj_list.append(
                    Category(
                        id=row[0],
                        name=row[1],
                        slug=row[2],
                    ),
                )
            Category.objects.bulk_create(obj_list)

    @staticmethod
    def import_comments_from_csv():
        """Imports the comments from the CSV file into the database"""
        with open(settings.CSV_FILES_DIR / "comments.csv", "rt") as f:
            f.readline()
            obj_list = []
            for row in csv.reader(f, dialect="excel"):
                obj_list.append(
                    Comment(
                        id=row[0],
                        review=Review.objects.get(id=row[1]),
                        text=row[2],
                        author=User.objects.get(id=row[3]),
                        pub_date=row[4],
                    ),
                )
            Comment.objects.bulk_create(obj_list)

    @staticmethod
    def import_genres_from_csv():
        """Imports the genres from the CSV file into the database"""
        with open(settings.CSV_FILES_DIR / "genre.csv", "rt") as f:
            f.readline()
            obj_list = []
            for row in csv.reader(f, dialect="excel"):
                obj_list.append(
                    Genre(
                        id=row[0],
                        name=row[1],
                        slug=row[2],
                    ),
                )
            Genre.objects.bulk_create(obj_list)

    @staticmethod
    def import_titles_from_csv():
        """Imports the titles from the CSV file into the database"""
        with open(settings.CSV_FILES_DIR / "titles.csv", "rt") as f:
            f.readline()
            obj_list = []
            for row in csv.reader(f, dialect="excel"):
                obj_list.append(
                    Title(
                        id=row[0],
                        name=row[1],
                        year=row[2],
                        category=Category.objects.get(id=row[3]),
                    ),
                )
            Title.objects.bulk_create(obj_list)

    @staticmethod
    def import_reviews_from_csv():
        """Imports the reviews from the CSV file into the database"""
        with open(settings.CSV_FILES_DIR / "review.csv", "rt") as f:
            f.readline()
            obj_list = []
            for row in csv.reader(f, dialect="excel"):
                obj_list.append(
                    Review(
                        id=row[0],
                        title=Title.objects.get(id=row[1]),
                        text=row[2],
                        author=User.objects.get(id=row[3]),
                        score=row[4],
                        pub_date=row[5],
                    ),
                )
            Review.objects.bulk_create(obj_list)

    @staticmethod
    def import_genre_titles_from_csv():
        """Imports the genre titles from the CSV file into the database"""
        with open(settings.CSV_FILES_DIR / "genre_title.csv", "rt") as f:
            f.readline()
            obj_list = []
            for row in csv.reader(f, dialect="excel"):
                obj_list.append(
                    GenreTitle(
                        id=row[0],
                        title=Title.objects.get(id=row[1]),
                        genre=Genre.objects.get(id=row[2]),
                    ),
                )
            GenreTitle.objects.bulk_create(obj_list)

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
