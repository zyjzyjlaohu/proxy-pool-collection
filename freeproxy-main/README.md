# freeproxy

通过fofa资产测绘平台获取大量代理数据，利用并发技术快速检测代理的可用性并爆破弱口令，爆破用户名密码可以自行添加到user.txt和pass.txt


使用fofa以下fofa语句进行搜索socks5代理数据，需要key，支持无key，无key可以将key设为空然后可以使用下面的语法进行查询后导出到fofa_results.txt

```
protocol=="socks5" && "Version:5 Method:No Authentication(0x00)" && country="CN"
```


示范格式

```
127.0.0.1:1080
```
![image](https://github.com/user-attachments/assets/d5d0810b-aff7-429f-a140-b9a6665cd0f8)



可食用的地址输出在valid_proxies.txt中

![image](https://github.com/user-attachments/assets/f2bcfa6a-5222-4287-ab0a-dc178e362096)


可以将valid_proxies.txt直接放入到ProxyCat代理的ip.txt中，开启ProxyCat的代理就使用成功了

安装方法

```
git clone https://github.com/qiangshaozhang/freeproxy.git
```

使用方法

```
cd freeproxy
python3 freeproxy.py 
```
![image](https://github.com/user-attachments/assets/4562eef5-0614-461e-8ca2-ab6fcfb1c765)

免责申明

如果您下载、安装、使用、修改本工具及相关代码，即表明您信任本工具。

在使用本工具时造成对您自己或他人任何形式的损失和伤害，我们不承担任何责任。

如您在使用本工具的过程中存在任何非法行为，您需自行承担相应后果，我们将不承担任何法律及连带责任。

请您务必审慎阅读、充分理解各条款内容，特别是免除或者限制责任的条款，并选择接受或不接受。

除非您已阅读并接受本协议所有条款，否则您无权下载、安装或使用本工具。

您的下载、安装、使用等行为即视为您已阅读并同意上述协议的约束。