import scrapy

class AritcleSpider(scrapy.Spider):
    name='Article'

    def start_requests(self):
        urls=[
            'https://en.wikipedia.org/wiki/Python_(programming_language)',
            'https://en.wikipedia.org/wiki/Functional_programming',
            'https://en.wikipedia.org/wiki/Monty_Python']
        return [scrapy.Request(url=url,callback=self.parse) for url in urls]

    def parse(self,response):
        url = response.url
        title = response.css('h1::text').extract_first()
        print(f'URL is: {url}')
        print(f'Title is: {title}')