import asyncio
import logging

import aiofiles
import httpx
from bs4 import BeautifulSoup

from .item_processor import ItemProcessorProtocol


class ScraperService:
    def __init__(self, headers, request_delay, processor: ItemProcessorProtocol):
        self.headers = headers
        self.request_delay = request_delay
        self.processor = processor

    async def scrape_ebay(self, url, max_pages=10):
        page_count = 0
        async with httpx.AsyncClient(http2=True) as client:
            while url and page_count < max_pages:
                logging.info(f"Fetching page {page_count + 1} of {max_pages}")
                soup = await self.scrape_page(client, url, page_count + 1)
                if soup is None:
                    break

                next_page = soup.find('a', class_='pagination__next')
                url = next_page['href'] if next_page else None
                page_count += 1

                await asyncio.sleep(self.request_delay)

    async def scrape_page(self, client, url, page_count):
        try:
            response = await client.get(
                url,
                headers=self.headers,
                follow_redirects=True,
            )
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            async with aiofiles.open(f'resources/parsed_{page_count}.html', 'w') as f:
                await f.write(soup.prettify())

            items = soup.find('ul', class_='srp-results').find_all(
                'li', class_='s-item'
            )
            if not items:
                logging.info(f"No items found on page {page_count}.")
                return soup

            for item in items:
                await self.processor.process_item(item)
            return soup
        except httpx.HTTPStatusError as e:
            logging.error(
                f"HTTP status error for {url}: {e.response.status_code}",
                exc_info=True,
            )
            return None
        except httpx.RequestError as e:
            logging.error(f"Request error for {url}: {e}", exc_info=True)
            return None
        except Exception as e:
            logging.exception(
                f"An unexpected error occurred while processing page {page_count}: {e}"
            )
            return None
