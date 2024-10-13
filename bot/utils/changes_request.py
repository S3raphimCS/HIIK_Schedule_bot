import requests
from bs4 import BeautifulSoup


URL = 'https://hiik.ru/students/schedule/izmenenie-v-raspisanii.php'

def parse():
    response = requests.get(URL)

    bs = BeautifulSoup(response.text, "html.parser")

    changes = bs.findAll('div', "doc_item")
    links = {}

    for link in changes:
        text = link.a.text
        download_link = "https://hiik.ru" + link.a["href"]
        if "СПО" in text:
            links["СПО"] = (text, download_link)
        else:
            links["ВО"] = (text, download_link)
    return links

if __name__ == "__main__":
    a = parse()
    for link in a:
        print(a[link])