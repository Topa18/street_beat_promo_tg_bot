from scrapper.headers import HEADERS, create_json_data
from datetime import datetime
import requests


def get_pages_qty(headers: dict, gender: str):
    """Get pages qty

    Args:
        headers (dict): Headers for query
        gender (str): 'man'|'woman'

    Returns:
        Int: Pages quantity for chosen gender
    """

    response = requests.post('https://street-beat.ru/api/catalog/full',
                             headers=headers,
                             json=create_json_data(gender))
    
    pages_qty = response.json().get('catalog').get('pagination').get('lastPage')
    
    return pages_qty


def get_data(headers: dict, gender: str):
    """Get data for all sneakers for sale for chosen gender

    Args:
        headers (dict): Headers for query
        gender (str): 'man'|'woman'

    Returns:
        List: List of dictionaries, that contain sneakers data
    """

    sneakers_for_sale = []

    pages_qty = get_pages_qty(headers, gender)

    for page in range(1, pages_qty + 1):
        json_data = create_json_data(gender, page)

        response = requests.post('https://street-beat.ru/api/catalog/page',
                                 headers=headers,
                                 json=json_data)
        
        data = response.json()

        sneakers_at_page = data.get('catalog').get('listing').get('items')
        
        for item in sneakers_at_page:
            # Сheck if item exists and item for sale
            if item.get('price') and item.get('sizes'):
                rec_price = item.get('price').get('recommended').get('price')
                special_price = item.get('price').get('special').get('price')
            
                if rec_price != special_price:
                    sizes = ""
                    available_sizes = item.get('sizes').get('options')

                    for size in available_sizes:
                        sizes += size.get('grid').get('rus') + '; '

                    item_card = {
                        "url": "https://street-beat.ru" + item.get('url'),
                        "brand": item.get('brand'),
                        "model": item.get('title'),
                        "old_price": rec_price,
                        "new_price" : special_price,
                        "type": item.get('badge').get('text'),
                        "color": item.get('color'),
                        "sizes": sizes 
                    }

                    sneakers_for_sale.append(item_card)

    return sneakers_for_sale


def post_process_data(raw_data):
    procesed_data = []
    stack = []

    for counter, item in enumerate(raw_data):
        if len(stack) < 5:
            stack.append(item)

        if len(stack) == 5:
            procesed_data.append(stack)
            stack = []

        if counter + 1 == len(raw_data) and stack:
            procesed_data.append(stack)
    
    return procesed_data



