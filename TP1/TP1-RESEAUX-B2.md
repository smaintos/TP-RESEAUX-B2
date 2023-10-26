TP1-RESEAUX-B2

***TP1 : Maîtrise réseau du poste***
--------------

TP1 : Maîtrise réseau du poste
I. Basics
II. Go further
III. Le requin


--------------

***I. Basics***



☀️ Carte réseau WiFi

``` 
(base) ➜  ~ ifconfig

en0: flags=8863<UP,BROADCAST,SMART,RUNNING,SIMPLEX,MULTICAST> mtu 1500
	options=6460<TSO4,TSO6,CHANNEL_IO,PARTIAL_CSUM,ZEROINVERT_CSUM>
	ether fc:e2:6c:0f:cb:24 ( <- adresse mac)
	inet6 fe80::85b:9dc6:a32f:fe02%en0 prefixlen 64 secured scopeid 0xc 
	inet 10.33.76.197 ( <-adresse ip)netmask 0xfffff000 broadcast 10.33.79.255
	nd6 options=201<PERFORMNUD,DAD>
	media: autoselect
	status: active
````


```
(base) ➜  ~ ifconfig en0 | grep "inet\|netmask"

	inet6 fe80::145a:3f01:8f1f:e30b%en0 prefixlen 64 secured scopeid 0xc 
	inet 10.33.76.197 netmask 0xfffff000 broadcast 10.33.79.255/20
```

☀️ Déso pas déso

* l'adresse de réseau du LAN auquel vous êtes connectés en WiFi

10.33.76.197 ET 255.255.0.0 = 10.33.0.0

10.33.79.255 ET 255.255.0.0 = 10.33.0.0

Il y a 4094 adresses IP disponibles.

☀️ Hostname

* déterminer le hostname de votre PC

```
(base) ➜  ~ hostname
MacBook-Air-de-smaintos.local
```
☀️ Passerelle du réseau

☀️ Serveur DHCP et DNS

* l'adresse IP de la passerelle du réseau

```
(base) ➜  ~ ipconfig getpacket en0 | grep server_identifier

server_identifier (ip): 10.33.79.254
```

et

* l'adresse MAC de la passerelle du réseau

```
(base) ➜  ~ scutil --dns | grep 'nameserver\[[0-9]*\]'

  nameserver[0] : 8.8.8.8
  nameserver[1] : 1.1.1.1
  nameserver[0] : 8.8.8.8
  nameserver[1] : 1.1.1.1 
```

☀️ Table de routage

* dans votre table de routage, laquelle est la route par défaut

```
(base) ➜  ~ netstat -nr | grep default

default            10.33.79.254       UGScg                 en0  
```
------------------

***II. Go further***

☀️ Hosts ?

* faites en sorte que pour votre PC, le nom b2.hello.vous corresponde à l'IP 1.1.1.1

* prouvez avec un ping b2.hello.vous que ça ping bien 1.1.1.1

```
(base) ➜  ~ ping b2.hello.vous
PING b2.hello.vous (1.1.1.1): 56 data bytes
64 bytes from 1.1.1.1: icmp_seq=0 ttl=57 time=53.900 ms
64 bytes from 1.1.1.1: icmp_seq=1 ttl=57 time=77.933 ms
64 bytes from 1.1.1.1: icmp_seq=2 ttl=57 time=111.531 ms
64 bytes from 1.1.1.1: icmp_seq=3 ttl=57 time=18.905 ms
64 bytes from 1.1.1.1: icmp_seq=4 ttl=57 time=192.853 ms
^C
--- b2.hello.vous ping statistics ---
5 packets transmitted, 5 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 18.905/91.024/192.853/59.229 ms
```

☀️ Go mater une vidéo youtube et déterminer, pendant qu'elle tourne...


* l'adresse IP du serveur auquel vous êtes connectés pour regarder la vidéo

Source Address: 91.68.245.12

* le port du serveur auquel vous êtes connectés

port 443

* le port que votre PC a ouvert en local pour se connecter au port du serveur distant

port 57207

☀️ Requêtes DNS

* à quelle adresse IP correspond le nom de domaine www.ynov.com

```
(base) ➜  ~ ping ynov.com
PING ynov.com (104.26.11.233): 56 data bytes
64 bytes from 104.26.11.233: icmp_seq=0 ttl=57 time=14.319 ms
64 bytes from 104.26.11.233: icmp_seq=1 ttl=57 time=19.209 ms
64 bytes from 104.26.11.233: icmp_seq=2 ttl=57 time=18.501 ms
64 bytes from 104.26.11.233: icmp_seq=3 ttl=57 time=25.455 ms
64 bytes from 104.26.11.233: icmp_seq=4 ttl=57 time=14.266 ms
64 bytes from 104.26.11.233: icmp_seq=5 ttl=57 time=22.431 ms
^C
--- ynov.com ping statistics ---
6 packets transmitted, 6 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 14.266/19.030/25.455/4.042 ms
```

* à quel nom de domaine correspond l'IP 174.43.238.89

Nom de domaine : 89.sub-174-43-238.myvzw.com


☀️ Hop hop hop

* par combien de machines vos paquets passent quand vous essayez de joindre www.ynov.com

```
(base) ➜  ~ traceroute ynov.com

