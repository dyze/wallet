class Test:
	pass
	

instance1 = Test()

instance2 = "Test"


print(type(instance1))

print(type(instance2))

print(isinstance(instance1, Test))

print(isinstance(instance2, Test))

if isinstance(instance1, Test):
	print('instance1 is of type Test')
	
	