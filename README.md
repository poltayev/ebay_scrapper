# eBay Scraper
A simple scraper to collect data from eBay listings, allowing filtering by item condition and page limit.

## Quickstart
### Local Setup
Install dependencies:
```bash
pip install -r requirements.txt
```


### Run the scraper:
```bash
# 'condition' is a filter, which can have such values as "New", "Pre-Owned", etc. Default values is "New"
# 'max_pages' is the pages' scrapping limitations. Default value is 5

python3 main.py --condition "New" --max_pages 5
```

## Or use Docker Compose:
```bash
docker-compose up # but in the current version you will be needed to change command arguments in docker-compose.yml file
```