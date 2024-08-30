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
        self.output_filename = 'target.csv'
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
                link = json_data['sitemapindex']['sitemap'][i]['loc']
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
            item['Store Name'] = 'target'
        except:
            item['Store Name'] = ''
        try:
            item['Product_Brand'] = ''
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

            print('Image Saved...')
        try:
            item['Product_Image_URL'] = ', '.join(product_res.xpath('//picture[@class="styles__FadeInPicture-sc-12vb1rw-0 gGbteH"]/img/@src'))
        except:
            item['Product_Image_URL'] = ''
        try:
            item['Product_Model'] = ''
        except:
            item['Product_Model'] = ''
        try:
            item['Product_Category'] = '/ '.join(product_res.xpath('//div[@class="h-padding-h-default"]//div/span//a/span/text()')).strip()
        except:
            item['Product_Category'] = ''
        try:
            item['Manufacture'] = ''
        except:
            item['Manufacture'] = ''
        try:
            item['Product_Price'] = (product_req.text).split('formatted_current_price')[1].split('$')[1].split('\\')[0]
        except:
            item['Product Price'] = ''
        try:
            item['In_Stock'] = ''
        except:
            item['In_Stock'] = ''
        try:
            TCIN = product_res.xpath('//div/b[contains(text(),"TCIN")]/following-sibling::text()')[1]
        except:
            TCIN = ''


        # url = "https://carts.target.com/web_checkouts/v1/cart_items?field_groups=CART%2CCART_ITEMS%2CSUMMARY&key=9f36aeafbe60771e321a7cc95a78140772ab3e96"
        #
        # payload = json.dumps({
        #     "cart_item": {
        #         "item_channel_id": "10",
        #         "tcin": f"{TCIN}",
        #         "quantity": 1
        #     },
        #     "cart_type": "REGULAR",
        #     "channel_id": "10",
        #     "shopping_context": "DIGITAL"
        # })
        # headers = {
        #     'authority': 'carts.target.com',
        #     'accept': 'application/json',
        #     'accept-language': 'en-US,en;q=0.9',
        #     'content-type': 'application/json',
        #     'cookie': 'TealeafAkaSid=FtAGXgt2qlVfhC_OvdOjKLEoqxFe8XGe; visitorId=0187C0FA97240201B72BF1837179F265; sapphire=1; UserLocation=39500|21.200|72.830|GJ|IN; __gads=ID=41d32e46ab1544ea:T=1682569865:S=ALNI_Ma7InZuNH2cVaVNEb5wlhp2MfW7FQ; fiatsCookie=DSI_3241|DSN_UNC%20Franklin%20St|DSZ_27516; crl8.fpcuid=389dce16-0f54-457b-a348-8bc27164a54d; ffsession={%22sessionHash%22:%2233ef72bcbd5301682653752219%22}; accessToken=eyJraWQiOiJlYXMyIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiJlOTFiNTU4Zi1hNGU5LTQzODQtYjJhNC0wNGVjYjA3ZjUxZGUiLCJpc3MiOiJNSTYiLCJleHAiOjE2ODI3NDAxNTMsImlhdCI6MTY4MjY1Mzc1MywianRpIjoiVEdULjM4NDFkNTBlZjRlMTRkZDhhYmE3NjE4OWExNzgzOGI5LWwiLCJza3kiOiJlYXMyIiwic3V0IjoiRyIsImRpZCI6ImQyNzZhYzNmODE5NTJjMzgzZDQxN2Q1YTk5NzUyM2M3MmNjMmMzN2YyNzM5NjM0NGRkMjM1MjU4NzllMGEzZmEiLCJzY28iOiJlY29tLm5vbmUsb3BlbmlkIiwiY2xpIjoiZWNvbS13ZWItMS4wLjAiLCJhc2wiOiJMIn0.NuoR1dF9xcueoTecDHuZcndD7xERxJbZMC49ZaiFcvlC4wp__kROG4RvAPCJueA4fP24JoVdlzS5cWXh6mxAdFLevh2NkfUR9BIEtDAegw2AmbCEseVHEsd9eCNdTHDoaKUUPCm0W32TvHoU6944khhP1HDjHi-2JezGxE-0Wh8_jI68iLrqrxzOn303cKsURyKfA4kvuIz4zKxGYaSZuCCnHKeCldPI-MtyV94RyPhSjUCbVRdTigHoVLMaIQgi0mRWoH0cnP1jGwV3Ng2Glfq5xcuRNOcuhNG3i_UItrby_aG4b8CPtvkTAqRG0yUHvDhWB5I6s8CbQnzqegRoOQ; idToken=eyJhbGciOiJub25lIn0.eyJzdWIiOiJlOTFiNTU4Zi1hNGU5LTQzODQtYjJhNC0wNGVjYjA3ZjUxZGUiLCJpc3MiOiJNSTYiLCJleHAiOjE2ODI3NDAxNTMsImlhdCI6MTY4MjY1Mzc1MywiYXNzIjoiTCIsInN1dCI6IkciLCJjbGkiOiJlY29tLXdlYi0xLjAuMCIsInBybyI6eyJmbiI6bnVsbCwiZW0iOm51bGwsInBoIjpmYWxzZSwibGVkIjpudWxsLCJsdHkiOmZhbHNlfX0.; refreshToken=H3dM0YJYT4cE15mbqxaWXeUraga2XJvJCEsFIkj_5xnDRBJkaHuZ_mTppPJazhQG68WtAdA6fJUYVqgmEQvSEA; __gpi=UID=00000bfe0f38f9bd:T=1682569865:RT=1682653753:S=ALNI_MaAFl7XRgu3bgIzPbzzWlrFZRqcJQ; ci_pixmgr=other; 3YCzT93n=A9r1mMaHAQAAv6LKoRdNkTFha0WpTO4pejwOPopGMK7qd5V7JVZtiQMk5mcoAXqiBNuuchZ2wH8AAEB3AAAAAA|1|1|b11c555bc66e450c0f6c169476992bffece924b1; TealeafAkaSid=FtAGXgt2qlVfhC_OvdOjKLEoqxFe8XGe',
        #     'origin': 'https://www.target.com',
        #     'referer': f'https://www.target.com/p/girls-disney-the-little-mermaid-bike-shorts-disney-store/-/A-{pro_id}?preselect={TCIN}',
        #     'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        #     'sec-ch-ua-mobile': '?0',
        #     'sec-ch-ua-platform': '"Windows"',
        #     'sec-fetch-dest': 'empty',
        #     'sec-fetch-mode': 'cors',
        #     'sec-fetch-site': 'same-site',
        #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        #     'x-application-name': 'web',
        #     'x-gyjwza5z-a': '8OyXVxpQvZilD-YesQoJpgkVn=GI9i6GpNtLjWUw=J7nysahDb2ur6UE-qAqHaV4x64msK2tjCs-HV3ndyMWBVcwTBZHnjwW08-kjZf6VBS4cpk29xmuhAxw9pU3Ds5szrSouiYbq0Lj3cqAM-pRcSMjJ8F1-EA_EyrbgJes7WyvWmkJuD9EBtMw2kJtm_rv0rE_1ATj5rZ-kIop3pB3FWjJ48J5qCQ4RlKsb2=62S_9gnv8GcRkGUCLwclYsxUQKEnNGCtzNODd1A-zex=M0DouGff=QxL8-SxBXEVsUjxdmJ7qW66ApSQWX0wRAVyn45CnFX-ZCKDl=F1TV7_4vmJteEaq_nCpCSoc00jzCSGtlQkQNEtXZF_GFWr357W0=hOQU4IZINoUhoDMm8ceQZHvu1KI6nkerfiGx6btZGSFdne=BM7GTKedesdSqR5bnuCi-ECaK60g5VW9Illi=1nqqSvcbSWqhWsGATnZZow=Z0rXJXWlMgxgq8xNmBp4IqYyzi=bNJTm03GhjualB49zuF0=A4MrTgdTpdj9222sqb08TiCVJiGZqdJj79EIZUxkMD8OjUrlA0tMd24gzjnqk4mU3qGF19UrU5c_x1Co4=gINnASHDvBOXQN5Dk4wgQ81XXU3B-56dMUGo=MBxXAGIxbifDixZLJdWM7vwGrBQGtpks-IOMtXEH4_AEDih828zcx=X90K9xF_5OIss5tDHVjjyX7idThgXQXAYId5W6y=8hVz2Fli07Mhx5MlA=5Kk4l-4WokuuMD1CplLnz-iQLd3iq2i1z20_453Ssg-co2t2BruOG74vfg=Bu5cxugid2wFy5ax1nI2C30phkXvp3HitN1UCDx5tuafA67fmfANNibUZq2_SGtKL=Ak-AStHvLkZwCFCtCJqtVvSsIL0-ivCiYoqNWqL4p7uvjB2jK9vN8_-hCX1r253pqprYpr82pYACze16_oSO2wahtRY2oDs3CJwivYaZ4RWHpuJeMrdQ4SEe_Sc1YnFBt482z9xfbrwg25n5AIJD3o801QE=uVh7u3aGezsianVZL7IfYzrmgdkx1LE44=nHTYJ3v2E6oeIMhF=iLccVMt-AA=0F3W9ZKF2nsCJd48T5m3jfUFl=YT9zZH5=vW7Vls0bC60bMYNlJFNUxU-lMaZXiEbTFQKlmexlNftVnK_GxyeTrwFRB6iOhah5vfAi53tRUUN5invRMZoVGZ16tZ2OFH3NzCBXTMqodmK7izz1bLW1Kj4V7fOyetYI1uULODNb1ZSyza_38f0bS7nLczjseYMH7EGmOiSIbIk4DepHAe-_7MFsx0xrXTVu1XTFdfXGokWG-rvKNluM-sOAVudLdy6dg=fB5OZBqhesRQ5FwHE_nAgt90gQH636JUcf6phBMy-1JIJ7u0NvcuGZkS9ch=xk4nnngo745WCzqQqgVEN916huM5J=__whEUcTp4kdnnh_E60VDd5hpzMB813ertW9ToCOp5pUjAKzIm1bWbUGe4CWAX2K4HNhV1JkQWvn0=mz5wsorGo382I-wwChNvljnwJhIXeAxBCtgZ3osnOvIEgIyjp3Wnwe8l2DyachitVmhILE-WGl7_Gfg61AH5tGt0AxkJ41NTpb0ncfvlcs2ru29r0oiiYrB_2sjtOHGA7zRehNUVWar4h6Ytpl9rOlV6i=prC2hIka2uwX6qq4JvEb9ao1TxQ3tlHRMBXxOkSvjwJTzs40k5o2iS1iRcZz9h1WegxcnuANZE7HVe5409N5wZeVfxwSQYtVv1O=MC2cVvFAWj24-H-5cmmx=duaVaZACMohU=FYRB7AEj_5q4mr-QDmmdNwQqigBv1NjAyKchp7Tls9bzytNpu3uVMIHIfDHcVwUUqUokLsUOs_OVFGc2SkAll11MZsMz50XLz8bjIH2q113ND-DTrsdez-wZGY-1W1sF9qcpe8EZ9pWTl48J_DtVx6uB1j47BLBZyXxjQJY-zmd8Fh=fu4jxNUoFXCzTUbt=u=UsMet8G7S3hfF=ALRs0tX3eQ97cO1LoMNUvk9yb2RRhA1Cx45Eqhi8JdIQvqYL6uiuekBsx_5lBh1_mqAgxmn1ugvtkiUE08mchV2XH4Q0EC6fchaLHdtB1bh-HeDiskM2FkdS=tOWSV5yx0-C5kqGEM4BzU5ipyKB9gzTZW4_r3y7McgRMv1DXpxAEZZa8hxYDHceVYS9wdeYNbY=rOg7WOaeKcAKjGYV1DCZcfCNdA-0k-M5eBo1XtBRoS=yqWjpXu-Lfou22GzZRgK8MNcQ_6QJsGAz5rd2=xRlm2Riev_BQOOL5IE9yWkCfdKTT1f11WgohXEUHH2t68fDxFK9cAhBMkD5yH7jxRbxxBVQiqUwZDtbY_laSHtxthmz9upEEusR7EQk2fjzzL0D3Vk_VQMhwxWHaNpeTUfgogw5WRce3jcdVKu_4zzLjNvosl39Wfwlu743RYpCvLUzGeBlMWlWZQL9WuzmAkOk7QhF34H_Ri8cer-MeVazV7u5TvNbbOnbwbFXmS_5J=ASptFHHfNto1wge4UGCLtwf4TLq_9nqYaOHD-70SUEL7-Ec6Ezk1cm8dO8SvQrlS_gZh-W6066QalU7tLSIzDH7b74mZCG_-ticldOgyz3IqMN3mRnR2oxvg2DC1cObkE71BmnVwkwKVlAK=U54c9iI=YS9KzFGf=DE-fop=Qu2aMMJcLJTCff9LYdQJr4dsK-aJS84i36rR5Fqg=H3g7Vh5D=Bo68d-grjadx6tn=fDgT19Ji6VeALDbHAfIg=Mda7qopLpGjQ4ghRaN_K_kwxwdK-T-uijNbsr9uGUUiB46KFa1nM4vb-8Nm_9=CFKAuSiQQzze=6tRjUJp8HQu_ZvoYyjL0cEHkzYpYHm=FaTgI0eEYcny63gwRnO82yRzRaVbnRNn=0HKVNp5jNlXpIcsjEtNf3xpHVY3BIRS8=5LbVqcCxshU=L8Sv1=D-9=tg6W5x6cJ12HOMY8tfr5FUMQc=mRBwtDZ99fyjEkNkM2Ye1nw2ia9MndGTFD-rnN-Aij4wEJ3bfzGbo2wsDQ91Oz_t3DmdaZ5vbE1njSwKp19DnIg1HkUVBUqwIwpj55o7aNkyQ8AlsUzF-S=ieiJCQEUbMQ2Qh59XLI8TRZhTn75NFfgV56pu3fQypOWNjKIeM_68_OExcXcJuymyJIIM46_QaE-tDYBb2bE6-6Q3hy5bfHY_K_I-1R-LgaQ=Go=LUd6TXQ-0bTyDv5hweA09Mowngy5sC4mDCx5S0l0bV2g1pOssBgGJuVWT_YKralA6s_VmIu48vxjzOWzuVrlB6Es4QxUE5XbnijdfslSOYEcDuXdALNlL-vnrozkYwKDdDUefHLKy88XpshGxV1AqgXYYisLEw63KQzyrL_0IufBpL0ucU1q-n_yF52q5KpK3d4cUQyGikJhyJTwwOmpzSb4cG25CjxLJaXasu=B-Eu-c=8DD8ruAGiL36G8oVn8ILyfR2ZdsEhYa_U8=xxeZC3EUL=lEEeMZoA8lWOgtQYXtSzfSyg4nC5cAGxzCryWJ2ypa7m95Nh1Twko2TzniFc_Tk00B6lA8-bgbUs9mkUhQ2ynT18kHpVp5MuzQ1fE5KT6Zjgj22wku_e17i4O-Jy45rG306jGWjnwe3-shfIMT8QCAIlLgbEb5AqCsua_5i09AWRj4TtXGRU29ys6dzQjnuqyvwTr-HoCXcoY8U225yE6qOKQnOKXKdA-F8Yowqvh2ggbd4WJ46D_Qdj=QTU3p3I-LG1WaeB=eG2bLzqVptpYg5FELS0eeHWO6Ge2dzAMUaYgTZFGcxLCjYVJtXTA_azjMNrJNurwUuZjIWcdt9a=3m5a4Wvzgbn=rf8AR=OdiSVZxeRSoEI1k5Cho8HXzkn8EjriJ3LVFNpvRtG6ycm_-FqpkjkTl08pvhN4-x-6-QUqwMuoJX9XHtcR4ziBNMeE9NrbgtBmB88uwj_lAh59Bp96dk63SaFTA54cshGRY-LcKGpdQZc4Sr6Vlr=p=vSvO2uCpOZ6-5U4LWp1mh6=Z3NReflWfW__6rOSyKLWkH7DMK=Vc28VWDBRblEKylXS_k5YfWqT=D0aya4V0J9szkGSL0DAiG7QezuASaJDTum-N1OBV0hb0Z9wWTb0jwRN5T36Yba_G0jXkjnFnjaLnvZAEQuyNxB0jv8OFo1NDfZ3yJFy9_g1C0KYKT-IiiZiylfJLODkzOAp=12gxLFs9cVw_rwXbvCn3IlaLgjVcU1y3i_gQbwxestkyZbxf=4o-Q=FDW9J3ztuWtnmQkB4iF43_D1BhSKXwsUfNeV-kV=Ub7398J8pU1F3nIBmxFK_C54TceJBGMnQCo0xF8-n6FX0SYlHVv86VBoBq-ayBpJ0U3ZDueLD6_xk4M0WszdXW2SRQixLE=UkwNRuIJVUiRBDDJ9Tx7EOnxxlIHi62TH=_Z_nZDuGfuZEnsy==bSJq9CQGg9oWAhI-5g5UIOvucybxVNcW4G-k=iK8vfNLZ8iJVkY-nK_r_rOIe29r2AaonZtgLE50C8dgsxy2TdI61tykYIGBNByqj0s4gZFW53mxOHG7uuDaOKsYqv4puEtJG42UveRAH1sIe6uB22=Dob5dRNJFBNyIOMZ0vhakbIgR19w2DpICxMd26LcLmtaprdiv7KjHAXrvBCFf7mC8014RRy4i_erSnrJs9pw6kT51-ikJa9=lfgm91xsU=T1fW6GulD4uRvj1kwGAitW6efDXqKSy7uGVIkSA5fW1tWGpvEcN2B4yXjhRnXb9Ns7K3CqmXH86v-IAOA1dSR6J2y3vOqzXr1xYVnBFuO1ajqbJ9ibU8Uc435GBTaDRgWn17-XGzhqxe4J_Qg_btk=oTNbTWexvA0=qxuTz=ZA4CuqC3RXtwk4efSq1A_k39opYkN_gi9d5uN_onAd5WH2iZkDILr18-wjj6AdtE-Sqbnb52ha1DfVD4vMhbSu9kzbZ7H2SdVyjM1yEBwrFAetXj-06BWo2a=mekCaGMQARQC9rw7Gh-hLIopLAqKkJRKF3qkRejf7F_UnYoM1zEJeRnca4e8ZfVJAEO7YBoor_kiMzTIRt856JUKRN=qseC85xCU9DkA_AZE38ZiaWD5YY2KeBLBzONbMgDfHA3M3OCZDgzUCaLIV6j_RN6ZloBuWfJwm7UA8RmT5vqFppvImCEHvLEuiIqWwb=aCWgANYJDam0FcMjmxKZCr_IvyF2nsgB3VqB6nC8whF38-NqT_cgh=_IAbAXYcvlnTWZpENWYl7UrWT0wfccInkdJQ8HDC-T-MEGqc4uvFlrZ_fT60p-AJNQ-24Wjs3xokL0nqr7fA9fcdiaRAGaUIzkwJWAdaOcK3TOE24cZYOOfS9WthkUIN=-Xl45ksfCJ8HzR-hwgCM1Gevts5fYjZj-KQxyBBvGknzJoo-W9YxHyFHlm5r7ATrsCY5uS0IMTIpapFK90sayF2Jplj4tjM3Bsc84ZGWxSx2CXlFSVm2Yz_vHA-iFvCrGmlSdNk9EM9t_23Svmq99EC0_ZeVawaG5MCeWq0Ic16YiSwzrZYr8a1fAWVL6ZJGGjNg3Irh8G3CTV1bTO-3rDOSB2nQNl9x5rdT=c=9Lz=R_xTibd6rx3cGElW-R4GN1lRo=WW-J6aI-Z5cIInOyMAbDyMv2d8xXYvKmhaIKZ7U=dl36uw7Uf1YKFdGAcXvLM=ZjIbGV_QLc=DekB5lypUBtO5nWv5pd5Tsh8LjCpYz7AdmBl7GpQT41o09pLr-CIclvlR4S69=rYmcebB0Ei4XArRjZeZnldUVlx7194bWS5NQ5lcWmRNTf4LpYkQYdvbjbya4_LOE3SE_qeW3u-ULTWUfos-rLLGES9QrEcLgVzhCrhezZwZ-DCCt==UTpw3u6SUlw=L5ejCMYab4rXqnBTFq5T9-nS8smSB2YKnA66vx39wafZxyMFFJFZFTiSYzBOL93AqekhJlNHMN-y0TvfZC3ws5eCRpnSDvmWw=uyWR_Z4kQ9FYIkK-1ukMJqQh_hrJcG_kzZUWuylGJlhm5B1ToLHDe5Mw6YDcKhLH9A0oGY9uOZNrWFqVA-V2OG7ot59srQ3U1iY1fG5uhMpjcaKa3Xfgic47iv4BWo4KHLqz3324ruD5MyvKh_uAkfGLB5nCVOnwRqNrK-0ELwz1Z64fgLWsdHsjL5B89ZAosH23=QwI3HeIa98iObeIeOX6ZLDsQFY=8yweTweLHzjr9ZuC1EuuU=ZuD2hySvRrvqDWmNxlYUSIC-86wRJdWsHcn8S7La_0lxzHVedsKSwmgYZH3SppsIWOJKp8usLxJGCg_EDfB4sbqduK9STE6102J6i-S7ISm3zjlxeoyAuuK-WZJOv7=ZYEdBw0jL7y2dQ2UG3LF56xlcJ0dkgNyOdFuMMAiYmMEQw3rgCBQ2V1tbzA=44iOhKBRgUbwV3kd1gcLi6Syko_5NpnkW1xOqpsa9B6tKvIWFtEb=AircyoSE9CV1R0cDx3Xv7tSMZgiaSOynajDGSWbDW894vt=Dhc1t3Ub1Of2uQzpLnK2cTfvWwnwEaU5YOOsAZqlGJaFZJFXRWk9YRSG1wRmuDY83vWdzzl4EQzS9w=FUEnSNr=kUA7W_LEqxYV15dwu80Si4R6arxrnuLOvmrOctifq_psbGmWGCC5UH6gO11nEkDwdjpHZAQGStl=_RgzIkj1ggiau8wfk2GomLJOAZ6NZADpqEDi1Q8Oc5TthaLzGEpakLqRRBv39A8C4uajRUF=ZRwrA29_bh4nWvm86hF3g9vcugSbYeNUfaoWjgNGySSFLhk=G4s5-yargs1ZBnxO5SEz8YlUzr0L3HQsKx=a_geuDYXOFNlnCY9Q2TC5jNKSRrtRlh9kBOUM9R89VI7UYI47dUOJu32JMbjEUbzhxFt8di0vmDIm1VFXKYySK7qMm6NXLyoQfMrZEWKUwi=WDu8FIAm8qmp1GuHrq=SxrxI23yq9X3fYMy=MuHdA5CXx4ZN3F=htTGNiYzmd_ZjwV9pIXDDFUqN9vokOrZ6t9Ygzfotxhw1TmOGIlJpNUJUNAYsGboFg6_jOeehecX6L4QHI2anWk6LpUyqQnZtvqHsasngdwKNJ=pTIlkx3w-bKI66ICnliOyIacIfJpmGtp=ru0xuGtzOJ5uYXqQXfe4Vuc_FCI=grB06H0=KScJQQo2yTtkYuWVUB5-9346kV2ZI1ZNHpCZFydM=g1hgBKH8AxEkeR3lt7w_n8HcqkKKq_rCyvHAhdNfvTLVxVihq_6stKUxjRN=t3hx2tce7W031SrKmveGK4L2sX7Yjk5bX6gc5i1lxop=ODgfzcrVOStGZgrLSNCftDYTqOhWYr',
        #     'x-gyjwza5z-b': 'iu80rw',
        #     'x-gyjwza5z-c': 'AEC_-8aHAQAAX1y9df1lwfB0g5Xe0z42odQBK7jMVhbq8k3iPAJhC1uYHtAU',
        #     'x-gyjwza5z-d': 'ABaAhIjBCKHFgQGAAYIQgISi0aIA5JmBzvpjzz8AAmELW5ge0BT_____5gVpjQDMYEKnibGODHpfnIdkGJxj',
        #     'x-gyjwza5z-f': 'A9knF8eHAQAAH-dH3FsByOcKWXHeixh7eSdJtsD7qiB2EoE_g2DIbXVwwNJvAXqiBNuuchZ2wH8AAEB3AAAAAA==',
        #     'x-gyjwza5z-z': 'q'
        # }
        #
        # response = requests.request("POST", url, headers=headers, data=payload)
        # try:
        #     stock = re.findall('{"availability_status":"(.*?)",',response.text)[0]
        # except:
        #     stock = ''
        # if 'IN_STOCK' in stock:
        #     item['In_Stock'] = 'Yes'
        # else:
        #     item['In_Stock'] = 'No'

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
