import requests
import datetime as dt
from requests.exceptions import HTTPError



# This is a list of user agents that we will cycle through
USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36"
]


def get_VND_data(ticker: str, start_date: str=None, end_date: str=None):
    '''
    Get VNDirect data for a given ticker and date range.
    If start_date and end date are not provided, the function will return data for the current day
    :param ticker: ticker symbol
    :param start_date: start date in YYYY-MM-DD format
    :param end_date: end date in YYYY-MM-DD format
    :return: JSON response
    '''
    # Cycle through the user agents to avoid getting blocked
    for agent in USER_AGENTS:
        headers = {'user-agent': agent}
        API_VNDIRECT = 'https://finfo-api.vndirect.com.vn/v4/stock_prices/'
        if start_date is None or end_date is None:
            query = 'code:' + ticker
            params = {
                "sort": "date",
                "size": 1,
                "page": 1,
                "q": query
            }
        else:
            query = 'code:' + ticker + '~date:gte:' + start_date + '~date:lte:' + end_date
            delta = dt.datetime.strptime(end_date, '%Y-%m-%d') \
                - dt.datetime.strptime(start_date, '%Y-%m-%d')
            params = {
                "sort": "date",
                "size": delta.days + 1,
                "page": 1,
                "q": query
            }
        res = requests.get(API_VNDIRECT, params=params, headers=headers)
        if res.status_code == 200:
            break
        elif res.status_code != 403:
            raise HTTPError('Error code: ' + str(res.status_code))
            
    return res.json()