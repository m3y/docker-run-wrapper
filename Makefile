curdir = $(shell pwd)

.PHONY: install
install:
	ln -s $(curdir)/docker_run_wrapper.py /usr/local/bin/drw

.PHONY: test
test:
	python test_docker_run_wrapper.py

.PHONY: clean
clean:
	rm *.pyc
