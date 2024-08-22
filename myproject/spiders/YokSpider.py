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
        splash.private_mode_enabled = false  -- Disable private mode
        assert(splash:go(args.url))          -- Navigate to the URL
        assert(splash:wait(args.wait))       -- Wait for the page to load

        -- Try to find and click the 'Next' button
        local next_button_disabled = splash:select('#mydata_next.disabled')
        if not next_button_disabled then
            local next_button = splash:select('#mydata_next a')
            next_button:mouse_click()        -- Click the 'Next' button
            assert(splash:wait(args.wait))   -- Wait for the table to update
        end

        return {
            html = splash:html(),  -- Return the updated page HTML
            url = splash:url(),    -- Return the current page URL
        }
    end


    """

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, callback = self.parse, endpoint='execute', args={'lua_source': self.script, 'wait': 5})

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
            
        next_page_url = response.css('#mydata_next a::attr(href)').get()
        if next_page_url:
            # If not disabled, request the next page
            yield SplashRequest(response.url, self.parse, endpoint='execute', args={'lua_source': self.script, 'wait': 5})
        else:
            print("Next button is disabled, no more pages to scrape.")