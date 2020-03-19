from bs4 import BeautifulSoup
import urllib3
import ssl
import pandas
from multiprocessing import Process
import tldextract

ssl._create_default_https_context = ssl._create_unverified_context

# Load data into pandas dataframe
df = pandas.read_csv('./data/majestic_million.csv')

# We will fetch and try to get the meta

def fetch_meta(url):
    try:
        res = req.request('GET', str(url),headers=headers, timeout=1)
        soup = BeautifulSoup(res.data, 'html.parser')
        description = soup.find(attrs={'name': 'Description'})

    # If name description is big letters:
        if description == None:
            description = soup.find(attrs={'name': 'description'})

            if description == None:
                print('Context is empty, pass')
                meta_data = None
            else:
                content = description['content']
                url_clean = tldextract.extract(url)
                suffix = url_clean.suffix
                domain = url_clean.domain

                # Try to clean up websites with RU, JP, CN, PL we are trying to get only english trainig data.

                if suffix in ['com','org','ai','me','app','io','ly','co']:
                    print(url)
                    print(url_clean)
                    print(content)
                    meta_data = (str(content) + ' = @ = ' + str(domain) + '.' + str(suffix) + '\n')
                # Domains with weird tld's are not in our priority. We would like to keep our training data as clean as possible.
                else:
                    print('Domain suffix is low priority ' + str(url))
                    meta_data = None
                return meta_data
    except Exception as e:
        print(e)

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36','Accept-Language':'en-US'}
req = urllib3.PoolManager(maxsize=10)

# Use the domain amount to scrape how much meta data you want to collect.
# Majestic Million Csv contains top 1 Million Domains which will take lots of time to fetch and scrape all the data.

domain_amount = 100000
increment = int(domain_amount / 5)

# Since it will take a lot of time to do this in a single thread, we will create 4 instances to fetch websites in parallel.
# It's a little bit quick and dirty approach but you know, developers are lazy.

def worker_1():
    meta_context = open('./data/meta_context_1.txt', 'w')
    for x in range(increment):
        meta_data = fetch_meta(df['Domain'][x])
        if meta_data is not None:
            meta_context.write(meta_data)
        else:
            continue
    meta_context.close()

def worker_2():
    meta_context = open('./data/meta_context_2.txt', 'w')
    for x in range(increment+1, increment*2):
        meta_data = fetch_meta(df['Domain'][x])
        if meta_data is not None:
            meta_context.write(meta_data)
        else:
            continue
    meta_context.close()


def worker_3():
    meta_context = open('./data/meta_context_3.txt', 'w')
    for x in range((increment*2+1), increment*3):
        meta_data = fetch_meta(df['Domain'][x])
        if meta_data is not None:
            meta_context.write(meta_data)
        else:
            continue
    meta_context.close()


def worker_4():
    meta_context = open('./data/meta_context_4.txt', 'w')
    for x in range((increment*3+1), increment*4):
        meta_data = fetch_meta(df['Domain'][x])
        if meta_data is not None:
            meta_context.write(meta_data)
        else:
            continue
    meta_context.close()


def worker_5():
    meta_context = open('./data/meta_context_5.txt', 'w')
    for x in range((increment*4+1), increment*5):
        meta_data = fetch_meta(df['Domain'][x])
        if meta_data is not None:
            meta_context.write(meta_data)
        else:
            continue
    meta_context.close()

if __name__ == '__main__':
    Process(target=worker_1).start()
    Process(target=worker_2).start()
    Process(target=worker_3).start()
    Process(target=worker_4).start()
    Process(target=worker_5).start()
