# crawler_weehui
爬取漫小说(weehui)的漫画资源

# 起因

昨天看到这个漫画网站有个漫画挺有趣的.但是居然要收费才能看.
然后找遍互联网找到这家可以看.
但是需要收费三块钱一天,十块钱七天.
不过每天晚上的19点到21点这个网站可以免费观看.
但不是每个人都这在这个时候有空的啊.所有可以直接在这个时候通过这个小脚本自动下载所有的图片到自己的电脑上随便看

##  使用过程

1. 输入用户名
2. 密码
3. 漫画链接地址如(http://www.weehui.com/cartoon/index/d0de830142167fc4cff3a61d72faea02)
4. 总话数(-.- 懒得写了.自己去看有几话.比如一共有57话,那么输入57)
5. 漫画存放的地址(必须为文件夹)
6. 可选第几话开始下载
7. 可选第几话结束卸载
6. 等待下载完成.图片命名为 话数_第几张图片.jpg

``` python
# 用户名
# 用户名
username = input('漫小说用户名:')
# 密码
password = input('漫小说密码:')
# 漫画链接地址
cartoonUrl = input('漫画链接地址:')
# 漫画总章数
cartoonPagesNum = input('漫画总章数(比如一共有57话,那么输入57)):')
# 漫画存放的地址 "/Users/hdy/Desktop/pic/"
save_url = input('漫画存放地址(必须为文件夹):')
# 第几话开始下载
cartoonStartIndex = input('从第几话开始?如果不输入默认为1:')
if(cartoonStartIndex):
    cartoonStartIndex = int(cartoonStartIndex)
else:
    cartoonStartIndex = 1

# 第几话结束
cartoonEndIndex = input('从第几话结束?如果不输入默认为到底:')
if(cartoonEndIndex):
    cartoonEndIndex = int(cartoonEndIndex)
else:
    cartoonEndIndex = int(cartoonPagesNum)

# 开始下载
login(username, password, cartoonUrl)
```

## 使用过程图片
![下载中..](https://github.com/egdw/crawler_weehui/blob/master/show.jpg?raw=true)
![下载完成..](https://github.com/egdw/crawler_weehui/blob/master/main2.png?raw=true)

## 分析了登录的请求
很简单.毫无难度的登录.甚至连密码加密都没有...
``` python
        payload = {'name': username, 'password': password}
        headers = {'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
                   'Host': 'www.weehui.com', 'Origin': 'http://www.weehui.com', 'Referer': 'http://www.weehui.com/login/login'}
        r = rq.post('http://www.weehui.com/login/login',
                    data=payload, headers=headers)
```
## 然后遍历图片
没有自动去分析漫画一共有几话.懒的写了.- -.
```python
def get(index):
    print("正在下载第"+str(index)+'章内容..')
    global cartoon_id
    url = 'http://www.weehui.com/cartoon/read/' + \
        cartoon_id+'/'+str(index)
    r = rq.get(url)
    print(r)
    soup = BeautifulSoup(r.text, 'html5lib')
    # print(soup.prettify())
    div = soup.findAll('div', attrs={"class": 'contentNovel'})[0]
    # print(div)
    soup = BeautifulSoup(str(div), 'html5lib')
    i = 0
    for src in soup.findAll("img"):
        data_original = src.get('data-original')
        if(data_original == None):
            data_original = src.get('src')
        print(data_original)
        i = i + 1
        headers = {'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
                   'Referer': url}
        ir = requests.get(data_original, headers=headers)
        global save_url
        if ir.status_code == 200:
            open(save_url +
                 str(index)+"_"+str(i)+".jpg", 'wb').write(ir.content)

    index = index+1
    global cartoonPagesNum
    if(index < int(cartoonPagesNum)):
        get(index)

```