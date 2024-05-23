# ecommerce_etl_scrapy_dashboard

In order to run the web scraping script, run the following:

```bash
scrapy crawl mercadolivre -o ../../data/products_data.jsonl

scrapy crawl mercadolivre -o ../../data/products_data.csv
```

Command to run the data transofrmation script (run from the src directory):

```bash
python transform/main.py 
```