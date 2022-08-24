import requests
import unicodedata
from bs4 import BeautifulSoup


def get_info_cars():
    url = 'https://www.carsensor.net/usedcar/search.php?STID=CS210610&CARC' \
          '=HO_S003&FMCC=HO_S003_F005&YMIN=2015&AR=35*33*36*34&SMAX=60000&PMAX=3000000&CL=BK'

    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    info_cars = soup.find_all('div', class_='cassette js_listTableCassette')

    info_prices = []
    for info_car in info_cars:
        title = info_car.find('h3', class_='cassetteMain__title').text
        title = unicodedata.normalize("NFKD", title)
        title = title.replace('\n', '')
        base_price_main = info_car.find('span', class_='basePrice__mainPriceNum').text
        tmp_price_sub = info_car.find('span', class_='basePrice__subPriceNum')
        base_price_sub = tmp_price_sub.text if tmp_price_sub else ''
        base_price = base_price_main + base_price_sub

        tmp_total_price_main = info_car.find('span', class_='totalPrice__mainPriceNum')
        total_price_main = tmp_total_price_main.text if tmp_total_price_main else ''
        tmp_total_price_sub = info_car.find('span', class_='totalPrice__subPriceNum')
        total_price_sub = tmp_total_price_sub.text if tmp_total_price_sub else ''
        total_price = total_price_main + total_price_sub

        car_datas = info_car.select('div.specList__detailBox > dd.specList__data > span')
        model_year, miles_indo = car_datas[0].text, car_datas[2].text

        pref_city = info_car.select('div.cassetteSub > div.cassetteSub__area > p')
        pref_city = [i.text for i in pref_city]


        info_prices.append({
            'pref_city': pref_city,
            'base_price': base_price,
            'total_price': total_price,
            'model_year': model_year,
            'miles_indo': miles_indo,
            'note': title,
        })

    return info_prices


def main():
    results = get_info_cars()
    for result in results:
        print(result)


if __name__ == "__main__":
    main()

