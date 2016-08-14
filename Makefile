filename = pasgens

compile: setup.py $(filename).c
	python setup.py build
	find -path "./build/*.so" | xargs cp -t .

install: setup.py
	python setup.py install

clean: build
	rm -R build
