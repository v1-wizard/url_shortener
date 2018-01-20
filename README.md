# url_shortener
Yet another url shortener

# Getting started
```
docker build -t "url_shorter:latest" .
docker run --rm --name=url_shorter -e USH_PORT=7776 -p 8888:7776 url_shorter:latest
```

# API
1. /shortcut - create new short url
```
➜  ~ curl -X POST -d '{"link":"http://example.com"}' http://localhost:8888/shortcut
{"id": "31dc820b-d8cb-4d53-95bc-52b7a5445380"}% 
```
2. /stats - get last redirect timestamp and count of redirects
```
➜  ~ curl -X POST -d '{"id":"31dc820b-d8cb-4d53-95bc-52b7a5445380"}' http://localhost:8888/stats
{"last_redirected": 1513959507.3422477, "redirects_count": 1}%  
```
3. /r/{link_id} - url for redirect to real link
```
➜  ~ curl http://localhost:8888/r/31dc820b-d8cb-4d53-95bc-52b7a5445380
302: Found% 
```
4. /admin/purge - remove all data from db
```
➜  ~ curl -X DELETE -d '{}' http://localhost:8888/admin/purge
200: OK%
```
