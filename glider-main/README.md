# glider

[![Go Version](https://img.shields.io/github/go-mod/go-version/nadoo/glider?style=flat-square)](https://go.dev/dl/)
[![Go Report Card](https://goreportcard.com/badge/github.com/nadoo/glider?style=flat-square)](https://goreportcard.com/report/github.com/nadoo/glider)
[![GitHub release](https://img.shields.io/github/v/release/nadoo/glider.svg?style=flat-square&include_prereleases)](https://github.com/nadoo/glider/releases)
[![Actions Status](https://img.shields.io/github/actions/workflow/status/nadoo/glider/build.yml?branch=dev&style=flat-square)](https://github.com/nadoo/glider/actions)
[![DockerHub](https://img.shields.io/docker/image-size/nadoo/glider?color=blue&label=docker&style=flat-square)](https://hub.docker.com/r/nadoo/glider)

glider is a forward proxy with multiple protocols support, and also a dns/dhcp server with ipset management features(like dnsmasq).

we can set up local listeners as proxy servers, and forward requests to internet via forwarders.

```bash
                |Forwarder ----------------->|
   Listener --> |                            | Internet
                |Forwarder --> Forwarder->...|
```

## Features
- Act as both proxy client and proxy server(protocol converter)
- Flexible proxy & protocol chains
- Load balancing with the following scheduling algorithm:
  - rr: round robin
  - ha: high availability 
  - lha: latency based high availability
  - dh: destination hashing
- Rule & priority based forwarder choosing: [Config Examples](config/examples)
- DNS forwarding server:
  - dns over proxy
  - force upstream querying by tcp
  - association rules between dns and forwarder choosing
  - association rules between dns and ipset
  - dns cache support
  - custom dns record
- IPSet management (linux kernel version >= 2.6.32):
  - add ip/cidrs from rule files on startup
  - add resolved ips for domains from rule files by dns forwarding server
- Serve http and socks5 on the same port
- Periodical availability checking for forwarders
- Send requests from specific local ip/interface
- Services: 
  - dhcpd: a simple dhcp server that can run in failover mode

## Protocols

<details>
<summary>click to see details</summary>

|Protocol       | Listen/TCP |  Listen/UDP | Forward/TCP | Forward/UDP | Description
|:-:            |:-:|:-:|:-:|:-:|:-|
|Mixed          |√|√| | |http+socks5 server|
|HTTP           |√| |√| |client & server|
|SOCKS5         |√|√|√|√|client & server|
|SS             |√|√|√|√|client & server|
|Trojan         |√|√|√|√|client & server|
|Trojanc        |√|√|√|√|trojan cleartext(without tls)|
|VLESS          |√|√|√|√|client & server|
|VMess          | | |√|√|client only|
|SSR            | | |√| |client only|
|SSH            | | |√| |client only|
|SOCKS4         | | |√| |client only|
|SOCKS4A        | | |√| |client only|
|TCP            |√| |√| |tcp tunnel client & server|
|UDP            | |√| |√|udp tunnel client & server|
|TLS            |√| |√| |transport client & server|
|KCP            | |√|√| |transport client & server|
|Unix           |√|√|√|√|transport client & server|
|VSOCK          |√| |√| |transport client & server|
|Smux           |√| |√| |transport client & server|
|Websocket(WS)  |√| |√| |transport client & server|
|WS Secure      |√| |√| |websocket secure (wss)|
|Proxy Protocol |√| | | |version 1 server only|
|Simple-Obfs    | | |√| |transport client only|
|Redir          |√| | | |linux redirect proxy|
|Redir6         |√| | | |linux redirect proxy(ipv6)|
|TProxy         | |√| | |linux tproxy(udp only)|
|Reject         | | |√|√|reject all requests|

</details>

## Install

- Binary: [https://github.com/nadoo/glider/releases](https://github.com/nadoo/glider/releases)
- Docker: `docker pull nadoo/glider`
- Manjaro: `pamac install glider`
- ArchLinux: `sudo pacman -S glider`
- Homebrew: `brew install glider`
- MacPorts: `sudo port install glider`
- Source: `go install github.com/nadoo/glider@latest`