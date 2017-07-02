# docker run wrapper
[![Build Status](https://travis-ci.org/m3y/docker-run-wrapper.svg?branch=master)](https://travis-ci.org/m3y/docker-run-wrapper)

## usage
```
$ drw config  # vim starts
python = "python:3"
ghci = "haskell:latest"
ghc = "haskell:latest"
mysql = "mysql:5.7"
```

```
$ drw -s python
docker run --rm -it -w /drw/ -v $(pwd):/drw/ python:3 python
```

```
$ drw python
Python 3.6.1 (default, Jun  8 2017, 21:43:55)
[GCC 4.9.2] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

```
$ drw mysql -h HOST -u USER -p DATABASE
Enter password:
```

```
$ drw ghci
GHCi, version 8.0.2: http://www.haskell.org/ghc/  :? for help
Prelude>
```

```
$ drw 'ghc --make helloworld.hs && ./helloworld'
[1 of 1] Compiling Main             ( helloworld.hs, helloworld.o )
Linking helloworld ...
Hello, world
```
- use haskell:latest

## Installation

```
$ git clone git@github.com:m3y/docker-run-wrapper.git
$ cd docker-run-wrapper
$ make install
```

#### Mac OS X / Homebrew

```
$ brew tap m3y/drw
$ brew install drw
```
