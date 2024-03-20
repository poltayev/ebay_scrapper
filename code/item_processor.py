import json
import logging
import os
from typing import Protocol
from urllib.parse import parse_qs, urlparse

import aiofiles


class ItemDataExtractorProtocol(Protocol):
    async def extract_item_details(self, item) -> None: ...


class ItemDataSaverProtocol(Protocol):
    async def save_item_data(self, item_data, item_id) -> None: ...


class ItemProcessorProtocol(Protocol):
    async def process_item(self, item) -> None: ...


class ItemDataExtractor(ItemDataExtractorProtocol):
    def extract_item_details(self, item):
        title = item.find('div', class_='s-item__title').find('span').text
        price = item.find('span', class_='s-item__price').text
        product_url = item.find('a', class_='s-item__link')['href']
        condition = item.find('div', class_='s-item__subtitle').find('span').text

        return title, price, product_url, condition


class ItemDataSaver(ItemDataSaverProtocol):
    async def save_item_data(self, item_data, item_id):
        try:
            os.makedirs('data', exist_ok=True)
            async with aiofiles.open(f'data/{item_id}.json', 'w') as f:
                await f.write(json.dumps(item_data, indent=4))
        except Exception as e:
            logging.error(f"File operation failed: {e}", exc_info=True)


class ItemProcessor(ItemProcessorProtocol):
    def __init__(
        self,
        condition_filter,
        extractor: ItemDataExtractor,
        saver: ItemDataSaver,
    ):
        self.condition_filter = condition_filter
        self.extractor = extractor
        self.saver = saver

    async def process_item(self, item):
        title, price, product_url, condition = self.extractor.extract_item_details(item)
        if self.condition_filter and condition != self.condition_filter:
            logging.info(f"Skipping item due to condition filter: {title}")
            return

        item_id = self.get_item_id(product_url)
        item_data = {
            'title': title,
            'price': price,
            'product_url': product_url,
            'condition': condition,
        }
        logging.info(f"Processing item {title}")
        await self.saver.save_item_data(item_data, item_id)

    def get_item_id(self, url):
        parsed_url = urlparse(url)
        query_string = parse_qs(parsed_url.query)

        return query_string['hash'][0].split(':')[0]
