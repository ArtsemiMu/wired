import scrapy


class WiredSpider(scrapy.Spider):
    name = "wired_spider"
    allowed_domains = ["www.wired.com"]
    start_urls = ["https://www.wired.com/sitemap.xml"]
    article_count = 0
    max_articles = 10

    def parse(self, response):
        namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        sitemap_urls = response.xpath('//ns:loc/text()', namespaces=namespace).getall()

        for sitemap_url in sitemap_urls:
            if self.article_count >= self.max_articles:
                break
            yield scrapy.Request(sitemap_url, callback=self.parse_sitemap)
        
    def parse_sitemap(self, response):
        namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        
        article_urls = response.xpath('//ns:loc/text()', namespaces=namespace).getall()

        for article_url in article_urls:
            if self.article_count >= self.max_articles:
                break
            yield scrapy.Request(article_url, callback=self.parse_article)

    def parse_article(self, response):
        if self.article_count >= self.max_articles:
            return
        
        headline = response.xpath('//h1/text()').get()
        article_html = response.xpath('//article').get()

        self.article_count += 1
        yield {
            "headline": headline,
            "article_html": article_html,
            "url": response.url
        }