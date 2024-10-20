import time
import argparse
import aiohttp
import asyncio

from bs4 import BeautifulSoup
from termcolor import colored
from fake_useragent import UserAgent


SEARCH_ENGINES = {
    'Google': {
        'url': "https://www.google.com/search?q={query}",
        'result_selector': 'div.g',
        'title_selector': 'h3',
        'link_selector': 'a',
        'description_selector': 'div.VwiC3b'  
    },
    'Bing': {
        'url': "https://www.bing.com/search?q={query}",
        'result_selector': 'li.b_algo',
        'title_selector': 'h2',
        'link_selector': 'a',
        'description_selector': 'p'  
    },
    'Yandex': {
        'url': "https://yandex.com/search/?text={query}",
        'result_selector': 'li.serp-item',
        'title_selector': 'h2',
        'link_selector': 'a',
        'description_selector': 'div.text-container'  
    }
}

ua = UserAgent()
HEADERS = {'User-Agent': ua.random}

async def fetch(session, url):
    try:
        async with session.get(url, headers=HEADERS, timeout=aiohttp.ClientTimeout(total=10)) as response:
            return await response.text()
    except Exception as e:
        print(f"{colored('| !', 'red')} Error during fetch: {str(e)}.")
        return None

async def search_engine(session, query, search_url, result_selector, title_selector, link_selector, description_selector):
    try:
        html_content = await fetch(session, search_url.format(query=query))
        if not html_content:
            return []

        soup = BeautifulSoup(html_content, 'html.parser')
        results = []

        for item in soup.select(result_selector):
            title = item.select_one(title_selector).text if item.select_one(title_selector) else "No title"
            link = item.select_one(link_selector)['href'] if item.select_one(link_selector) else "No link"
            description = item.select_one(description_selector).text if item.select_one(description_selector) else "No description"
            results.append((title, description, link))

        return results
    except Exception as e:
        print(f"{colored('| !', 'red')} Error during search: {str(e)}.")
        return []

async def search_dork_all_engines(dork):
    start_time = time.time()
    total_results = 0

    connector = aiohttp.TCPConnector(limit=10)  # Limit to 10 concurrent connections
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [
            search_engine(session, dork, details['url'], details['result_selector'], details['title_selector'],
                          details['link_selector'], details['description_selector'])
            for engine, details in SEARCH_ENGINES.items()
        ]

        search_results = await asyncio.gather(*tasks)

        for engine, results in zip(SEARCH_ENGINES.keys(), search_results):
            if results:
                print(colored('| #', 'green') + f" {engine}:\n")
                for title, description, link in results:
                        clickable_link = f"\033]8;;{link}\033\\Click\033]8;;\033\\"
                        print(f"{colored('+', 'green')} Title: {title}")
                        print(f"{colored('+', 'green')} Description: {description}")
                        print(f"{colored('+', 'green')} Site: {clickable_link}\n")
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

                   [v.1.0.6]
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

                   [v.1.0.6]
  .___                \       _____           .   
  /   `    __.  .___  |   ,  (      ` , __   _/_  
  |    | .'   \ /   \ |  /    `--.  | |'  `.  |   
  |    | |    | |   ' |-<        |  | |    |  |   
  /---/   `._.' /     /  \_ \___.'  / /    |  \__/
""")
        
        file_types = ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'sql', 'db', 'csv', 'mdb', 'accdb', 'sqlite', 'psql']
        file_type_dork = ' OR '.join([f'filetype:{ft}' for ft in file_types])
        specific_dork = f'{query} {file_type_dork}'
        print(colored('| *', 'green') + f" Searching with dork: {query}...\n")
        asyncio.run(search_dork_all_engines(specific_dork))
    else:
        print(r"""
GitHub - https://github.com/datasint/DorkSint

                   [v.1.0.6]
  .___                \       _____           .   
  /   `    __.  .___  |   ,  (      ` , __   _/_  
  |    | .'   \ /   \ |  /    `--.  | |'  `.  |   
  |    | |    | |   ' |-<        |  | |    |  |   
  /---/   `._.' /     /  \_ \___.'  / /    |  \__/
""")
        
        print(colored('| *', 'green') + f" Searching with dork: {query}...\n")
        asyncio.run(search_dork_all_engines(query))

if __name__ == "__main__":
    main()
