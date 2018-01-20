# url_shortener
Yet another url shortener

# Getting started
```
docker build -t "url_shorter:latest" .
docker run --rm --name=url_shorter -e USH_PORT=7776 -p 8888:7776 url_shorter:latest
```

# API
1. Create new short url
```
➜  ~ curl -X POST -d '{"link":"http://example.com"}' http://localhost:8888/shortcut
{"id": "31dc820b-d8cb-4d53-95bc-52b7a5445380"}% 
```
2. Get last redirect timestamp and count of redirects
```
➜  ~ curl -X POST -d '{"id":"31dc820b-d8cb-4d53-95bc-52b7a5445380"}' http://localhost:8888/stats
{"last_redirected": 1513959507.3422477, "redirects_count": 1}%  
```
3. Redirect to real link
```
➜  ~ curl http://localhost:8888/r/31dc820b-d8cb-4d53-95bc-52b7a5445380
302: Found% 
```
4. Remove all data from db
```
➜  ~ curl -X DELETE -d '{"Are you sure?":"Yes"}' http://localhost:8888/admin/all_links
200: OK%
```
5. Get map all links
```
➜  ~ curl http://localhost:8888/admin/all_links
{"links": {"31dc820b-d8cb-4d53-95bc-52b7a5445380": "http://example.com"}}%
```
