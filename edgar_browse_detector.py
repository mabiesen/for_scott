import requests
import bs4
import json
from urllib.parse import urlparse
from datetime import datetime

# For clarity breaking this URL into pieces
# SOME_CIK of query string will be used for interpolation
PRIMARY_URL = 'https://www.sec.gov/'
QUERY_STRING = 'cgi-bin/browse-edgar?CIK=SOME_CIK&owner=exclude'

CIKS = {'churchill_capital_corp_iv': '1811210'}

def build_url(cik):
    query = QUERY_STRING.replace("SOME_CIK",cik)
    return PRIMARY_URL + query 

# this is fetching the raw html
def get_html_for_url(url):
  result = requests.get(url)
  result.raise_for_status()
  return result.text #we dont need the result status detail, just html

# parsing html for table in question, getting rows, td elements
# iterating td elements and putting into array, returning array
def get_table_rows_from_html(html, table_class_name='tableFile2'):
  return_arr = []
  headers = ['filings','format','description','filed_eff','film_number']
  exampleSoup = bs4.BeautifulSoup(html, features="html.parser")
  table_element = exampleSoup.find("table",{"class": table_class_name})
  trs = table_element.find_all("tr")
  for tr in trs:
      ctr = 0
      temp_hsh = {}
      tds = tr.find_all("td")
      for td in tds:
          temp_hsh[headers[ctr]] = td.get_text().strip() # clean whitespace
          ctr += 1
      return_arr.append(temp_hsh)
  return return_arr

# first run no cache will exist for company
# we will handle the error using try/except
def read_cache(company):
    ret_arr = []
    try: 
        with open(company + '.json', 'r') as readfile:
            ret_arr = json.load(readfile)
        return ret_arr
    except:
        return ret_arr

def write_to_cache(company, all_items):
    with open(company + '.json', 'w') as writefile:
        json.dump(all_items, writefile)

def diff_arrays_of_hashes(new_arr, old_arr):
    diff = []
    for item in new_arr:
        if not item in old_arr:
            diff.append(item)
    return diff

def alert(company, cache_diff):
    print("A Change Was detected!!!")
    print("This might be the first time we evaluated this company, this could be a false positive")
    print("Printing Each New Item:")
    for item in cache_diff:
        print(item)
        print("")

# THIS IS OUR PRIMARY METHOD
def run_for_all_companies():
    for company in CIKS:
        date_and_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print(f'Evaluating {company} at {date_and_time}')
        url = build_url(CIKS[company])
        html = get_html_for_url(url)
        table_rows = get_table_rows_from_html(html)
        cached_stuff = read_cache(company)
        cache_diff = diff_arrays_of_hashes(table_rows, cached_stuff)
        if len(cache_diff) > 0:
            alert(company, cache_diff)
            write_to_cache(company, cache_diff + cached_stuff)
        else:
            print(f'No change for {company}')

# ---------------MAIN-----------------------
run_for_all_companies()
