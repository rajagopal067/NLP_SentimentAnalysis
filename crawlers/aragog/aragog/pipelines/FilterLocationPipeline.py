from ..items.items import AragogItem
from scrapy.exceptions import DropItem
from scrapy.selector import Selector


class FilterLocationPipeline(object):
	def isValidLocation(self,item):
		valid = False
		htmlTxt =item["body"]
		locs = ["Los Angeles","LA","Seattle","New York","NY"]
		bizSubHeader=Selector(text=htmlTxt).xpath('//div[@class="biz-page-subheader"]')
		if len(bizSubHeader) > 0 :
			address  = bizSubHeader.xpath('//div[@class="mapbox-text"]/ul/li[@class="address"]//address[@itemprop="address"]/span/text()').extract()
			if len(address)>0 and len(set(locs) & set(address)) >0:
				valid = True
		return valid
	def process_item(self, item, spider):
		if self.isValidLocation(item) :
			return item
		else :
			raise DropItem("[DROP] Page did not meet Business Location Criteria - Dropping")
