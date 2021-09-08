# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags


# def remove_currency(value):
#     return value.replace('Rs', '').strip()

def absolute_url(url, loader_context):
    return loader_context['response'].url


def remove_extra_strings(value):
    return value.replace('\n', '').replace('  ', '').replace('(', '').replace(')', '').strip()


def remove_extra_part(value):
    return value.replace('\n', '').replace('  ', '')[0:7].replace('•', '').strip()


class TourRadarItem(scrapy.Item):
    # define the fields for your item here like:
    Package_Title = scrapy.Field(input_processor=MapCompose(remove_tags, remove_extra_strings), output_processor=TakeFirst())
    Url = scrapy.Field(input_processor=MapCompose(remove_tags, absolute_url), output_processor=TakeFirst())
    Price = scrapy.Field(input_processor=MapCompose(remove_tags, remove_extra_strings))
    Duration = scrapy.Field(input_processor=MapCompose(remove_tags, remove_extra_part), output_processor=TakeFirst())
    Rating = scrapy.Field(input_processor=MapCompose(remove_tags, remove_extra_strings), output_processor=TakeFirst())
    Reviews = scrapy.Field(input_processor=MapCompose(remove_tags, remove_extra_strings), output_processor=TakeFirst())
    Group_size = scrapy.Field(input_processor=MapCompose(remove_tags, remove_extra_strings), output_processor=TakeFirst())
    Highlights = scrapy.Field(input_processor=MapCompose(remove_tags))
    Itinerary = scrapy.Field(input_processor=MapCompose(remove_tags))


