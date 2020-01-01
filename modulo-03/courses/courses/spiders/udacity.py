import scrapy


class UdacitySpider(scrapy.Spider):

    name = "udacity"
    start_urls = ['https://br.udacity.com/courses/all/']

    def parse(self, response):
        divs = response.xpath("/html/body/div[1]/div/div[2]/div[2]/div[1]/div")
        for div in divs:
            link = div.xpath('.//h3/a')
            href = link.xpath('./@href').extract_first()
            yield scrapy.Request(
                url='https://br.udacity.com%s' % href,
                callback=self.parse_detail
            )

    def parse_detail(self, response):
        title = response.xpath('//title/text()').extract_first()
        headline = response.xpath(
            '//h2[contains(@class, "course-header-subtitle")]/text()'
        ).extract_first()
        image = response.xpath(
            '/html/body/div[1]/div[2]/div/div/div/div[2]/div[2]/div[1]/img/@src'
        ).extract_first()
        instructors = []
        for div in response.xpath('//div[contains(@class, "instructor-information-entry")]'):
            instructors.append(
                {
                    'name': div.xpath('.//h3//span/text()').extract_first(),
                    'image': div.xpath('.//img/@src').extract_first(),
                }
            )
        yield {
            'title': title,
            'headline': headline,
            'image': image,
            'instructors': instructors,
        }
