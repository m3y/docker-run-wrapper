curdir = $(shell pwd)

.PHONY: install
install:
	ln -s $(curdir)/drw /usr/local/bin/drw

.PHONY: test
test:
	@mv drw drw.py
	python test_drw.py
	@mv drw.py drw
