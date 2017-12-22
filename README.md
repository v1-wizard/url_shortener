# url_shortener
Yet another url shortener

# API
1. /shortcut - create new short url
```
➜  ~ curl -X POST -d '{"link":"http://example.com"}' http://localhost:7777/shortcut
{"id": "31dc820b-d8cb-4d53-95bc-52b7a5445380"}% 
```
2. /stats - get last redirect timestamp and count of redirects
```
➜  ~ curl -X POST -d '{"id":"31dc820b-d8cb-4d53-95bc-52b7a5445380"}' http://localhost:7777/stats
{"last_redirected": 1513959507.3422477, "redirects_count": 1}%  
```
3. /r/{link_id} - url for redirect to real link
```
➜  ~ curl http://localhost:7777/r/31dc820b-d8cb-4d53-95bc-52b7a5445380
302: Found% 
```
