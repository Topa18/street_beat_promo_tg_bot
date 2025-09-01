def create_json_data(gender: str, page=1):
    json_data = {
        'pagination': {
            'page': int(f'{page}'),
        },
        'sorting': {
            'key': 'sort',
            'value': 'desc',
        },
        'seo': {
            'uri': f'/cat/{gender}/obuv/krossovki/?page={page}',
        },
        'search': '',
    }

    return json_data


HEADERS = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ru,en;q=0.9',
        'content-type': 'application/json; charset=UTF-8',
        'origin': 'https://street-beat.ru',
        'priority': 'u=1, i',
        'sec-ch-ua': '"Chromium";v="124", "YaBrowser";v="24.6", "Not-A.Brand";v="99", "Yowser";v="2.5"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 YaBrowser/24.6.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

