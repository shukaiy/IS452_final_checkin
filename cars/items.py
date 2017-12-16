# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CarItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    Price = scrapy.Field()
    Mileage = scrapy.Field()
    Dealer_name = scrapy.Field()
    Dealer_address = scrapy.Field()
    Dealer_phone_number = scrapy.Field()
    Engine = scrapy.Field()
    Transmission = scrapy.Field()
    Drivetrain = scrapy.Field()
    VIN = scrapy.Field()
    Stock = scrapy.Field()
    Interior_Color = scrapy.Field()
    Exterior_Color = scrapy.Field()
    MPG = scrapy.Field()
    FuelType = scrapy.Field()
    Car_id = scrapy.Field()

