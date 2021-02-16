import scrapy

from scrapy.loader import ItemLoader
from ..items import GfbankasItem
from itemloaders.processors import TakeFirst


class GfbankasSpider(scrapy.Spider):
	name = 'gfbankas'
	start_urls = ['https://www.gfbankas.lt/blogas/']

	def parse(self, response):
		post_links = response.xpath('//h3[@class="news-title"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[@class="page-link right"]/@href').getall()
		yield from response.follow_all(next_page, self.parse)


	def parse_post(self, response):
		title = response.xpath('//h1[@class="fw-bold heading-size-1"]/text()').get()
		description = response.xpath('//div[@class="simple-content"]//p//text()').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//span[@class="news-date"]/text()').get()

		item = ItemLoader(item=GfbankasItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
