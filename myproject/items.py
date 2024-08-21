# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class UniversityItem(scrapy.Item):
    university_id = scrapy.Field()
    university_name = scrapy.Field()
    faculty_name = scrapy.Field()
    department_name = scrapy.Field()
    language_and_program_type = scrapy.Field()
    location = scrapy.Field()
    university_type = scrapy.Field()
    fee_status = scrapy.Field()
    education_type = scrapy.Field()
    quota = scrapy.Field()
    status = scrapy.Field()
