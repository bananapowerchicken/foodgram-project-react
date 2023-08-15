import csv
from recipes.models import Ingredient

def load_ingredients(file_path):
    with open(file_path, encoding='utf-8', mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            Ingredient.objects.get_or_create(name=row[0], measurement_unit=row[1])

# docker-compose exec backend python manage.py shell
# from scripts.load_csv import load_ingredients
# load_ingredients('data/ingredients.csv')