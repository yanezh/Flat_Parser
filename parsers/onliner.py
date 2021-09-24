import requests


class OnlinerParser:

    @staticmethod
    def parse(url, first_page=True):
        flats = []
        print(f"Get: {url}")
        response = requests.get(url)
        data_json = response.json()
        for flat in data_json['apartments']:
            flat_dict = {'id': 'onliner_' + str(flat['id']),
                         'address': flat['location']['address'],
                         'url': flat['url'],
                         'price_usd': float(flat['price']['amount']),
                         'last_update': flat['last_time_up'],
                         'photo': flat['photo']}
            flats.append(flat_dict)
        if first_page and data_json['page']['last'] > 1:
            for i in range(2, data_json['page']['last']):
                flats_new = OnlinerParser.parse(url.replace('page=1', 'page=%d' % i), first_page=False)
                flats.extend(flats_new)
        return flats
