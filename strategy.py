class wolf(object): 
    def bark(self):
        print "hooooowll"

class dog(object): 
    def bark(self):
        print "woof"


def barkforme(dogtype):
    dogtype.bark()


my_dog = dog()
my_wolf = wolf()
barkforme(my_dog)
barkforme(my_wolf)

class Animal:
    def __init__(self, name):    # Constructor of the class
        self.name = name
    def talk(self):              # Abstract method, defined by convention only
        raise NotImplementedError("Subclass must implement abstract method")
 
class Cat(Animal):
    def talk(self):
        return 'Meow!'
 
class Dog(Animal):
    def talk(self):
        return 'Woof! Woof!'
 
animals = [Cat('Missy'),
           Dog('Lassie')]
 
for animal in animals:
    print(animal.name + ': ' + animal.talk())
 
 
# prints the following:
# Missy: Meow!
# Lassie: Woof! Woof!