traceroute: Warning: ynov.com has multiple addresses; using 104.26.10.233
traceroute to ynov.com (104.26.10.233), 64 hops max, 52 byte packets
 1  10.33.79.254 (10.33.79.254)  84.327 ms  19.959 ms  6.770 ms
 2  145.117.7.195.rev.sfr.net (195.7.117.145)  24.364 ms  22.264 ms  19.870 ms
 3  * * *
 4  196.224.65.86.rev.sfr.net (86.65.224.196)  287.132 ms  6.733 ms  6.589 ms
 5  12.148.6.194.rev.sfr.net (194.6.148.12)  18.279 ms
    68.150.6.194.rev.sfr.net (194.6.150.68)  14.745 ms  16.319 ms
 6  68.150.6.194.rev.sfr.net (194.6.150.68)  12.866 ms  19.478 ms  236.507 ms
 7  141.101.67.48 (141.101.67.48)  21.390 ms  15.268 ms  33.977 ms
 8  172.71.120.4 (172.71.120.4)  17.787 ms
    141.101.67.54 (141.101.67.54)  17.958 ms
    172.71.128.4 (172.71.128.4)  17.127 ms
 9  104.26.10.233 (104.26.10.233)  13.872 ms  13.048 ms  12.342 ms
```
☀️ IP publique

```
(base) ➜  ~ curl ifconfig.me
195.7.117.146% 
```


☀️ Scan réseau


* combien il y a de machines dans le LAN auquel vous êtes connectés
* 
```
 (base) ➜  ~ nmap -sP 10.33.76.197
Starting Nmap 7.93 ( https://nmap.org ) at 2023-10-19 16:34 CEST
Nmap scan report for 10.33.76.197
Host is up (0.00040s latency).
Nmap done: 1 IP address (1 host up) scanned in 0.23 seconds
(base) ➜  ~ nmap -sP 10.33.76.197/20
Starting Nmap 7.93 ( https://nmap.org ) at 2023-10-19 16:35 CEST
Stats: 0:06:14 elapsed; 0 hosts completed (0 up), 4096 undergoing Ping Scan
Ping Scan Timing: About 17.13% done; ETC: 17:11 (0:30:14 remaining)
Stats: 0:06:14 elapsed; 0 hosts completed (0 up), 4096 undergoing Ping Scan
Ping Scan Timing: About 17.14% done; ETC: 17:11 (0:30:12 remaining)
```

***III. Le requin***

☀️ Capture ARP (repo)
☀️ Capture DNS (repo)

(base) ➜  ~ nslookup ynov.com
Server:		8.8.8.8
Address:	8.8.8.8#53

Non-authoritative answer:
Name:	ynov.com
Address: 104.26.11.233
Name:	ynov.com
Address: 104.26.10.233
Name:	ynov.com
Address: 172.67.74.226

☀️ Capture TCP (repo)


