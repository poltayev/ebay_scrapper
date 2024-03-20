import asyncio
import logging
from code.item_processor import ItemDataExtractor, ItemDataSaver, ItemProcessor
from code.service import ScraperService
from code.utilities.settings import BASE_URL, HEADERS, REQUEST_DELAY, args


async def main():
    processor = ItemProcessor(
        condition_filter=args.condition,
        extractor=ItemDataExtractor(),
        saver=ItemDataSaver(),
    )
    scrapeService = ScraperService(HEADERS, REQUEST_DELAY, processor)

    logging.info("eBay crawler started...")
    await scrapeService.scrape_ebay(BASE_URL, max_pages=args.max_pages)
    logging.info("eBay crawler has finished.")


if __name__ == '__main__':
    asyncio.run(main())
