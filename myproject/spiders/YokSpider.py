import scrapy
from myproject.items import UniversityItem
from scrapy_splash import SplashRequest

class YokSpider(scrapy.Spider):
    name = "yok_spider"
    counter = 0
    start_urls = [
        'https://yokatlas.yok.gov.tr/tercih-sihirbazi-t4-tablo.php?p=say',
    ]
    script = """
    function main(splash, args)
        splash.private_mode_enabled = false
        splash:set_viewport_full()
        splash:go(args.url)

        local wait_after_click = 5.0
        local scrolls = 0
        local page_number = args.page_number

        local scroll_to = splash:jsfunc('window.scrollTo')
        local get_body_height = splash:jsfunc(
            'function() { return document.body.scrollHeight; }'
        )

        while scrolls <= page_number do
            scroll_to(0, get_body_height())
            splash:wait(2.0)  -- Short wait before clicking
            splash:runjs("document.querySelector('#mydata_next a').click()")
            splash:wait(wait_after_click)  -- Wait for the content to load
            scrolls = scrolls + 1
        end


        return {
            html = splash:html(),
            url = splash:url()
        }
    end
    """
    

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, callback=self.parse, endpoint='execute', args={'lua_source': self.script, 'wait': 5, 'page_number': self.counter})
            self.counter+=1

    def parse(self, response):
        rows = response.css('#mydata > tbody > tr')

        for row in rows:
            item = UniversityItem()
            item['university_id'] = row.css('td:nth-child(2) a::text').get()
            item['university_name'] = row.css('td:nth-child(3) strong::text').get().strip()
            item['faculty_name'] = row.css('td:nth-child(3) font::text').get()
            item['department_name'] = row.css('td:nth-child(4) strong::text').get().strip()
            item['language_and_program_type'] = row.css('td:nth-child(4) font::text').get()
            item['location'] = row.css('td:nth-child(5)::text').get().strip()
            item['university_type'] = row.css('td:nth-child(6)::text').get()
            item['fee_status'] = row.css('td:nth-child(7)::text').get()
            item['education_type'] = row.css('td:nth-child(8)::text').get()
            item['quota'] = row.css('td:nth-child(9) font[color="red"]::text').get()
            item['status'] = row.css('td:nth-child(10)::text').get()

            yield item

        # Determine if it's the first page or not
        next_page_url = response.css('#mydata_next a::attr(href)').get()
        self.counter+=1
        if next_page_url:
            yield SplashRequest(response.url, self.parse, endpoint='execute', args={'lua_source': self.script, 'wait': 5, 'page_number': self.counter})
        else:
            self.log("Next button is disabled, no more pages to scrape.")
