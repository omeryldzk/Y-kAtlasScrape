import scrapy
from myproject.items import UniversityItem
from scrapy_splash import SplashRequest

class YokSpider(scrapy.Spider):
    name = "yok_spider"
    start_urls = [
        'https://yokatlas.yok.gov.tr/tercih-sihirbazi-t4-tablo.php?p=say',
    ]
    script = """
    function main(splash, args)
        splash.private_mode_enabled = false
        assert(splash:go(args.url))
        assert(splash:wait(5))

        -- Execute the click on the "Next" button
        local next_button = splash:select('#mydata_next a')
        if next_button then
            next_button:mouse_click()
            assert(splash:wait(5))  -- Wait for the content to load
        end

        return {
            html = splash:html(),
            url = splash:url(),
            -- Optional: take a screenshot to see what is happening
            -- png = splash:png(),
        }
    end
    """

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 5})

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
            item['status'] = row.css('td:nth-child(10) font[color="red"]::text').get()

            yield item
            
        next_button_disabled = response.css('#mydata_next').xpath('@class').get() == 'paginate_button next disabled'
        if not next_button_disabled:
            # If not disabled, request the next page
            yield SplashRequest(response.url, self.parse, endpoint='execute', args={'lua_source': self.script, 'wait': 5})
        else:
            print("Next button is disabled, no more pages to scrape.")