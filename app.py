import requests
from lxml import html
from urllib.parse import urljoin
import csv

movies = []

def write_to_csv(data):
    headers = ['Name', 'Release Year' , 'Rating']
    with open('movies.csv', 'w', encoding='utf-8') as f:
        writer = csv.DictWriter(f,headers)
        writer.writeheader()
        writer.writerows(data)

def get(lists):
    try:
        return lists.pop(0)
    except:
        return ''


def scraping(url):
    resp = requests.get(url=url, headers={
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 Edg/83.0.478.61'
    })


    tree = html.fromstring(html=resp.content)

    movies_main = tree.xpath("//div[@class='lister-list']/div") 

    for movie in movies_main:
        m = {
                'Name' : get(movie.xpath(".//div[@class='lister-item-content']/h3/a/text()")),
                'Release Year' : get(movie.xpath(".//div[@class='lister-item-content']/h3/span[2]/text()")),
                'Rating' : get(movie.xpath(".//div[@class='lister-item-content']/div/div/strong/text()"))    
        }
        movies.append(m)
        
    next_page = tree.xpath("(//a[@class='lister-page-next next-page']/@href)[2]")

    if len(next_page) != 0:
        next_page_url = urljoin(base=url, url=next_page[0])
        scraping(url=next_page_url)

scraping(url='https://www.imdb.com/search/title/?genres=drama&groups=top_250&sort=user_rating,desc&ref_=adv_prv')

print(len(movies))
write_to_csv(movies)

    