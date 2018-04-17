# url_shortener
Yet another url shortener

# Getting started
```
docker-compose up -d
```

# API
1. Create new short url
```
➜  ~ curl -X POST -d '{"link":"http://example.com"}' http://localhost:8888/shortcut
{"id": "k0gvcpsgtd"}% 
```
```
➜  ~ ws ws://127.0.0.1:8888/ws
> {"command":"shortcut","body":{"link":"http://example.com"}}
< {"code": 200, "body": {"id": "k0gvcpsgtd"}}
```
2. Get last redirect timestamp and count of redirects
```
➜  ~ curl -X POST -d '{"id":"k0gvcpsgtd"}' http://localhost:8888/stats
{"last_redirected": 1513959507.3422477, "redirects_count": 1}%  
```
```
➜  ~ ws ws://127.0.0.1:8888/ws
> {"command":"get_stats","body":{"id":"k0gvcpsgtd"}}
< {"code": 200, "body": {"last_redirected": null, "redirects_count": 0}}
```
3. Redirect to real link
```
➜  ~ curl http://localhost:8888/r/k0gvcpsgtd
302: Found% 
```
4. Remove all data from db
```
➜  ~ curl -X DELETE -d '{"confirm":"Yes"}' http://localhost:8888/admin/all_links
200: OK%
```
```
➜  ~ ws ws://127.0.0.1:8888/ws
> {"command":"purge_all","body":{"confirm":"yes"}}
< {"code": 200, "body": {}}

```
5. Get map all links
```
➜  ~ curl http://localhost:8888/admin/all_links
{"links": {"k0gvcpsgtd": "http://example.com"}}%
```
```
➜  ~ ws ws://127.0.0.1:8888/ws
> {"command":"get_all_links","body":{}}
< {"code": 200, "body": {"links": {"k0gvcpsgtd": "http://example.com"}}}
```

# Links
* https://github.com/hashrocket/ws - websocket cli for exploring and debugging.  