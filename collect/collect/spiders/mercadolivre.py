import scrapy


class MercadolivreSpider(scrapy.Spider):
    name = "mercadolivre"
    allowed_domains = ["lista.mercadolivre.com.br"]
    start_urls = ["https://lista.mercadolivre.com.br/teclado-mecanico#D[A:teclado%20mecanico]"]

    def parse(self, response):
        pass
