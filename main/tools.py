from bs4 import BeautifulSoup
import requests
import pandas as pd
from django.http import JsonResponse
def get_stock_data(request, stock_name):
    url = f'https://www.sharesansar.com/live-trading'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
    }
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')

    table = soup.find('table')
    rows = table.find_all('tr')
    tablehead = rows[0].find_all('th')
    tablehead = [ele.text.strip() for ele in tablehead]
    df = pd.DataFrame(columns=tablehead)
    for row in rows[1:]:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        df = df._append(pd.Series(cols, index=tablehead), ignore_index=True)
    data = {
        'symbol': df[df["Symbol"] == stock_name]['Symbol'].values[0],
        'price': df[df["Symbol"] == stock_name]['LTP'].values[0],
        'change': df[df["Symbol"] == stock_name]['Point Change'].values[0],
        'changepercen': df[df["Symbol"] == stock_name]['% Change'].values[0],
        'open': df[df["Symbol"] == stock_name]['Open'].values[0],
        'high': df[df["Symbol"] == stock_name]['High'].values[0],
        'low': df[df["Symbol"] == stock_name]['Low'].values[0],
        'volume': df[df["Symbol"] == stock_name]['Volume'].values[0],
        'prevclose': df[df["Symbol"] == stock_name]['Prev. Close'].values[0],
    }
    return data
def return_js_names(request):
    url = f'https://www.sharesansar.com/live-trading'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
    }
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')

    table = soup.find('table')
    rows = table.find_all('tr')
    tablehead = rows[0].find_all('th')
    tablehead = [ele.text.strip() for ele in tablehead]
    df = pd.DataFrame(columns=tablehead)
    for row in rows[1:]:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        df = df._append(pd.Series(cols, index=tablehead), ignore_index=True)
    result = df["Symbol"].to_list()
    return JsonResponse(result, safe=False)

def get_index_data(request):
    url = "https://www.sharesansar.com/live-trading"  # Replace this with your actual HTML content
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    indices = soup.find_all('div', class_='mu-list')
    index_data = []
    for index in indices:
        name = index.find('h4').text.strip()
        price = index.find('p', class_='mu-price').text.strip()
        value = index.find('span', class_='mu-value').text.strip()
        percent = index.find('span', class_='mu-percent').text.strip()
        index_data.append({
            'name': name,
            'price': price,
            'value': value,
            'percent': percent
        })
    return JsonResponse(index_data, safe=False)

def get_all_stock_data (request):
    url = f'https://www.sharesansar.com/live-trading'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
    }
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')

    table = soup.find('table')
    rows = table.find_all('tr')
    tablehead = rows[0].find_all('th')
    tablehead = [ele.text.strip() for ele in tablehead]
    df = pd.DataFrame(columns=tablehead)
    for row in rows[1:]:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        df = df._append(pd.Series(cols, index=tablehead), ignore_index=True)

    return JsonResponse(df.to_dict('records'), safe=False)