class MyClass:
    def execute(self, funid):
        self.a[funid](self)
    def print_hello(self):
        print("Hello")
    def print_bye(self):
        print("Bye")
    a = {"h":print_hello, "b": print_bye}
    
        
    
myclass = MyClass()
myclass.execute("h")