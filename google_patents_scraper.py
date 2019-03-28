import pandas as pd
import scrapy
import requests
import json
import argparse
from time import sleep
from lxml import html


def parse_args():

    desc = "Scrapes Google Patents for Relevant Information"  
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument('-v', '--verbose', action='store_true',
        help='Boolean flag indicating if statements should be printed to the console.')

    parser.add_argument('-s', '--search', type=str, nargs='+', required=True,
        help='REQUIRED: The search terms to search Google Patents')

    parser.add_argument('-o', '--output', type=str, required=True,
        default='output.csv',
        help='REQUIRED: Output CSV file')

    parser.add_argument('-n', '--number', type=int, 
        default=100,
        help='Number of returned results')
   
    args = parser.parse_args()
    return args


def generate_json_url(search_terms, num=100):
    """
    Generates the escaped url for downloading the data JSON from Google Patents
    
    Parameters:
    search_terms: The company you want to search for
    num_response: The number of patents
    
    Returns:
    String, URL for Google Patents
    """
    search_terms = search_terms.replace(" ", "+")
    base_url = "https://patents.google.com/xhr/query?url="
    url = base_url + f"assignee={search_terms}%26num={num}%26oq={search_terms}&exp=&sort=new"
    return url


def get_patent_json(json_url):
    """
    Gets Google Patents JSON from API
    
    Parameters:
    json_url: a properly formatted url to the Google Patents API
    
    Returns:
    List of Dicts: Relevant contents of the Google Patents API
    """
    patent_request = requests.get(json_url)
    patent_json = patent_request.json()
    relevant_keys = ['title', 'snippet', 'priority_date', 'filing_date',
                    'grant_date', 'publication_date', 'inventor', 'assignee',
                    'publication_number', 'pdf']
    patent_list = []
    num_results = len(patent_json['results']['cluster'][0]['result'])
    for i in range(num_results):
        patent_dict = {k:v for k,v in patent_json['results']['cluster'][0]['result'][i]['patent'].items() 
         if k in relevant_keys}
        patent_list.append(patent_dict)
    return patent_list


def scrape_patents(patent_list, sleep_time=0.1, verbose=False):
    """
    Scrapes remaining data from Google Patents that isn't available through JSON
    
    Parameters:
    patent_list: a list of dictionary objects produced by get_patent_list
    sleep: how long to wait between each page scrape to avoid being blacklisted
    verbose: print during scraping
    
    Returns:
    
    """
    for idx, patent in enumerate(patent_list):
        
        patent_url = "https://patents.google.com/patent/" + patent['publication_number']
        patent_list[idx]['patent_url'] = patent_url
        
        if verbose: 
            print(f"Getting Patent Number {idx}")
        html_get = requests.get(patent_url).content
        sel = html.fromstring(html_get)

        claims_list = sel.xpath('//div[@class="claim-text"]//text()')
        claims_text = ' '.join(claims_list)

        pdf_link = sel.xpath('//a[@itemprop="pdfLink"]/@href') #Doesn't always exist
        pdf_link = ''.join(pdf_link) 
        
        patent_list[idx]['claims_text'] = claims_text
        patent_list[idx]['pdf_link'] = pdf_link
        sleep(sleep_time)
    
    return patent_list


def output_csv(file_name, patent_list):
    """
    Saves a CSV file to disk from a patent list
    
    Parameters:
    file_name: string with output filename
    """
    df = pd.DataFrame(patent_list)
    df.to_csv(file_name, index=None)


def main():
    args = parse_args()
    if args.verbose: print("Input Arguments\n", args, '\n')


if __name__ == '__main__':
  main()