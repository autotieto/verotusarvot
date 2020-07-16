#!env python

import requests
import argparse
from bs4 import BeautifulSoup as soup
import re
from urllib.parse import urljoin
import hashlib

RE_YEAR = re.compile('([0-9]{4})', re.M)

def parse_args():
    parser = argparse.ArgumentParser(description='Download data.')
    parser.add_argument('--url', default='https://www.vero.fi/henkiloasiakkaat/auto/autoverotus/autoveron_maara/taulukoita_ajoneuvojen_sovelletuista_ve/')
    return parser.parse_args()


def main(args):
    s = requests.Session()
    r = s.get(args.url)
    page = soup(r.text, 'lxml')
    year_links = page.select('h2:has(> a[id]):contains(Henkil) + ul > li:contains(xls) > a')
    md5sums = []
    for a in year_links:
        year = RE_YEAR.findall(a.text)[0]
        filename = f'data/car_taxes_{year}.xls'
        url = urljoin(args.url, a['href'])
        digester = hashlib.md5()
        with s.get(url, stream=True) as r, open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=10240):
                f.write(chunk)
                digester.update(chunk)
        md5 = digester.hexdigest()
        md5sums.append((md5, filename))
        print(f'''{year}, {filename}, {md5}, {url}''')
    with open('data/MD5SUMS', 'w') as f:
        for md5, filename in md5sums:
            f.write(f"{md5} {filename}\n")


if __name__=='__main__':
    main(parse_args())
