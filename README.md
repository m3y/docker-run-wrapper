# docker run wrapper
[![Build Status](https://travis-ci.org/m3y/docker-run-wrapper.svg?branch=master)](https://travis-ci.org/m3y/docker-run-wrapper)

## usage
```
$ make install
```

```
$ vim ~/.config/drw/config.toml
python = "python:3"
ghci = "haskell:latest"
mysql = "mysql:5.7"
```

```
$ drw python
Python 3.6.1 (default, Jun  8 2017, 21:43:55)
[GCC 4.9.2] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

```
$ drw ghci
GHCi, version 8.0.2: http://www.haskell.org/ghc/  :? for help
Prelude>
```
