.PHONY: build test

classic: build test-classic
smart_holder: build test-smart_holder

build:
	python setup.py build_ext --inplace

test-classic:
	python test_classic.py

test-smart_holder:
	python test_smart_holder.py

install-pybind-smart_holder:
	sudo pip uninstall pybind11
	git clone --branch smart_holder https://github.com/pybind/pybind11.git
	cd pybind11; \
	sudo python setup.py install
