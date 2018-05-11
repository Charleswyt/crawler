## urllib

python内置的HTTP请求库 <br>
        
        urllib.rerquest    请求模块
        urllib.error       异常处理模块
        urllib.parse       url解析模块
        urllib.robotparser robots.txt解析模块

**python2与python3的差异**

* python2

        import urllib2
        
        _url = "http://www.baidu.com"
        response = urllib2.urlopen(_url)

* python3

        import urllib.request
        
        _url = "http://www.baidu.com"
        response = urllib.request.urlopen(_url)

## example

* urlopen


    import sys
    import io
    import urllib.request

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码
    _url = "http://www.baidu.com"
    response = urllib.request.urlopen(_url)
    print(response.read().decode("utf-8"))
    
    -------------------------------------------------------------------------------

    import urllib.parse
    import urllib.request
    
    _url = "http://httpbin.org/post"
    data = bytes(urllib.parse.urlencode({"word":"hello"}), encoding="utf8")
    response = urllib.request.urlopen(_url, data=data)
    print(response.read())

    -------------------------------------------------------------------------------
    
    import urllib.request
    
    _url = "http://httpbin.org/get"
    response = urllib.request.urlopen(_url, timeout=1)
    print(response.read())

    -------------------------------------------------------------------------------
    
    import socket
    import urllib.request
    import urllib.error

    _url = "http://httpbin.org/get"
    try:
        respose = urllib.request(_url, timeout=0.1)
    except urllib.URLError as e:
        if isinstance(e.reason, socket.timeout)
            print("TIME OUT")

* response

**响应类型**

    import urllib
    
    _url = "https://www.python.org"
    response = urllib.request.urlopen(_url)
    print(type(response))
    
**状态码，响应头**

    import urllib.request
    
    _url = "https://www.python.org"
    response = urllib.request.urlopen(_url)
    print(response.status)
    print(response.getheaders())
    print(response.getheader("Server"))

* request
    

    import urllib.request
    
    _url = "https://python.org"
    req = urllib.request.Request(_url)
    response = urllib.request.urlopen(req)
    print(response.read().decode("utf-8"))

    -------------------------------------------------------------------------------

    from urllib import request, parse
    
    _url = "https://httpbin.org/post"
    headers = {
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)",
        "Host": "httpbin.org"
    }
    dict = {
        "name" = "Germey"
    }
    data = bytes(parse.urlencode(dict), encoding="utf8")
    req = request.Request(url=_url, data=data, headers=headers, method="POST")
    response = request.urlopen(req)
    print(response.read().decode("utf-8"))
    
    // 大多数情况下，网站都会根据我们的请求头信息来区分你是不是一个爬虫程序，如果一旦识别出这是一个爬虫程序，很容易就会拒绝我们的请求，因此我们需要给我们的爬虫手动添加请求头信息，来模拟浏览器的行为，但是当我们需要大量的爬取某一个网站的时候，一直使用同一个User-Agent显然也是不够的
    MY_USER_AGENT = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    ]
    
    -------------------------------------------------------------------------------
    
    from urllib import request, parse
    
    _url = "https://httpbin.org/post"
    dict = {
        "name" = "Germey"
    }
    data = bytes(parse.urlencode(dict), encoding="utf8")
    req = request.Request(url=_url, data=data, method="POST")
    req.add_header("User-Agent", "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)")
    response = request.urlopen(req)
    print(response.read().decode("utf-8"))
    
* Handler
    

**代理**
    
    
    import urllib.request
    
    _url = "http://www.baidu.com"
    proxy_handler = urllib.request.ProxyHandler({
        "http://127.0.0.1:9743",
        "https://127.0.0.1:9743"
    })
    opener = urllib.request.build_opener(proxy_handler)
    response = opener.open(_url)
    print(response.read())
    
    
**Cookie**
    
    import urllib.cookiejar, urllib.request
    
    _url = "http://www.baidu.com"
    cookie = http.cookiejar.CookieJar()
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)
    response = opener.open(_url)
    for item in cookie:
        print(item.name + "=" + item.value)
        
    -------------------------------------------------------------------------------
    
    import http.cookiejar, urllib.request
    
    _url = "http://www.baidu.com"
    filename = "cookie.txt"
    cookie = http.cookiejar.MozillaCookieJar(filename)
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)
    response = opener.open(_url)
    cookie.save(ignore_discard=True, ignore_expires=True)
    
    -------------------------------------------------------------------------------
    
    import http.cookiejar, urllib.request
    
    _url = "http://www.baidu.com"
    filename = "cookie.txt"
    cookie = http.cookiejar.LWPCookieJar(filename)
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)
    response = opener.open(_url)
    cookie.save(ignore_discard=True, ignore_expires=True)
    
        
    -------------------------------------------------------------------------------
    
    import http.cookiejar, urllib.request
    
    _url = "http://www.baidu.com"
    filename = "cookie.txt"
    cookie = http.cookiejar.LWPCookieJar()
    cookie.load(filename, ignore_discard=True, ignore_expires=True)
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)
    response = opener.open(_url)
    print(response.read().decode("utf-8"))
    
    
* 异常处理

from urllib import request, error

    _url = "http://www.baidu.com"
    try:
        response = request.open(_url)
        except error.HTTPError as e:
            print(e.reason, e.code, e.headers, sep="\n")
        except error.URLError as e:
            print(e.reason)
        else:
            print("Request Successfully.")
            
    
    