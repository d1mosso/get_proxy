import requests
from bs4 import BeautifulSoup
import json
import time
import threading
from proxy_randomizer import RegisteredProviders  # берет рандомно прокси с ресурсов https://free-proxy-list.net/ и https://www.sslproxies.org/


lock = threading.Lock()

class Proxy_from_sslproxies_org():
    URL = "https://www.sslproxies.org/"

    @classmethod
    def __get_html(cls, url):
        r = requests.get(url)
        return r.text

    @classmethod
    def __get_list_ip(cls, html):
        list_ip = []
        soup = BeautifulSoup(html, "lxml")
        elements = soup.find("tbody").find_all("tr")
        for element in elements:
            ip = element.find_all("td")[0].text
            port = element.find_all("td")[1].text
            proxy = "{}:{}".format(ip, port)
            list_ip.append(proxy)
        return list_ip

    @classmethod
    def facade(cls):
        """ Функция возвращает список https прокси. """
        html = cls.__get_html(cls.URL)
        list_ip = cls.__get_list_ip(html)
        return list_ip


def check_proxy_curl(ip_from_list):
    try:
        ip_in_site = json.loads(requests.get("https://api.ipify.org?format=json",
                                             proxies={"https": ip_from_list, "http": ip_from_list},
                                             timeout=3).text).get('ip')
        # print('{} is ok'.format(ip_from_list.split(':')[0]))
        # print('ip_in_site {}'.format(ip_in_site))
        if ip_from_list.split(':')[0] == ip_in_site:
            return True
    except Exception as x:
        print('--' + ip_from_list + ' is dead: ' + x.__class__.__name__)
        return False


def source_proxy_1():
    copy_proxy_list = []
    while True:
        proxy_list_1 = Proxy_from_sslproxies_org.facade()
        if proxy_list_1 == copy_proxy_list:
            time.sleep(5)
            proxy_list_1.clear()
            continue
        print(proxy_list_1)
        for proxy in proxy_list_1:
            if check_proxy_curl(proxy):
                print('{} is ok'.format(proxy))
                write_ok_proxy_in_file(proxy)

        copy_proxy_list = proxy_list_1.copy()
        proxy_list_1.clear()


def source_proxy_2():
    rp = RegisteredProviders()
    rp.parse_providers()

    while True:
        proxy_full = rp.get_random_proxy()
        proxy = str(proxy_full).split(' ')[0]  # Получаем Прокси
        if check_proxy_curl(proxy):
            write_ok_proxy_in_file(proxy)


def write_ok_proxy_in_file(proxy):
    with lock:
        with open("proxy_list.txt", "a") as f:
            f.write('{}\n'.format(proxy))


def read_file_proxies():
    while True:
        with lock:
            with open('proxy_list.txt', 'r+') as fp:
                lines = fp.readlines()
                if len(lines) > 10:
                    fp.seek(0)
                    fp.truncate()
                    print('delete old proxies: {}'.format(lines[:(len(lines)-10)]))
                    fp.writelines(lines[-10:])
        time.sleep(10)


def get_proxy_threads():
    first_thread = threading.Thread(target=source_proxy_1, name='Thread Proxy_from_sslproxies_org')
    first_thread.start()
    second_thread = threading.Thread(target=source_proxy_2, name='Thread proxy_randomizer')
    second_thread.start()
    read_thread = threading.Thread(target=read_file_proxies, name='Thread read_file_proxies')
    read_thread.start()
