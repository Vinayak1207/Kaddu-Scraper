import scrapy


class QuotesSpider(scrapy.Spider):
    name = "kaddu"


    def start_requests(self):

        with open('links.txt') as f:
            urls = f.read().splitlines()


        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)




    def parse(self, response):

        Name = response.css('body > div.wrapper > div.wrap1200 > div.wrap940 > div.wrap700 > div > h1 > span::text').extract_first()

        if Name is not None:
            print("damnn")
            #for Nutrient values
            a=[]
            i=0
            table = response.css("#tab-content > div.nut-value > div > table")
            rows = table.css("tr")
            for row in rows:
                col = row.css("td")
                d={}
                for td in col:
                    if(i==0):
                        d['Attr name'] = td.xpath(".//text()").extract_first();
                        i+=1
                    elif(i==1):
                        d['Weight'] = td.xpath(".//text()").extract_first();
                        i+=1
                    elif(i==2):
                        d['perc daily value'] = td.xpath(".//text()").extract_first();
                        i=0
                if(d['Attr name'] not in ('Details','QUICK FACTS','AVOID TOO MUCH','GET ENOUGH')):
                   a.append(d)


            #Ingredients
            b = response.css("#tab-content > div.ingredient > p:nth-child(1)::text").extract()
            c=""

            for x in b:
                if x.endswith('("'):
                    x = x[:-2];
                if x.startswith('")'):
                    x = x[2:];
                c += x + "-"




            yield {
            'Name':response.css('body > div.wrapper > div.wrap1200 > div.wrap940 > div.wrap700 > div > h1 > span::text').extract_first(),
            'Callories per serve':response.css('body > div.wrapper > div.wrap1200 > div.wrap940 > div.wrap700 > div > div.prod-info > div.data > ul > li:nth-child(1) > span::text').extract_first(),
            "Serving Size":response.css("body > div.wrapper > div.wrap1200 > div.wrap940 > div.wrap700 > div > div.prod-info > div.data > ul > li:nth-child(2) > span::text").extract_first(),
            "Jogging require to burn":response.css("body > div.wrapper > div.wrap1200 > div.wrap940 > div.wrap700 > div > div.prod-info > div.data > ul > li:nth-child(3) > span::text").extract_first(),
             "Details":a,
             "Ingredients":c


            }
