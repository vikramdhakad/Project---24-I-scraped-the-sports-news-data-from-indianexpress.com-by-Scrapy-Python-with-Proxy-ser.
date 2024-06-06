import scrapy
# from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class ScraperSpider(scrapy.Spider):
    name = "scraper"
    allowed_domains = ["indianexpress.com"]
    start_urls = ["https://indianexpress.com/section/sports/"]
    
        
    def parse(self, response):
        for title in response.xpath("//h2[@class='title']/a"):
            name = title.xpath("@href").get()
            yield response.follow(url=name,callback=self.data)
        
        for page in range(1,20):
            link = response.xpath("//a[@class='next page-numbers']/@href").get()
            yield response.follow(url=link, callback=self.parse)
            
        for titles in response.xpath("//h2[@class='title']/a"):
            names = titles.xpath("@href").get()
            yield response.follow(url=names,callback=self.data)
            
    def data (self, response):
        yield{
            "New Title": response.xpath("//h1/text()").get(),
            "News": response.xpath("(//h2/text())[1]").get(),
            "Date": response.xpath("//span[@itemprop='dateModified']/text()").get()
        }