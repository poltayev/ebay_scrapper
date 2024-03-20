import argparse


def init_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="eBay Crawler")
    parser.add_argument(
        "--condition",
        type=str,
        help="Condition filter for items",
        default="New",
    )
    parser.add_argument(
        "--max_pages",
        type=int,
        help="Maximum number of pages to scrape",
        default=5,
    )

    return parser
