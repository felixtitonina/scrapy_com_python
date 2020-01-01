import scrapy

from courses import settings


class EdxLoginSpider(scrapy.Spider):
    
    name = 'edx_login'
    allowed_domains = ['courses.edx.org', 'edx.org']
    start_urls = [
        'https://courses.edx.org/login?next=/dashboard'
    ]

    def parse(self, response):
        formdata = {
            'email': settings.EDX_EMAIL,
            'password': settings.EDX_PASSWORD,
        }
        headers = {}
        cookies = response.headers.getlist('Set-Cookie')
        csrf_token = ''
        for cookie in cookies:
            cookie = cookie.decode('utf-8')
            if 'csrf' in cookie:
                csrf_token = cookie.split(';')[0].split('=')[1]
                break
        self.log(csrf_token)
        headers['X-CSRFToken'] = csrf_token
        headers['X-Requested-With'] = 'XMLHttpRequest'
        yield scrapy.FormRequest(
            url='https://courses.edx.org/user_api/v1/account/login_session/',
            method='POST', formdata=formdata, callback=self.parse_login,
            headers=headers
        )

    def parse_login(self, response):
        yield scrapy.Request(
            url='https://courses.edx.org/dashboard',
            callback=self.parse_dashboard
        )
    
    def parse_dashboard(self, response):
        self.log(response.xpath('//title/text()').extract_first())
