curdir = $(shell pwd)

.PHONY: install
install:
	ln -s $(curdir)/docker_run_wrapper.py /usr/local/bin/drw
