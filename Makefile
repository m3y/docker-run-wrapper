curdir = $(shell pwd)

.PHONY: install
install:
	ln -s $(curdir)/bin/drw /usr/local/bin/drw

.PHONY: test
test:
	@mv drw drw.py
	python test_docker_run_wrapper.py
	@mv drw.py drw
