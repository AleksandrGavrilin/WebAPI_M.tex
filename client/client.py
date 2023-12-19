import os
import threading

import requests
import random
import logging
import time

N = int(os.getenv("N", 3))
M = int(os.getenv("M", 100))


url = os.getenv("URL", "http://localhost:8000/api/data")


# Генерация текста запроса
def generate_log():
    ips = ['192.168.132.111', '192.122.132.111', '192.148.132.111']  # пример возможных адресов
    methods = ['GET', 'POST', 'PUT', 'DELETE']  # пример возможных HTTP методов
    uris = ['/home', '/users', '/products']  # пример возможных URI
    status_codes = [200, 201, 400, 404, 500]  # пример возможных HTTP статус кодов

    ip_address = random.choice(ips)
    http_method = random.choice(methods)
    uri = random.choice(uris)
    http_status_code = random.choice(status_codes)

    text = f'{ip_address} {http_method} {uri} {http_status_code}'
    return text


# Отправка POST запроса
def send_request():
    log = generate_log()
    try:
        requests.post(url, json={"log": log})
        logging.info(log)
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")


# Запуск N потоков с рандомной задержкой
def run():
    logging.basicConfig(filename='../client.log', level=logging.INFO)
    threads = []
    for _ in range(N):
        t = threading.Thread(target=send_request)
        t.start()
        threads.append(t)
        delay = random.randint(0, M)
        time.sleep(delay/1000)
    for t in threads:
        t.join()


if __name__ == '__main__':
    run()
