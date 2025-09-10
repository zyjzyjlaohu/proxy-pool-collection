# ProxyPool

![build](https://github.com/Python3WebSpider/ProxyPool/workflows/build/badge.svg)
![deploy](https://github.com/Python3WebSpider/ProxyPool/workflows/deploy/badge.svg)
![](https://img.shields.io/badge/python-3.6%2B-brightgreen)
![Docker Pulls](https://img.shields.io/docker/pulls/germey/proxypool)

简易高效的代理池，提供如下功能：

- 定时抓取免费代理网站，简易可扩展。
- 使用 Redis 对代理进行存储并对代理可用性进行排序。
- 定时测试和筛选，剔除不可用代理，留下可用代理。
- 提供代理 API，随机取用测试通过的可用代理。

代理池原理解析可见「[如何搭建一个高效的代理池](https://cuiqingcai.com/7048.html)」，建议使用之前阅读。

## 使用前注意

本代理池是基于市面上各种公开代理源搭建的，所以可用性并不高，很可能上百上千个代理中才能找到一两个可用代理，不适合直接用于爬虫爬取任务。

如果您的目的是为了尽快使用代理完成爬取任务，建议您对接一些付费代理或者直接使用已有代理资源；如果您的目的是为了学习如何搭建一个代理池，您可以参考本项目继续完成后续步骤。

付费代理推荐：

- [ADSL 拨号代理](https://platform.acedata.cloud/documents/a82a528a-8e32-4c4c-a9d0-a21be7c9ef8c)：海量拨号（中国境内）高质量代理
- [海外/全球代理](https://platform.acedata.cloud/documents/50f1437a-1857-43c5-85cf-5800ae1b31e4)：中国境外高质量代理
- [蜂窝 4G/5G 代理](https://platform.acedata.cloud/documents/1cc59b19-1550-4169-a59d-ad6faf7f7517)：极高质量（中国境内）防风控代理

## 使用准备

首先当然是克隆代码并进入 ProxyPool 文件夹：

```
git clone https://github.com/Python3WebSpider/ProxyPool.git
cd ProxyPool
```

然后选用下面 Docker 和常规方式任意一个执行即可。

## 使用要求

可以通过两种方式来运行代理池，一种方式是使用 Docker（推荐），另一种方式是常规方式运行，要求如下：

### Docker

如果使用 Docker，则需要安装如下环境：

- Docker
- Docker-Compose

安装方法自行搜索即可。

官方 Docker Hub 镜像：[germey/proxypool](https://hub.docker.com/r/germey/proxypool)

### 常规方式

常规方式要求有 Python 环境、Redis 环境，具体要求如下：

- Python>=3.6
- Redis

## Docker 运行

如果安装好了 Docker 和 Docker-Compose，只需要一条命令即可运行。

```shell script
docker-compose up
```

运行结果类似如下：

```
redis        | 1:M 19 Feb 2020 17:09:43.940 * DB loaded from disk: 0.000 seconds
redis        | 1:M 19 Feb 2020 17:09:43.940 * Ready to accept connections
proxypool    | 2020-02-19 17:09:44,200 CRIT Supervisor is running as root.  Privileges were not dropped because no user is specified in the config file.  If you intend to run as root, you can set user=root in the config file to avoid this message.
proxypool    | 2020-02-19 17:09:44,203 INFO supervisord started with pid 1
proxypool    | 2020-02-19 17:09:45,209 INFO spawned: 'getter' with pid 10
proxypool    | 2020-02-19 17:09:45,212 INFO spawned: 'server' with pid 11
proxypool    | 2020-02-19 17:09:45,216 INFO spawned: 'tester' with pid 12
proxypool    | 2020-02-19 17:09:46,596 INFO success: getter entered RUNNING state, process has stayed up for > than 1 seconds (startsecs)
proxypool    | 2020-02-19 17:09:46,596 INFO success: server entered RUNNING state, process has stayed up for > than 1 seconds (startsecs)
proxypool    | 2020-02-19 17:09:46,596 INFO success: tester entered RUNNING state, process has stayed up for > than 1 seconds (startsecs)
```

可以看到 Redis、Getter、Server、Tester 都已经启动成功。

这时候访问 [http://localhost:5555/random](http://localhost:5555/random) 即可获取一个随机可用代理。

如果下载速度特别慢，可以自行修改 Dockerfile，修改：

```diff
- RUN pip install -r requirements.txt
+ RUN pip install -r requirements.txt -i https://pypi.douban.com/simple
```

## 常规方式运行

如果不使用 Docker 运行，配置好 Python、Redis 环境之后也可运行，步骤如下。

### Windows环境下的运行方式
