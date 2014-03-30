from scrapy.spider import Spider
from scrapy import log
import re


class FourmiSpider(Spider):
	name = "FourmiSpider"
	start_urls = ["http://localhost/"]
	parsers = []

	def __init__(self, compound=None, *args, **kwargs):
		super(FourmiSpider, self).__init__(*args, **kwargs)
		self.synonyms = [compound]

	def parse(self, reponse):
		for parser in self.parsers:
			if re.match(parser.website, reponse.url):
				log.msg("Url: " + reponse.url + " -> Parser: " + parser.website, level=log.DEBUG)
				return parser.parse(reponse)
		return none


	def add_parser(self, parser):
		self.parsers.append(parser)
