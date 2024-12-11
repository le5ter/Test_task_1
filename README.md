# Тестовое задание для Betting Software

## Что нужно для запуска
Заполнить файл example.env и переименовать его в .env.

Далее создаем контейнеры

```bash
docker-compose up
```

Далее, используя консоль контейнера postgres, перейти в /var/lib/postgresql/data и в файле pg_hba.conf,
используя

```
nano pg_hba.conf
```

прописать

```
host    all             all             0.0.0.0/0              md5
host    all             all             ::/0                   md5
```

для взаимодействия вне контейнера.

## Для доступа к API Line provider используем адрес
```
http://127.0.0.1:8000
```
## Для доступа к API Bet Maker используем адрес
```
http://127.0.0.1:8001
```