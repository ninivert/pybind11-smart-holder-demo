from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension

ext_modules = [
	Pybind11Extension(
		'example_classic',
		['pybind_classic.cpp']
	),
	Pybind11Extension(
		'example_smart_holder',
		['pybind_smart_holder.cpp']
	)
]

setup(
	ext_modules=ext_modules
)
