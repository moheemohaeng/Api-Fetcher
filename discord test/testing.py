class testing:
    def __init__(self) -> None:
        self.a = 50
        self.b = 30
        self.c : int = 0
    
    def add(self, a, b):
        self.c = a+b
        print('abced')
    
te = testing()
te.add(3,4)
print(te.c)

