# get proxy
:mushroom:
#### Сбор и валидация прокси в реальном времени из открытых источников: 
#### https://www.sslproxies.org/, https://free-proxy-list.net/
#### Cоздание списка из 10 рабочих и постоянная их актуализаця.

### API:

**http://ip:8000/health** - статус сервиса

**http://ip:8000/get_proxy** - получить 1 рабочий прокси

### Образ docker:
**_dimosso/get_proxy:beta_**

Скачивание и запуск контейнера:

- docker run -d --restart=always -p 8000:8000/tcp dimosso/get_proxy:beta
