Title: WebDav за https proxy
Category: linux
Date: 2020-06-19 22:55:22
Tags: webdav, nginx, https
og_image: images/2020-06-19-webdav-proxy-title.png

![Title]({static}/images/2020-06-19-webdav-proxy-title.png)

Регулярно читаю различную литературу. Зачастую в *pdf* формате. *Pdf* книги читаю через [GoodReader](TODO add link) на *iPad* (*liara*). Постоянно отмечаю и комментирую текст через аннотации, которые сохраняются непосредственно в pdf файл. А для синхронизации книжек использую *webdav*, настроенный на домашнем сервере с помощью *nginx*. Ранее все крутилось почти на голом *CubieBoard* (*edi2*), а теперь на *HP MicroServer* (*edi3*) в контейнерах. В скобках указаны имена девайсов в моей локальной сети. Называю железки по именам героев из *Mass Effect*. *edi3* — это уже третья реинкарнация моего центрального домашнего сервера.

Как-то раз я задумал скрыть все сервисы, запущенные на сервере за proxy. Задача proxy сводится к распределению трафика на основе имени домена и поддержке *https*. Внутренний (фактически межконтейнерный) трафик остается нешифрованным. Изначально роль proxy выполнял *nginx*. На нем же был настроен *webdav* для книг. Но достаточно быстро я перешел на [*Fabio*][fabio]. Решение судя по всему не сильно популярное, но гибкое и динамичное. Работает примерно так:

* Настройки задаются в labels контейнеров
* [*Registrator*](https://github.com/gliderlabs/registrator) копирует информацию в [*consul*][consul]
* [*Fabio*][fabio] читает данные из [*consul*][consul] и строит Routing Table. Обновления динамические, ничего ребутать или релоудить не надо.

Вот пример кусочка `docker-compose` для [*gitea*](https://gitea.io):

```yml
services:
  gitea:
    image: gitea/gitea:1.11
    labels:
      SERVICE_3000_NAME: gitea
      SERVICE_3000_CHECK_HTTP: /api/v1/version
      SERVICE_3000_CHECK_INTERVAL: 15s
      SERVICE_3000_TAGS: urlprefix-gitea.puzan.info:443/
      SERVICE_22_NAME: gitea-ssh
      SERVICE_22_CHECK_TCP: true
      SERVICE_22_CHECK_INTERVAL: 15s
      SERVICE_22_TAGS: urlprefix-:2222 proto=tcp
```

Вернемся к *webdav*. В этой схеме *webdav* переехал в отдельный *nginx* (80 порт в контейнере), доступ к которому осуществляется через [*fabio*][fabio] через *https* (443 порт на *edi3*). Ничего не предвещало беды, но я столкнулся вот с такой ошибкой во время обновления файлов (*nginx* лог):

```
read_1  | 172.21.0.7 - puzan [18/Jun/2020:20:49:46 +0000] "PROPFIND /current/ HTTP/1.1" 207 2657 "-" "GoodReader"
read_1  | 172.21.0.7 - puzan [18/Jun/2020:20:49:46 +0000] "PUT /current/temp1 HTTP/1.1" 201 0 "-" "GoodReader"
read_1  | 2020/06/18 20:49:46 [error] 6#6: *7 client sent invalid "Destination" header: "https://read.puzan.info/current/some_book.pdf", client: 172.21.0.7, server: www.read.puzan.info, request: "MOVE /current/temp1 HTTP/1.1", host: "read.puzan.info"
read_1  | 172.21.0.7 - puzan [18/Jun/2020:20:49:46 +0000] "MOVE /current/temp1 HTTP/1.1" 400 173 "-" "GoodReader"
```

Как видно сначала происходит поиск файлов через `PROPFIND`. Затем выполняется `PUT` обновленного файла во временный файл `/current/temp1`. Дальше выполняется попытка `MOVE`. Но `MOVE` выполняется для `Destination="https://read.puzan.info/…"`. И как видно *nginx* ничего не знает про *https* сервис. Тут встает вопрос почему *GoodReader* не использует относительные пути. Но это немного другая история, которая не поддается быстрому исправлению.

Починить проблему на серверной стороне (без поднятия внутренней *https* точки) помогает модуль [Headers More](https://www.nginx.com/resources/wiki/modules/headers_more/). Суть фикса заключается в том, чтобы переписать значение `Destination` заголовка c `https://…`, на `http://…`. *Nginx* конфиг для *webdav* теперь у меня выглядит примерно так:

```nginx
server {
    listen 80;
    server_name www.read.puzan.info read.puzan.info;

    location / {
        # Rewrite destination header if it starts with https
        set $destination $http_destination;
        if ($destination ~ ^https://(.+)) {
            set $destination http://$1;
            more_set_input_headers "Destination: $destination";
        }

        root /data/read;

        dav_methods PUT DELETE MKCOL COPY MOVE;
        dav_ext_methods PROPFIND OPTIONS;
    }
}
```

Установка модуля в *debian*:

```
apt-get install -y nginx libnginx-mod-http-headers-more-filter
```

Использую базовый образ *debian* в контейнере для webdab, чтобы не искать и собирать нужные *nginx* модули (тут есть еще зависимость на `dav_ext_module`). Изначально пробовал *alpine*, но быстро сдался.

---

PS. Решение было найдено на каком-то китайском форуме (ссылку потерял уже), который вывел на [идею с перезаписью заголовка](https://serverfault.com/questions/901325/how-to-rewrite-webdav-http-destination-request-header-on-nginx).

[fabio]: https://fabiolb.net
[consul]: https://www.consul.io
