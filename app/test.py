class Person:
    x = 2
    def __init__(self, name, lvl):
        self.name = name
        self.lvl = lvl
        # self.name, self.lvl = info

    def __repr__(self):
        return f"{self.name} - {self.lvl}"

    def ret(self):
        return f"{self.name} - {self.lvl}"

    @classmethod
    def class_meth(cls, info):
        name, lvl = info
        return cls(name, lvl)

    @staticmethod
    def static_meth(self):
        return f"{self.name} - {self.lvl}"

person = ['SOA', '23']


information = Person.class_meth(person)

print(information.ret())

print(Person.static_meth(information))