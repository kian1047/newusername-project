class User :
    def __init__(self,username,password,role=""):
        self.username = username.strip()
        self.password = password.strip()
        self.role = role


    def __str__(self):
        return f"username: {self.username},role: {self.role}"


class Item:
    def __init__(self,name,quantity,price,category):
        self.n = name.strip()
        self.q = float(quantity)
        self.p = float(price)
        self.c = category.strip()

    def __str__(self):
        return f"Name: {self.n},Ouantity: {self.q},Price{self.p},category{self.c}"
    def to_tuple(self):
        return (self.n,self.q,self.p,self.c)