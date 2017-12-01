import sys
import json,re
import time
import scrapy
from scrapy.http import Request


class Cars_Spider(scrapy.Spider):
    name='Cars'
    allowed_domains = ["www.cars.com"]

    def start_requests(self):
        for page  in range(1,17):
            next_url='https://www.cars.com/for-sale/searchresults.action/?page={}&perPage=50&rd=10&searchSource=SORT&sort=price-highest&stkTypId=28881&zc=61801'.format(page)
            yield Request(next_url, self.parse,dont_filter = True)


    def parse(self, response):
        listingIds=response.xpath("//div[contains(@id,'listing-')]/@id").extract()
        Ids=[]
        for each_id in listingIds:
            id=re.search(re.compile('(\d+)',re.S),each_id)
            if id :
                Ids.append(id.group(0))

        for page_id in Ids:
            next_url='https://www.cars.com/vehicledetail/detail/{}/overview/'.format(page_id)
            yield Request(next_url, self.get_detail,dont_filter = True,meta={'Car_id':page_id})


    def get_detail(self,response):
        item=ErshoucheItem()
        item['title']=response.xpath("//div[@class='vdp-header']//div[@class='vdp-cap-mmy']/h1/text()").extract()[0]
        item['Car_id']=response.meta['Car_id']
        item['Price']=response.xpath("//section[@id='vdpOverview']/div[@class='vdp-cap-price']/div[@class='vdp-cap-price__price']/text()").extract()
        item['Mileage']=response.xpath("//section[@id='vdpOverview']/div[@class='vdp-cap-price']/span[@class='vdp-cap-price__mileage']/text()").extract()
        item['Dealer_name']=response.xpath("//div[@class='dealer_box']/div[@class='dealer_box__info']/span[@class='dealer_box__name']/text()").extract()
        item['Dealer_address']=response.xpath("//div[@class='dealer_box']/div[@class='dealer_box__info']/span[@class='dealer_box__address']/text()").extract()
        item['Dealer_phone_number']=response.xpath("//div[@class='dealer_box']/div[@class='dealer_box__info']/span[@class='dealer_box__phone--desktop']/text()").extract()

        item['Engine']=self.get_text(response.xpath("//div[@class='vdp-details-basics accordion__section']/div[@class='accordion__section-body']/dl[@class='vdp-details-basics__facets']//strong[contains(text(),'Engine')]/..").xpath('string(.)').extract())
        item['Transmission']=self.get_text(response.xpath("//div[@class='vdp-details-basics accordion__section']/div[@class='accordion__section-body']/dl[@class='vdp-details-basics__facets']//strong[contains(text(),'Transmission')]/..").xpath('string(.)').extract())
        item['Drivetrain']=self.get_text(response.xpath("//div[@class='vdp-details-basics accordion__section']/div[@class='accordion__section-body']/dl[@class='vdp-details-basics__facets']//strong[contains(text(),'Drivetrain')]/..").xpath('string(.)').extract())
        item['VIN']=self.get_text(response.xpath("//div[@class='vdp-details-basics accordion__section']/div[@class='accordion__section-body']/dl[@class='vdp-details-basics__facets']//strong[contains(text(),'VIN')]/..").xpath('string(.)').extract())
        item['Stock']=self.get_text(response.xpath("//div[@class='vdp-details-basics accordion__section']/div[@class='accordion__section-body']/dl[@class='vdp-details-basics__facets']//strong[contains(text(),'Stock')]/..").xpath('string(.)').extract())
        item['Interior_Color']=self.get_text(response.xpath("//div[@class='vdp-details-basics accordion__section']/div[@class='accordion__section-body']/dl[@class='vdp-details-basics__facets']//strong[contains(text(),'Interior')]/..").xpath('string(.)').extract())
        item['Exterior_Color']=self.get_text(response.xpath("//div[@class='vdp-details-basics accordion__section']/div[@class='accordion__section-body']/dl[@class='vdp-details-basics__facets']//strong[contains(text(),'Exterior')]/..").xpath('string(.)').extract())
        item['MPG']=self.get_text(response.xpath("//div[@class='vdp-details-basics accordion__section']/div[@class='accordion__section-body']/dl[@class='vdp-details-basics__facets']//strong[contains(text(),'MPG')]/..").xpath('string(.)').extract())
        item['FuelType']=self.get_text(response.xpath("//div[@class='vdp-details-basics accordion__section']/div[@class='accordion__section-body']/dl[@class='vdp-details-basics__facets']//strong[contains(text(),'FuelType')]/..").xpath('string(.)').extract())

        yield item

    def get_text(self,s_path):
        if len(s_path)>0:
            return s_path[0].split(':')[-1].replace('\n','').strip()
