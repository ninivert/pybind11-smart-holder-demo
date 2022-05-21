# Demo of `pybind11` polymorphic holder

In the main branch, Python classes inheriting from C++ classes are sliced when stored polymorphically (in a smart pointer, or collection).

The `smart_holder` branch prevents this. (written as of august 2021)

See also [`pybind11/README_smart_holder.rst`](https://github.com/pybind/pybind11/blob/smart_holder/README_smart_holder.rst)

I encountered this problem while developping [Swing-bye-py](https://github.com/ninivert/Swing-bye-py), and wanted to create a small reproducible example.

```py
from example_classic import Parent, Child, VecHolder

# ...

class SubChild(Child, Parent):
	def __init__(self):
		Parent.__init__(self)
		Child.__init__(self)

	def str(self):
		return "I am a SubChild, defined in python"

	def say(self):
		print("Special method from python subclass of Child")

# ...
pychild = SubChild()
# ...
vecholder = VecHolder()
# ...
vecholder.get(2).say()  # gets `pychild` and successfully calls Python's `say` method
# ...
del pychild  # C++ should have ownership, so this is OK
# ...
vecholder.get(2).say()  # gets `pychild` but raises AttributeError (pychild has been sliced)
```

## Installing `smart_holder` branch and building

WARNING : this will remove any previously `pybind11` installation. Run this preferably in a virtual env.

```sh
make install-pybind-smart_holder
```

Then build the Python modules

```sh
make build
```

## Running & demo

### Classic branch has object slicing

```sh
python test_classic.py
```

outputs

```
>>> declaring and printing Parent instance
I am a Parent
>>> declaring and printing Child instance
I am a Child
>>> declaring and printing SubChild instance
I am a SubChild, defined in python
>>> using python method from SubChild
Special method from python subclass of Child
>>> setting holder to <example_classic.Parent object at 0x7fe958563f30>
>>> getting holded
<example_classic.Parent object at 0x7fe958563f30>
I am a Parent
>>> setting holder to <example_classic.Child object at 0x7fe95828d870>
>>> getting holded
<example_classic.Child object at 0x7fe95828d870>
I am a Child
>>> setting holder to <__main__.SubChild object at 0x7fe9582856c0>
>>> getting holded
<__main__.SubChild object at 0x7fe9582856c0>
I am a SubChild, defined in python
>>> using python method from SubChild
Special method from python subclass of Child
>>> adding <example_classic.Parent object at 0x7fe958563f30> to vecholder
>>> getting vecholder index 0 (parent)
<example_classic.Parent object at 0x7fe958563f30>
I am a Parent
>>> adding <example_classic.Child object at 0x7fe95828d870> to vecholder
>>> getting vecholder index 1 (child)
<example_classic.Child object at 0x7fe95828d870>
I am a Child
>>> adding <__main__.SubChild object at 0x7fe9582856c0> to vecholder
>>> getting vecholder index 2 (pychild)
<__main__.SubChild object at 0x7fe9582856c0>
I am a SubChild, defined in python
>>> using python method from SubChild stored in VecHolder
Special method from python subclass of Child
>>> deleting pychild in python
>>> using python method from (python deleted) SubChild stored in VecHolder
<example_classic.Child object at 0x7fe95828fbb0>
I am a Parent
'example_classic.Child' object has no attribute 'say'
!!! pychild has been sliced !!!
```

### `smart_holder` branch

```sh
python test_smart_holder.py
```

outputs

```
>>> declaring and printing Parent instance
I am a Parent
>>> declaring and printing Child instance
I am a Child
>>> declaring and printing PyChild instance
I am a PyChild, defined in python
>>> using python method from PyChild
Special method from python subclass of Child
>>> setting holder to <example_smart_holder.Parent object at 0x7fa6136ce370>
>>> getting holded
<example_smart_holder.Parent object at 0x7fa6136ce370>
I am a Parent
>>> setting holder to <example_smart_holder.Child object at 0x7fa6136ce4b0>
>>> getting holded
<example_smart_holder.Child object at 0x7fa6136ce4b0>
I am a Child
>>> setting holder to <__main__.PyChild object at 0x7fa6136c5a30>
>>> getting holded
<__main__.PyChild object at 0x7fa6136c5a30>
I am a PyChild, defined in python
>>> using python method from PyChild stored in the holder
Special method from python subclass of Child
>>> adding <example_smart_holder.Parent object at 0x7fa6136ce370> to vecholder
>>> getting vecholder index 0 (parent)
<example_smart_holder.Parent object at 0x7fa6136ce370>
I am a Parent
>>> adding <example_smart_holder.Child object at 0x7fa6136ce4b0> to vecholder
>>> getting vecholder index 1 (child)
<example_smart_holder.Child object at 0x7fa6136ce4b0>
I am a Child
>>> adding <__main__.PyChild object at 0x7fa6136c5a30> to vecholder
>>> getting vecholder index 2 (pychild)
<__main__.PyChild object at 0x7fa6136c5a30>
I am a PyChild, defined in python
>>> using python method from PyChild stored in VecHolder
Special method from python subclass of Child
>>> deleting pychild in python
>>> using python method from (python deleted) PyChild stored in VecHolder
<__main__.PyChild object at 0x7fa6136c5a30>
I am a PyChild, defined in python
Special method from python subclass of Child
c++ has successfully taken ownership of the python instance without slicing !
>>> testing two layers of polymorphic inheritance
<__main__.PyChildChild object at 0x7fa6136c6890>
Special method from python subclass of Child
Another special method from python subclass of ChildChild
```