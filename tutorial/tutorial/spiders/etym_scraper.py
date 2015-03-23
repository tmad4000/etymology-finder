import scrapy
 
class WordUnit(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    link = scrapy.Field()
    small_desc = scrapy.Field()
    desc = scrapy.Field()
    words = scrapy.Field()
 
 
class WordInfoSpyder(scrapy.Spider):
	name = "wordinfo"
	allowed_domains = ["wordinfo.info"]
	# just a quick hack
	start_urls = [
		"http://wordinfo.info/units/index/page:{0}".format(i) for i in range(1, 184)
	]
 
	def parse(self, response):
		"""
		Build up a list of urls to visit to actually grab information
		"""
		for url in response.xpath('//*[@id="Units"]/div/a/@href').extract():
			request = scrapy.Request("http://wordinfo.info/" + url, callback=self.parse_word_unit, dont_filter=False)
			request.meta['wordunit'] = None
			yield request
 
	def parse_word_unit(self, response):
		"""
		Grab the list of all words for a given wordunit
		note: this could be a paginated subrequest
		"""
 
		if response.meta['wordunit']:
			# we've already seen this before
			wordunit = response.meta['wordunit']
		else:
			# grab all the information
			wordunit = WordUnit()
			wordunit['name'] = response.css("h1.title").extract()[0].strip()
			wordunit['link'] = response.url 
			wordunit['desc'] = "".join(response.css(".description p").extract())
			wordunit['small_desc'] = response.css("h4.comment").extract()[0].strip()
			wordunit['words'] = []
 
		assert type(wordunit) == type(WordUnit())
 
		# grab all the words on the page
		for word in response.css('.word'):
			wordunit['words'].append({
				'word' : word.xpath("div[1]/text()[1]").extract()[0].strip(),
				'definition' : word.css(".definition").extract()[0].strip(),
				'part_of_speech' : word.css("a b").extract()[0].strip() if len(word.css("a b").extract()) else ""
			})
 
			# hella sketchy
			a = response.xpath('//*[@id="Unit"]/div[4]/div/span/a/img/@src').extract()
			if len(a) == 2 and a[0] != "/img/right_arrow_sm.gif":
				print("FOUND AN ENDING POINT")
				# then return this thing
				yield wordunit
 
 
		# now add new links (automatic filtering prevents extra links)
		for url in response.xpath('//*[@id="Unit"]/div[4]/div[1]/span/a/@href').extract():
			request = scrapy.Request("http://wordinfo.info/" + url, callback=self.parse_word_unit, dont_filter=False)
			request.meta['wordunit'] = wordunit
			yield request