import logging

from fake_useragent import UserAgent

from .arguments_setup import init_argument_parser

REQUEST_DELAY = 1.0

BASE_URL = "https://www.ebay.com/sch/garlandcomputer/m.html"

HEADERS = {
    'User-Agent': UserAgent().random,
    'Accept-Language': 'en-US,en;q=0.9',
}

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='scrape_log.log',
    filemode='w',
)

parser = init_argument_parser()
args = parser.parse_args()
