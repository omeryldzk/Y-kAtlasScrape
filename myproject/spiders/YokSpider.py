import json
import scrapy
from myproject.items import UniversityItem
from scrapy import FormRequest

class YokSpider(scrapy.Spider):
    name = "yok_spider"
    start_urls = [
        'https://yokatlas.yok.gov.tr/tercih-sihirbazi-t4-tablo.php?p=say',
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse_initial)

    def parse_initial(self, response):
        headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': response.request.headers.get('User-Agent').decode('utf-8'),
            'Referer': response.url,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
        
        # Start with the first AJAX request
        yield self.make_ajax_request(1, headers)

    def make_ajax_request(self, page_number, headers):
        return FormRequest(
            url='https://yokatlas.yok.gov.tr/server_side/server_processing-atlas2016-TS-t4.php',
            formdata={
                'draw': str(page_number),
                'start': str((page_number - 1) * 10),  # Adjust this based on the pagination (10 rows per page)
                'length': '10',  # Number of rows per page
                # Add other form data parameters captured from the browser if required
            },
            headers=headers,
            callback=self.parse_ajax_response,
            meta={'page_number': page_number}
        )

    def parse_ajax_response(self, response):
        try:
            self.logger.debug(f"Response body: {response.body.decode('utf-8')}")
            json_response = json.loads(response.body.decode('utf-8'))  # Attempt to parse JSON
            data = json_response.get('data', [])

            for row in data:
                item = UniversityItem()
                item['university_id'] = self.extract_university_id(row)
                item['university_name'] = self.extract_university_name(row)
                item['faculty_name'] = self.extract_faculty_name(row)
                item['department_name'] = self.extract_department_name(row)
                item['language_and_program_type'] = self.extract_language_and_program_type(row)
                item['location'] = self.extract_location(row)
                item['university_type'] = self.extract_university_type(row)
                item['fee_status'] = self.extract_fee_status(row)
                item['education_type'] = self.extract_education_type(row)
                item['quota'] = self.extract_quota(row)
                item['status'] = self.extract_status(row)

                yield item
            
            # Check if there are more pages to scrape
            page_number = response.meta['page_number']
            if page_number * 10 < int(json_response.get('recordsFiltered', 0)):
                yield self.make_ajax_request(page_number + 1, response.request.headers)

        except json.JSONDecodeError:
            self.logger.error("Failed to parse JSON response")
            self.logger.debug(f"Response body: {response.body.decode('utf-8')}")

    # Define extraction methods for the fields based on your row structure
    def extract_university_id(self, row):
        return row[1].split('>')[2].split('<')[0].strip()

    def extract_university_name(self, row):
        return row[2].split('>')[3].split('<')[0].strip()

    def extract_faculty_name(self, row):
        return row[2].split('>')[5].split('<')[0].strip()

    def extract_department_name(self, row):
        return row[3].split('>')[2].split('<')[0].strip()

    def extract_language_and_program_type(self, row):
        return row[3].split('>')[5].split('<')[0].strip()

    def extract_location(self, row):
        return row[4].strip()

    def extract_university_type(self, row):
        return row[5].strip()

    def extract_fee_status(self, row):
        return row[6].strip()

    def extract_education_type(self, row):
        return row[7].strip()

    def extract_quota(self, row):
        return row[8].strip()

    def extract_status(self, row):
        return row[9].strip()
