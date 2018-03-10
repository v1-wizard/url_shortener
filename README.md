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
```
➜  ~ ws ws://127.0.0.1:8888/ws
> {"type":"shortcut","body":{"link":"http://example.com"}}
< {"code": 200, "body": {"id": "c3f1dece-4cb4-481c-bd32-3d56045f0a79"}}
```
2. Get last redirect timestamp and count of redirects
```
➜  ~ curl -X POST -d '{"id":"31dc820b-d8cb-4d53-95bc-52b7a5445380"}' http://localhost:8888/stats
{"last_redirected": 1513959507.3422477, "redirects_count": 1}%  
```
```
➜  ~ ws ws://127.0.0.1:8888/ws
> {"type":"get_stats","body":{"id":"c3f1dece-4cb4-481c-bd32-3d56045f0a79"}}
< {"code": 200, "body": {"last_redirected": null, "redirects_count": 0}}
```
3. Redirect to real link
```
➜  ~ curl http://localhost:8888/r/31dc820b-d8cb-4d53-95bc-52b7a5445380
302: Found% 
```
4. Remove all data from db
```
➜  ~ curl -X DELETE -d '{"confirm":"Yes"}' http://localhost:8888/admin/all_links
200: OK%
```
```
➜  ~ ws ws://127.0.0.1:8888/ws
> {"type":"purge_all","body":{"confirm":"yes"}}
< {"code": 200, "body": {}}

```
5. Get map all links
```
➜  ~ curl http://localhost:8888/admin/all_links
{"links": {"31dc820b-d8cb-4d53-95bc-52b7a5445380": "http://example.com"}}%
```
```
➜  ~ ws ws://127.0.0.1:8888/ws
> {"type":"get_all_links","body":{}}
< {"code": 200, "body": {"links": {"c3f1dece-4cb4-481c-bd32-3d56045f0a79": "http://example.com"}}}
```
