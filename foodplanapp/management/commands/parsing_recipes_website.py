import requests

from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand


def parse_receipt_pages(response):
    receipts = []
    soup = BeautifulSoup(response.text, "lxml")

    receipt_urls = [
        receipt_tags["href"]
        for receipt_tags in soup.select("div.content-md h2 a")
    ]

    for receipt_url in receipt_urls:
        response = requests.get(receipt_url)
        response.raise_for_status()

        receipt_soup = BeautifulSoup(response.text, "lxml")

        receipt_name = receipt_soup.select_one("h1").text
        receipt_image = receipt_soup.select_one("div.m-img img")["src"]
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

        receipt_attributes = {
            "receipt_name": receipt_name,
            "receipt_image": receipt_image,
            "receipt_ingredients": receipt_ingredients,
        }

        receipts.append(receipt_attributes)

    return receipts


class Command(BaseCommand):
    help = "Парсинг сайта с рецепатами povarenok.ru"

    def handle(self, *args, **options):
        # рецепты супов
        soup_receipts_url = (
            "https://www.povarenok.ru/recipes/dishes/first/?searchid=28"
        )
        soup_receipts_url_response = requests.get(soup_receipts_url)
        soup_receipts_url_response.raise_for_status()

        soup_receipts = parse_receipt_pages(soup_receipts_url_response)

        # print(soup_receipts)
