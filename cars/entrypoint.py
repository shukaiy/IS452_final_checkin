# -*- coding: utf-8 -*-

from scrapy import cmdline
cmdline.execute("scrapy crawl cars -o cars.csv".split())

