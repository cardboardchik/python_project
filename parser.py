import requests
from bs4 import BeautifulSoup
from store.models import Item


def get_links():
    r = requests.get('https://headphones.com/collections/over-ear-on-ear-headphones?page=1')

    soup = BeautifulSoup(r.text, 'html.parser')

    page = soup.find_all('a', attrs={"class": "card__link"}, href=True)
    links = [i['href'] for i in page]
    return links


def get_items(links):
    for link in links:
        # print(link)
        r = requests.get('https://headphones.com' + link)
        soup = BeautifulSoup(r.text, 'html.parser')
        try:
            name = soup.find('h2', attrs={"class": "h1"}).text.strip()
            price = soup.find('span', attrs={"class": "price-item price-item--sale price-item--last"}).text.strip()[1:]
            img = soup.find('img', attrs={"sizes": "(min-width: 1200px) 605px, (min-width: 990px) calc(55.0vw - 10rem), (min-width: 750px) calc((100vw - 11.5rem) / 2), calc(100vw - 4rem)"})['srcset'].split(",")[0]
            try:
                spec = soup.find('table', attrs={"class": "specification-table"})
                specifications = []
                for i in range(len(spec.find_all("td"))):
                    if spec.find_all("td")[i].text:
                        specification = spec.find_all("td")[i].text.strip()
                        if "More information" in (spec.find_all("td")[i].text):
                            specification = spec.find_all("td")[i].text[:(spec.find_all("td")[i].text).index("More information")].strip()
                        specifications.append(specification)
                specifications_dict = {}
                for i in range(0, len(specifications), 2):
                    specifications_dict[specifications[i]] = specifications[i+1]
            except:
                specifications_dict = {}
            # description = soup.select_one('#description > div > p:nth-child(15)').text
            Item.objects.create(name=name, price=float(price.replace(",", "")), characteristics=specifications_dict, description="", img_links=img, category_id=1)
            print(name)
            print(float(price.replace(",", "")))
            print(img)
            print(specifications_dict)
        except:
            pass

# r = requests.get('https://headphones.com/products/focal-clear-headphones')
# soup = BeautifulSoup(r.text, 'html.parser')
# spec = soup.find('table', attrs={"class": "specification-table"})
# specifications = []
# for i in range(len(spec.find_all("td"))):
#     if spec.find_all("td")[i].text:
#         specification = spec.find_all("td")[i].text.strip()
#         if "More information" in (spec.find_all("td")[i].text):
#             specification = spec.find_all("td")[i].text[:(spec.find_all("td")[i].text).index("More information")].strip()
#         specifications.append(specification)
# specifications_dict = {}
# for i in range(0, len(specifications), 2):
#     specifications_dict[specifications[i]] = specifications[i+1]

# print(specifications_dict)

# s = [i.find_all("td") for i in spec.find_all("tr") if i.find_all("td") in i.find_all("td", attrs={"class": "specification-title"})]
# se = [i.find_next() for i in s]
# print(s)
get_items(get_links())