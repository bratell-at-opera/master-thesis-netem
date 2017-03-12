# netem
Source code for master-thesis

## Requirements

**Certificate**

In order to run the tests with QUIC, you need a valid server certificate and private key for a given domain. This is due to how Chromium handles QUIC security.

**Most requirements**

To install some requirements on a Debian based system (Debian 8 "Jessie" / Ubuntu 16.04 or later):

```
sudo apt-get install openvswitch-switch ethtool xdotool xvfb python3-dev python3-virtualenv python3-pip virtualenv
```

**Caddy and node+chrome-har-capturer is requirements that must be installed separately**

- You can get Caddy by running `go get github.com/mholt/caddy/caddy` using Go >=1.7 (https://golang.org/).
- Download node 6 or 7 from https://nodejs.org/en/ and place it in PATH

## Clone

```
git clone --recursive git@github.com:hansfilipelo/netem
cd netem
```

## Download websites to load from web servers

There's an included script (`fetch-sites/fetch-sites.bash`) that populates the folder "webroot" with pages from Alexa top 500 that loads somewhat okay as static sites. Either run this or put your own site in:

```
"this-folder"/webroot/url
```

It is recommended to use this as ~/.wgetrc:

```
header = Accept-Language: en-us,en;q=0.5
header = Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
header = Connection: keep-alive
user_agent = Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0
referer = /
robots = off
```

For each entry in `config/urls.txt` netem will load `https://MY_HOSTNAME/url` from the web server.

## Get started!

```
# Remember that you need a VALID certificate for the domain
sudo ./configure --key-file=path/to/my/key --cert-file=path/to/my/cert --hostname=MY_HOSTNAME
./netem --help
sudo ./netem OPTIONS
```


