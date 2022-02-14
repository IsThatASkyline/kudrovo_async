from bs4 import BeautifulSoup
from pymongo import MongoClient
import time
import asyncio
import aiohttp


start_time = time.time()

all_links = []
cards_data = []


def get_database():

    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb+srv://artklk12:artklk12@cluster0.ch7cl.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient

    client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client['user_shopping_list']


async def get_data(session, link_product):

    url = link_product
    headers = {
        "accept": "*/*",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
    }

    async with session.get(url=url, headers=headers) as response:
        src = await response.text()
        soup = BeautifulSoup(src, "lxml")

        try:
            title = soup.find('h1', class_='a10a3f92e9--title--UEAG3').text
        except Exception:
            title = "Нет названия"
        try:
            prise = soup.find('span', class_='a10a3f92e9--price_value--lqIK0').text
        except Exception:
            prise = "Нет цены"
        try:
            address = soup.find('address', class_='a10a3f92e9--address--F06X3').text.rstrip('На карте')
        except Exception:
            address = "Нет адреса"
        try:
            opisanie = soup.find('p', class_='a10a3f92e9--description-text--YNzWU').text
        except Exception:
            opisanie = "Нет описания"
        try:
            image = soup.find('div', class_='a10a3f92e9--photo_gallery_container--OS_kt').find("div").find("span").find(
                "span").get("content")
        except Exception:
            image = "Нет картинки"
        cards_data.append(
            {
                "Название": title,
                "Цена": prise.replace(" ", " "),
                "Адрес": address,
                "Описание": opisanie.replace("\n", ""),
                "Ссылка": link_product,
                "Картинка": image
            }
        )


async def get_links(session, page):

    url = f"https://spb.cian.ru/cat.php?deal_type=rent&engine_version=2&location%5B0%5D=244909&offer_type=flat&p={page}&room1=1&room2=1&type=4"
    headers = {
        "accept": "*/*",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
    }

    async with session.get(url=url, headers=headers) as response:
        src = await response.text()
        soup = BeautifulSoup(src, "lxml")
        cards = soup.find_all('article', class_='_93444fe79c--cont--OzgVc')

        tasks = []
        for item in cards:
            link_product = item.find('div', class_='_93444fe79c--container--kZeLu _93444fe79c--link--DqDOy').find(
                'a').get('href')
            task = asyncio.create_task(get_data(session, link_product))
            tasks.append(task)

        await asyncio.gather(*tasks)

async def gather_data():

    url = "https://spb.cian.ru/cat.php?deal_type=rent&engine_version=2&location%5B0%5D=244909&offer_type=flat&room1=1&room2=1&type=4"
    headers = {
        "accept": "*/*",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
    }
    async with aiohttp.ClientSession() as session:
        r = await session.get(url=url, headers=headers)
        soup = BeautifulSoup(await r.text(), "lxml")
        pages_count = int(soup.find("div", class_="_93444fe79c--wrapper--bKcEk").find_all("li")[-1].text)

        tasks = []

        for page in range(1, pages_count + 1):
            task = asyncio.create_task(get_links(session, page))
            tasks.append(task)

        await asyncio.gather(*tasks)

def main():
    asyncio.run(gather_data())
    #
    # with open(f"cards_data_asyncio.json", "w", encoding="utf-8") as file:
    #     json.dump(cards_data, file, indent=4, ensure_ascii=False)
    #
    # finish_time = time.time() - start_time
    # print(f"Всего квартир: {len(cards_data)}")
    # print(f"Затраченное время на работу скрипта: {finish_time}")
    #
    # with open(f"cards_data_asyncio.json", "r", encoding="utf-8") as file:
    #     cards_data = json.load(file)

    db = get_database()
    db.user_1_items.drop()
    col = db["user_1_items"]
    for card in cards_data:
        col.insert_one(card)

if __name__ == '__main__':
    main()
