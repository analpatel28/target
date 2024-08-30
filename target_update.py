import datetime
import json
import os.path
import re
import urllib
from datetime import datetime
import pandas as pd
import requests
from lxml import html
from lxml import html
from pathlib import Path
import xmltodict as xmltodict

class Target:
    def __init__(self):
        self.products_count = 1
        self.output_filename = 'target_sample1.csv'
        self.headers = {
            'authority': 'www.target.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'cookie': 'TealeafAkaSid=FtAGXgt2qlVfhC_OvdOjKLEoqxFe8XGe; visitorId=0187C0FA97240201B72BF1837179F265; sapphire=1; GuestLocation=395003|21.200|72.830|GJ|IN; UserLocation=39500|21.200|72.830|GJ|IN; ffsession={%22sessionHash%22:%22a2da77644dacc1682569863163%22}; egsSessionId=bebb123b-dc0a-4731-b7e3-9e8af3927d77; accessToken=eyJraWQiOiJlYXMyIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiJlOTFiNTU4Zi1hNGU5LTQzODQtYjJhNC0wNGVjYjA3ZjUxZGUiLCJpc3MiOiJNSTYiLCJleHAiOjE2ODI2NTYyNjUsImlhdCI6MTY4MjU2OTg2NSwianRpIjoiVEdULjAyYzcwZGYzYjU2NzQ2MDNhZjhkNjk4OTlkY2E5YmRlLWwiLCJza3kiOiJlYXMyIiwic3V0IjoiRyIsImRpZCI6ImQyNzZhYzNmODE5NTJjMzgzZDQxN2Q1YTk5NzUyM2M3MmNjMmMzN2YyNzM5NjM0NGRkMjM1MjU4NzllMGEzZmEiLCJzY28iOiJlY29tLm5vbmUsb3BlbmlkIiwiY2xpIjoiZWNvbS13ZWItMS4wLjAiLCJhc2wiOiJMIn0.cF5Vb0rOHGxxv6pLqIEfclcG5q7PtNtfnm-H6yU4iDRnGjpgAjgmr1daBS47Iegc09wAzUJrSoAAnErW1Ct10jBlBKfSr8uFUM3sJtjorYsn20El7HdeiTTXt6aRAQ6CR0lvn8hWgIU-BrDUK3nLXi7p4-bvZawo3ktEVxxlXvQ6uGFiFmr6jD-aeBcgetGEN-aOteAky_P1_PqH8bSbsv-Bdyy-i5LMKCW4h3R39RD8gR_Dt2jqmbatpLJYxvoO_eq18Na1FGmsY7DuPwZ7jRGiBvb0NT7vgMnE1HoivHDvGlS7SJnILKd6q3nSXanurSLlJmNI8QgLyoauQx8mHg; idToken=eyJhbGciOiJub25lIn0.eyJzdWIiOiJlOTFiNTU4Zi1hNGU5LTQzODQtYjJhNC0wNGVjYjA3ZjUxZGUiLCJpc3MiOiJNSTYiLCJleHAiOjE2ODI2NTYyNjUsImlhdCI6MTY4MjU2OTg2NSwiYXNzIjoiTCIsInN1dCI6IkciLCJjbGkiOiJlY29tLXdlYi0xLjAuMCIsInBybyI6eyJmbiI6bnVsbCwiZW0iOm51bGwsInBoIjpmYWxzZSwibGVkIjpudWxsLCJsdHkiOmZhbHNlfX0.; refreshToken=fLut8YcG7KuWJm4oJJxZC5jF8HaV68aKeo_vszkrJyFC1GSSFI3VjLxQ9fT3UnbXc9UFY5je83Hl8sSRRQHo9w; __gads=ID=41d32e46ab1544ea:T=1682569865:S=ALNI_Ma7InZuNH2cVaVNEb5wlhp2MfW7FQ; __gpi=UID=00000bfe0f38f9bd:T=1682569865:RT=1682569865:S=ALNI_MaAFl7XRgu3bgIzPbzzWlrFZRqcJQ; mdLogger=false; kampyle_userid=cfc8-da89-1a34-9d05-5a86-6228-ba41-046d; kampyleUserSession=1682569866275; kampyleUserSessionsCount=1; fiatsCookie=DSI_3241|DSN_UNC%20Franklin%20St|DSZ_27516; crl8.fpcuid=389dce16-0f54-457b-a348-8bc27164a54d; salsify_session_id=7f6e7794-b961-49d5-9490-bba68aad118f; dteRfWys=6kGx1B4U; kampyleSessionPageCounter=27',
            'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        }

        self.current_path = os.path.dirname(os.path.realpath(__file__))
        self.img_file_path = self.current_path + f'/Images/'
        if not os.path.exists(self.img_file_path):
            os.makedirs(self.img_file_path)

        self.base = 'www.target.com'
        self.Target_main()

    def Target_main(self):
        URL = "https://www.target.com/sitemap_index.xml.gz"
        response = requests.get(URL)
        data_dict = xmltodict.parse(response.text)
        json_data = json.dumps(data_dict)
        json_data = json.loads(json_data)
        try:
            ttl = json_data['sitemapindex']['sitemap']

        except:
            ttl = ''
        for i in range(len(ttl)):
            try:
                # link = json_data['sitemapindex']['sitemap'][i]['loc']
                link = 'https://www.target.com/p/sitemap_005.xml.gz'
            except:
                link = ''
            link_req = requests.get(link)
            data_dict = xmltodict.parse(link_req.text)
            json_data = json.dumps(data_dict)
            json_data = json.loads(json_data)
            try:
                data = json_data['urlset']['url']
            except:
                data = ''
            for k in data:
                product_link = k['loc']
                # product_link = 'https://www.target.com/p/boys-39-mickey-mouse-americana-graphic-t-shirt-off-white/-/A-88345334?preselect=88308059#lnk=sametab'
                product_req = requests.get(product_link, headers=self.headers)
                product_res = html.fromstring(product_req.text)

                try:
                    variant = product_res.xpath('//a[@class="BaseButton-sc-j0jbcc-0 BaseButtonSelector__StyledBaseButton-sc-dijc6i-0 dIJYmd bcAJIX ButtonSelectorImage-sc-18tvdw-0 doXEwD"]')
                except:
                    variant = ''
                if not variant:
                    try:
                        variant = product_res.xpath('//a[@class="BaseButton-sc-j0jbcc-0 BaseButtonSelector__StyledBaseButton-sc-dijc6i-0 dIJYmd bcAJIX ButtonSelectorLabel-sc-1j00i2s-0 cTwARz"]')
                    except:
                        variant = ''
                if variant:
                    for i in variant:
                        try:
                            product_link = 'https://www.target.com' + i.xpath('./@href')[0]
                        except:
                            product_link = ''
                        self.product_data(product_link)
                else:
                    self.product_data(product_link)

    def product_data(self,product_link):
        product_req = requests.get(product_link,headers=self.headers)
        product_res = html.fromstring(product_req.text)
        try:
            pro_id = product_link.split('/A-')[1]
        except:
            pro_id = ''
        item = {}
        now = datetime.now()
        try:
            item['Scrape_Date'] = now.strftime("%d-%m-%Y")
        except:
            item['Scrape_Date'] = ''
        try:
            item['Scrape_Time'] = now.strftime("%H:%M:%S %p")
        except:
            item['Scrape_Time'] = ''
        try:
            item['Store Name'] = 'Target'
        except:
            item['Store Name'] = ''
        try:
            item['Product_Brand'] = product_res.xpath('//a[@data-test="shopAllBrandLink"]/span/text()')[1]
        except:
            item['Product_Brand'] = ''
        try:
            item['Product_Name'] = product_res.xpath('//h1[@class="Heading__StyledHeading-sc-1ihrzmk-0 jmSnUp h-text-bold h-margin-b-tight"]/text()')[0]
        except:
            item['Product_Name'] = ''
        try:
            item['Product_URL'] = product_link
        except:
            item['Product_URL'] = ''
        try:
            item['Product_Image'] = ''
        except:
            item['Product_Image'] = ''
        try:
            item['Product_Image_URL'] = ', '.join(product_res.xpath('//picture[@class="styles__FadeInPicture-sc-12vb1rw-0 gGbteH"]/img/@src'))
        except:
            item['Product_Image_URL'] = ''
        try:
            item['Product_UPC'] = product_res.xpath('//div/b[contains(text(),"UPC")]/following-sibling::text()')[1]
        except:
            item['Product_UPC'] = ''
        upc = item['Product_UPC']
        img_count = 1
        try:
            images = product_res.xpath('//div[@class="AspectRatio__AspectRatioChildren-sc-1c5hpa0-1 dRDFXG"]/div//img')
        except:
            images = ''
        for j in images:
            img = j.xpath('./@src')[0]
            filename = Path(f'{self.img_file_path}/{upc}_{img_count}.jpg')
            with urllib.request.urlopen(img) as url_response:
                with open(filename, 'wb') as img_file:
                    img_file.write(url_response.read())
                    img_count += 1

            # print('Image Saved...')


        try:
            item['Product_Category'] = '/ '.join(product_res.xpath('//div[@class="h-padding-h-default"]//div/span//a/span/text()')).strip()
        except:
            item['Product_Category'] = ''
        try:
            item['Product_Model'] = ''
        except:
            item['Product_Model'] = ''
        try:
            item['Manufacture'] = ''
        except:
            item['Manufacture'] = ''
        # try:
        #     item['Product_Price'] = (product_req.text).split('formatted_current_price'c\
        #         ]'; 234[1].split('$')[1].split('\\')[0]
        # except:
        #     item['Product Price'] = ''
        try:
            item['In_Stock'] = ''
        except:
            item['In_Stock'] = ''
        try:
            TCIN = product_res.xpath('//div/b[contains(text(),"TCIN")]/following-sibling::text()')[1]
        except:
            TCIN = ''



        print(item)
        print(self.products_count)
        self.products_count += 1

        df = pd.DataFrame([item])
        if os.path.exists(self.output_filename):
            df.to_csv(self.output_filename, mode='a', index=False, header=False)
        else:
            df.to_csv(self.output_filename, mode='a', index=False, header=True)


if __name__ == '__main__':
    Target()
