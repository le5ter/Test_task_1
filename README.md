# Тестовое задание для Betting Software

## Что нужно для запуска

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

