"""
Вставка случайных товаров и SKU
"""
import asyncio
from random import randint, sample
from typing import List, Tuple

import asyncpg

from ch5.listing_5_5 import load_common_words


def generate_products(
    common_words: List[str],
    brand_id_start: int,
    brand_id_end: int,
    products_to_create: int,
) -> List[Tuple[str, int]]:
    products = []
    for _ in range(products_to_create):
        description = [
            common_words[index].replace("\n", "")
            for index in sample(range(len(common_words)), 10)
        ]
        description = " ".join(description).capitalize()
        brand_id = randint(brand_id_start, brand_id_end)
        products.append((description, brand_id))
    return products


def generate_skus(
    product_id_start: int,
    product_id_end: int,
    skus_to_create: int,
) -> List[Tuple[int, int, int]]:
    skus = []
    for _ in range(skus_to_create):
        product_id = randint(product_id_start, product_id_end)
        size_id = randint(1, 3)
        color_id = randint(1, 2)
        skus.append((product_id, size_id, color_id))
    return skus


async def main() -> None:
    common_words = load_common_words()
    product_tuples = generate_products(
        common_words, brand_id_start=1, brand_id_end=100, products_to_create=1000
    )
    sku_tuples = generate_skus(
        product_id_start=1, product_id_end=1000, skus_to_create=100000
    )
    connection = await asyncpg.connect(
        host="127.0.0.1",
        port=5432,
        user="postgres",
        database="products",
        password="postgres",
    )
    await connection.executemany(
        "INSERT INTO product VALUES(DEFAULT, $1, $2)", product_tuples
    )
    await connection.executemany(
        "INSERT INTO sku VALUES(DEFAULT, $1, $2, $3)", sku_tuples
    )
    await connection.close()


asyncio.run(main())
