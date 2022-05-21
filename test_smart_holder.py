from example_smart_holder import Parent, Child, ChildChild, Holder, VecHolder, print_poly

print('>>> declaring and printing Parent instance')
parent = Parent()
print_poly(parent)

print('>>> declaring and printing Child instance')
child = Child()
print_poly(child)

# IMPORTANT : THE PYTHON CLASS MUST INHERIT FROM **ALL** THE C++ PARENT CLASSES
class PyChild(Child, Parent):
	def __init__(self):
		Parent.__init__(self)
		Child.__init__(self)

	def str(self):
		return "I am a PyChild, defined in python"

	def say(self):
		print("Special method from python subclass of Child")

print('>>> declaring and printing PyChild instance')
pychild = PyChild()
print_poly(pychild)

print('>>> using python method from PyChild')
pychild.say()

print(f'>>> setting holder to {parent}')
holder = Holder()
holder.set(parent)

print('>>> getting holded')
print(holder.get())
print_poly(holder.get())

print(f'>>> setting holder to {child}')
holder = Holder()
holder.set(child)

print('>>> getting holded')
print(holder.get())
print_poly(holder.get())

print(f'>>> setting holder to {pychild}')
holder = Holder()
holder.set(pychild)

print('>>> getting holded')
print(holder.get())
print_poly(holder.get())

print('>>> using python method from PyChild stored in the holder')
holder.get().say()

print(f'>>> adding {parent} to vecholder')
vecholder = VecHolder()
vecholder.add(parent)

print('>>> getting vecholder index 0 (parent)')
print(vecholder.get(0))
print_poly(vecholder.get(0))

print(f'>>> adding {child} to vecholder')
vecholder.add(child)

print('>>> getting vecholder index 1 (child)')
print(vecholder.get(1))
print_poly(vecholder.get(1))

print(f'>>> adding {pychild} to vecholder')
vecholder.add(pychild)

print('>>> getting vecholder index 2 (pychild)')
print(vecholder.get(2))
print_poly(vecholder.get(2))

print('>>> using python method from PyChild stored in VecHolder')
vecholder.get(2).say()

print('>>> deleting pychild in python')
del pychild

print('>>> using python method from (python deleted) PyChild stored in VecHolder')
print(vecholder.get(2))
print_poly(vecholder.get(2))
got_err = False
try:
	vecholder.get(2).say()
except AttributeError as err:
	got_err = True
	print(err)
	print('!!! pychild has been sliced !!!')
if not got_err:
	print('c++ has successfully taken ownership of the python instance without slicing !')


print('>>> testing two layers of polymorphic inheritance')

class PyChildChild(ChildChild, Child, Parent):
	def __init__(self):
		Parent.__init__(self)
		Child.__init__(self)
		ChildChild.__init__(self)

	def str(self):
		return "I am a PyChildChild, defined in python"

	def say(self):
		print("Special method from python subclass of Child")

	def talk(self):
		print("Another special method from python subclass of ChildChild")

pychilchild = PyChildChild()
holder.set(pychilchild)
print(holder.get())
holder.get().say()
holder.get().talk()
