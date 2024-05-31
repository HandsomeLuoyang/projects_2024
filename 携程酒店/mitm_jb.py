from mitmproxy import http, ctx
import json
import csv

with open('mitm.csv', 'a') as af:
    csv_file = csv.writer(af)
    csv_file.writerow(['name', 'lat', 'lon', 'star'])


class xxx:
    def response(self, flow):
        if flow.request.url.endswith('AjaxHotelList.aspx'):
            print(flow.request.url)
            js = json.loads(flow.response.text)
            for item in js['hotelPositionJSON']:
                if item['star']:
                    item['star'] = item['star'][-1]
                else:
                    item['star'] = ''
                with open('mitm.csv', 'a') as af:
                    csv_file = csv.writer(af)
                    csv_file.writerow([item['name'], item['lat'], item['lon'], item['star']])

addons = [
	xxx() # 类名的加载，也可以定义多个类，然后以数组的形式添加，进行加载
]
