#include <memory>
#include <vector>
#include <string>
#include <iostream>
#include <pybind11/smart_holder.h>

namespace py = pybind11;

struct Parent {
	Parent() = default;
	virtual ~Parent() = default;

	virtual std::string str() const {
		return "I am a Parent";
	}
};

struct Child : public Parent {
	Child() = default;
	virtual ~Child() = default;

	virtual std::string str() const override {
		return "I am a Child";
	}
};

struct ChildChild : public Child {
	ChildChild() = default;
	virtual ~ChildChild() = default;

	virtual std::string str() const override {
		return "I am a ChildChild";
	}
};

class PyParent : public Parent, public py::trampoline_self_life_support {
public:
	using Parent::Parent;

	virtual std::string str() const override {
		PYBIND11_OVERRIDE(std::string, Parent, str);
	}
};

class PyChild : public Child, public py::trampoline_self_life_support {
public:
	using Child::Child;

	virtual std::string str() const override {
		PYBIND11_OVERRIDE(std::string, Child, str);
	}
};

class PyChildChild : public ChildChild, public py::trampoline_self_life_support {
public:
	using ChildChild::ChildChild;

	virtual std::string str() const override {
		PYBIND11_OVERRIDE(std::string, ChildChild, str);
	}
};

class Holder {
	std::shared_ptr<Parent> ptr;

public:
	Holder() = default;

	void set(std::shared_ptr<Parent> new_ptr) {
		ptr = new_ptr;
	}
	std::shared_ptr<Parent> get() const {
		return ptr;
	}
};

class VecHolder {
	std::vector<std::shared_ptr<Parent>> ptrs;

public:
	VecHolder() = default;

	void add(std::shared_ptr<Parent> new_ptr) {
		ptrs.push_back(new_ptr);
	}
	std::shared_ptr<Parent> get(unsigned int index) const {
		return ptrs[index];
	}
};


void print_poly(std::shared_ptr<Parent> const ptr) {
	std::cout << ptr->str() << std::endl;
}

PYBIND11_SMART_HOLDER_TYPE_CASTERS(Parent)
PYBIND11_SMART_HOLDER_TYPE_CASTERS(Child)
PYBIND11_SMART_HOLDER_TYPE_CASTERS(ChildChild)

PYBIND11_MODULE(example_smart_holder, m) {
	py::classh<Parent, PyParent>(m, "Parent")
		.def(py::init<>());

	py::classh<Child, PyChild, Parent>(m, "Child")
		.def(py::init<>());

	py::classh<ChildChild, PyChildChild, Child, Parent>(m, "ChildChild")
		.def(py::init<>());

	py::class_<Holder>(m, "Holder")
		.def(py::init<>())
		.def("set", &Holder::set)
		.def("get", &Holder::get);

	py::class_<VecHolder>(m, "VecHolder")
		.def(py::init<>())
		.def("add", &VecHolder::add)
		.def("get", &VecHolder::get);

	m.def("print_poly", &print_poly);
}
