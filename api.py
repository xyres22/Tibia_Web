import requests

def highscores(world,category='experience',voc='all',page=1):
    try:
        url = f'https://api.tibiadata.com/v4/highscores/{world}/{category}/{voc}/{page}'
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data['highscores']['highscore_list']
    except requests.exceptions.RequestException as e:
        return None

     
def world_list():
    try:
        url = 'https://api.tibiadata.com/v4/worlds'
        r = requests.get(url)
        r.raise_for_status()
        data = r.json()
        world_lst = [item['name'] for item in data['worlds']['regular_worlds']]
        return world_lst
    except requests.exceptions.RequestException as e:
        return None



def worlds_table():
    try:
        url = f'https://api.tibiadata.com/v4/worlds'
        r = requests.get(url)
        r.raise_for_status()
        data = r.json()
        return data
    except requests.exceptions.RequestException as e:
        return None

def world_details_api(name):
    try:
        url = f'https://api.tibiadata.com/v4/world/{name}'
        r = requests.get(url)
        r.raise_for_status()
        data = r.json()
        return data['world']
    except requests.exceptions.RequestException as e:
        return None

###########################
def char_details(name):
    try:
        url = f'https://api.tibiadata.com/v4/character/{name}'
        r = requests.get(url)
        data = r.json()
        if data['information']['status']['http_code'] == 200:
            return data['character']
        elif data['information']['status']['http_code'] == 502:
            return ('Invalid status')
    except requests.exceptions.RequestException as e:
        return None


def guild_info(name):
    try:
        url = f'https://api.tibiadata.com/v4/guild/{name}'
        r = requests.get(url)
        data = r.json()
        if data['information']['status']['http_code'] == 200:
            return data['guild']
        elif data['information']['status']['http_code'] == 502:
            return ('Invalid status')
    except requests.exceptions.RequestException as e:
        return None
    
def latest_news():
    try:
        url = f'https://api.tibiadata.com/v4/news/latest'
        r = requests.get(url)
        r.raise_for_status()
        data = r.json()
        new_data = []
        for item in range(8):
            w = data['news'][item]['id']
            url1 = f'https://api.tibiadata.com/v4/news/id/{w}'
            r1 = requests.get(url1)
            data1 = r1.json()
            new_data.append(data1['news']) 
        return new_data
    except requests.exceptions.RequestException as e:
        return None


def latest_newsticker():
    try:
        url = f'https://api.tibiadata.com/v4/news/newsticker'
        r = requests.get(url)
        r.raise_for_status()
        data = r.json()
        new_data = []
        for item in range(3):
            w = data['news'][item]['id']
            url1 = f'https://api.tibiadata.com/v4/news/id/{w}'
            r1 = requests.get(url1)
            data1 = r1.json()
            new_data.append(data1['news']) 
        return new_data
    except requests.exceptions.RequestException as e:
        return None