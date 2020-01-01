import scrapy

from w3lib.html import remove_tags

from scrapy.loader.processors import Join, TakeFirst, MapCompose
from scrapy.loader import ItemLoader


class VeducaItemLoader(ItemLoader):
    
    default_output_processor = TakeFirst()

    instructors_description_in = MapCompose(remove_tags, str.strip)


class CourseItem(scrapy.Item):
    
    title = scrapy.Field()
    headline = scrapy.Field()
    url = scrapy.Field()
    instructors = scrapy.Field()
    instructors_description = scrapy.Field()
    lectures = scrapy.Field(
        output_processor=Join(' | ')
    )
    image = scrapy.Field()
