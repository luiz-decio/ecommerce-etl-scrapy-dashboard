import scrapy

class MercadolivreSpider(scrapy.Spider):
    name = "mercadolivre"
    #allowed_domains = ["lista.mercadolivre.com.br"]
    start_urls = ["https://lista.mercadolivre.com.br/tenis-corrida-masculino"]
    
    # Creating a page count to limit the number of pages to parse
    page_count = 1
    max_pages = 10

    def parse(self, response):
        # Fetch all the products in the web page
        products = response.css('div.ui-search-result__content')
        
        # Parse each product in order to get the data
        for product in products:

            # Create a list of the whole prices and cents for each product (old price, new price and discount)
            prices = product.css('span.andes-money-amount__fraction::text').getall()
            cents = product.css('span.andes-money-amount__cents::text').getall()

            yield {
                'brand' : product.css('span.ui-search-item__brand-discoverability.ui-search-item__group__element::text').get() ,
                'name' : product.css('h2.ui-search-item__title::text').get() ,
                'old_price' : prices[0] if len(prices) > 0 else None ,
                'old_price_cents' : cents[0] if len(cents) > 0 else None ,
                'new_price' : prices[1] if len(prices) > 1 else None ,
                'new_price_cents' : cents[1] if len(cents) > 1 else None ,
                'reviews_rating_number' : product.css('span.ui-search-reviews__rating-number::text').get() ,
                'reviews_amount' : product.css('span.ui-search-reviews__amount::text').get()
            }

        # Checking the page number and proceeding to the next one in case it has not reached the page limit
        if self.page_count <= self.max_pages:
            next_page = response.css('li.andes-pagination__button.andes-pagination__button--next a::attr(href)').get()
            if next_page:
                self.page_count += 1
                yield scrapy.Request(url=next_page, callback=self.parse)