import os

import requests

from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from urllib.parse import urljoin, urlparse, unquote

from foodplanapp.models import (
    Dish,
    Dishitems,
)


def get_file_name(url):
    parsed_url = urlparse(url)
    path = unquote(parsed_url.path)
    _, file_name = os.path.split(path)

    return file_name


def download_image(url, filename, folder="images/"):
    response = requests.get(url)
    response.raise_for_status()
    file_path = os.path.join(folder, filename)
    with open(file_path, "wb") as file:
        file.write(response.content)

    return file_path


def parse_receipt_pages(response):
    receipts = []

    images_folder_name = os.path.join(os.getcwd(), "images/")
    os.makedirs(images_folder_name, exist_ok=True)

    soup = BeautifulSoup(response.text, "lxml")

    receipt_urls = [
        receipt_tags["href"]
        for receipt_tags in soup.select("div.content-md h2 a")
    ]

    for receipt_url in receipt_urls:
        receipt_guide = ""

        response = requests.get(receipt_url)
        response.raise_for_status()

        receipt_soup = BeautifulSoup(response.text, "lxml")

        receipt_name = receipt_soup.select_one("h1").text
        image_url = receipt_soup.select_one("div.m-img img")["src"]

        image_file_name = get_file_name(image_url)
        receipt_image = download_image(
            image_url, image_file_name, images_folder_name
        )

        receipt_ingredient_names = [
            name.text
            for name in receipt_soup.select(
                "div.ingredients-bl span[itemprop*=name]"
            )
        ]
        receipt_ingredient_amounts = [
            amount.text
            for amount in receipt_soup.select(
                "div.ingredients-bl span[itemprop*=amount]"
            )
        ]
        receipt_ingredients = [
            list(x)
            for x in zip(receipt_ingredient_names, receipt_ingredient_amounts)
        ]
        receipt_nutritional_value = receipt_soup.select_one(
            "div[id*=nae-value-bl] table tr"
        )

        nutritional_table = receipt_soup.find("table")
        need_row = nutritional_table.find_all("tr")[1]
        columns = need_row.find_all("td")
        receipt_nutritional_value = (
            columns[0].find("strong").text.strip().split()[0]
        )

        receipt_guide_rows = receipt_soup.select("div.cooking-bl div p")
        for receipt_guide_row in receipt_guide_rows:
            receipt_guide += "".join(receipt_guide_row.text)

        receipt_attributes = {
            "receipt_name": receipt_name,
            "receipt_image": receipt_image,
            "receipt_ingredients": receipt_ingredients,
            "receipt_nutritional_value": receipt_nutritional_value,
            "receipt_guide": receipt_guide,
        }

        receipts.append(receipt_attributes)

    return receipts


def put_test_data_to_db(receipts):
    for receipt in receipts:
        dish = Dish.objects.create(
            name=receipt["receipt_name"],
            image=receipt["receipt_image"],
            calories=receipt["receipt_nutritional_value"],
            guide=receipt["receipt_guide"],
        )
        for ingredient in receipt["receipt_ingredients"]:
            amount, measurement_unit = ingredient[1].split(" ", 1)
            Dishitems.objects.create(
                dish=dish,
                ingredient=ingredient[0],
                amount=amount,
                measurement_unit=measurement_unit,
            )


class Command(BaseCommand):
    help = "Парсинг сайта с рецепатами povarenok.ru"

    def handle(self, *args, **options):
        receipts_urls = [
            "https://www.povarenok.ru/recipes/dishes/first/?searchid=28",
            "https://www.povarenok.ru/recipes/dishes/main/?searchid=66",
            "https://www.povarenok.ru/recipes/dishes/starter/?searchid=1064",
            "https://www.povarenok.ru/recipes/dishes/bakery/?searchid=318",
            "https://www.povarenok.ru/recipes/dishes/sweet/?searchid=322",
            "https://www.povarenok.ru/recipes/dishes/drink/?searchid=525",
            "https://www.povarenok.ru/recipes/dishes/other/?searchid=510",
            "https://www.povarenok.ru/recipes/dishes/main/?searchid=72",
            "https://www.povarenok.ru/recipes/dishes/main/?searchid=97",
            "https://www.povarenok.ru/recipes/dishes/main/?searchid=165",
        ]

        for receipts_url in receipts_urls:
            print(receipts_url)
            receipts_url_response = requests.get(receipts_url)
            receipts_url_response.raise_for_status()

            receipts = parse_receipt_pages(receipts_url_response)

            put_test_data_to_db(receipts)
