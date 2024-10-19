# https://github.com/datasint/DorkSint #

################################################## 
#                                                #  
#  ____  ____  ____  _  __ ____  _  _      _____ #
# /  _ \/  _ \/  __\/ |/ // ___\/ \/ \  /|/__ __\#
# | | \|| / \||  \/||   / |    \| || |\ ||  / \  #
# | |_/|| \_/||    /|   \ \___ || || | \||  | |  #
# \____/\____/\_/\_\\_|\_\\____/\_/\_/  \|  \_/  #
#                                                #
##################################################  
                       
import argparse
import requests
from bs4 import BeautifulSoup
from termcolor import colored
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"
}

# u can add other search engines
SEARCH_ENGINES = {
    'Google': {
        'url': "https://www.google.com/search?q={query}",
        'result_selector': 'div.g',
        'title_selector': 'h3',
        'link_selector': 'a',
    },
    'Bing': {
        'url': "https://www.bing.com/search?q={query}",
        'result_selector': 'li.b_algo',
        'title_selector': 'h2',
        'link_selector': 'a',
    },
    'Yandex': {
        'url': "https://yandex.com/search/?text={query}",
        'result_selector': 'li.serp-item',
        'title_selector': 'h2',
        'link_selector': 'a',
    },
    'DuckDuckGo': {
        'url': "https://duckduckgo.com/html/?q={query}",
        'result_selector': 'div.result__body',
        'title_selector': 'a.result__a',
        'link_selector': 'a',
    },

}


def search_engine(query, search_url, result_selector, title_selector, link_selector):
    try:
        response = requests.get(search_url.format(query=query), headers=HEADERS)
        soup = BeautifulSoup(response.text, 'html.parser')

        results = []
        for item in soup.select(result_selector):
            title = item.select_one(title_selector).text if item.select_one(title_selector) else "No title"
            link = item.select_one(link_selector)['href'] if item.select_one(link_selector) else "No link"
            results.append((title, link))

        return results
    except Exception as e:
        print(f"{colored('| !', 'red')} Error during search: {str(e)}.")
        return []


def search_dork_all_engines(dork):
    start_time = time.time()
    total_results = 0

    for engine, details in SEARCH_ENGINES.items():
        results = search_engine(dork, details['url'], details['result_selector'], details['title_selector'], details['link_selector'])

        if results:
            print(colored('| #', 'green') + f" {engine}:\n")
            for title, link in results:
                print(f"{colored('+', 'green')} {colored('Title: ' + title)}")
                print(f"{colored('+', 'green')} {colored('Site: ' + link)}\n")
            total_results += len(results)
        else:
            print(colored('| #', 'red') + f' {engine}: No results found...\n')

    elapsed_time = time.time() - start_time

    print(colored('| #', 'green') + f" Search completed with {colored(total_results, 'green')} results.")
    print(colored('| #', 'green') + f" Search duration: {colored(str(f'{elapsed_time:.2f}') + ' s', 'green')}.")



def main():
    parser = argparse.ArgumentParser(description="DorkSint - OSINT Tool", usage="dorksint [-f] {your dork}")
    parser.add_argument("query", nargs='*', help="The search query (e.g., full name)")
    parser.add_argument("-f", "--filetypes", action="store_true", help="Include file-specific dork search")

    args = parser.parse_args()

    if not args.query:
        print(r"""
GitHub - https://github.com/datasint/DorkSint
              
                   [v.1.0.5]
  .___                \       _____           .   
  /   `    __.  .___  |   ,  (      ` , __   _/_  
  |    | .'   \ /   \ |  /    `--.  | |'  `.  |   
  |    | |    | |   ' |-<        |  | |    |  |   
  /---/   `._.' /     /  \_ \___.'  / /    |  \__/
""")
        print(colored('!', 'red') + ' Invalid usage!\n')
        print(colored('#', 'green') + " Usage:\n")
        print(colored('#', 'green') + " Default search: 'dorksint {your dork for search}'.")
        print(colored('#', 'green') + " Search with PDF, WORD, EXCEL, DB files: 'dorksint -f {your dork for search}'.\n")
        return  

    query = ' '.join(args.query)
    query = f'"{query}"'

    if args.filetypes:
        print(r"""
GitHub - https://github.com/datasint/DorkSint
              
                   [v.1.0.5]
  .___                \       _____           .   
  /   `    __.  .___  |   ,  (      ` , __   _/_  
  |    | .'   \ /   \ |  /    `--.  | |'  `.  |   
  |    | |    | |   ' |-<        |  | |    |  |   
  /---/   `._.' /     /  \_ \___.'  / /    |  \__/
""")
        
        file_types = ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'sql', 'db', 'csv']
        file_type_dork = ' OR '.join([f'filetype:{ft}' for ft in file_types])

        specific_dork = f'{query} {file_type_dork}'
        print(colored('| *', 'green') + f" Searching with dork: {query}...\n")
        search_dork_all_engines(specific_dork)

    else:

        print(r"""
GitHub - https://github.com/datasint/DorkSint
              
                   [v.1.0.5]
  .___                \       _____           .   
  /   `    __.  .___  |   ,  (      ` , __   _/_  
  |    | .'   \ /   \ |  /    `--.  | |'  `.  |   
  |    | |    | |   ' |-<        |  | |    |  |   
  /---/   `._.' /     /  \_ \___.'  / /    |  \__/
""")
        
        print(colored('| *', 'green') + f" Searching with dork: {query}...\n")
        search_dork_all_engines(query)

if __name__ == "__main__":
    main()