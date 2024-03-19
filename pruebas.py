class User():
    #datos de la tabla users:id, name, email, password, remember_me, is_Admin los dos ultimos booleanos
    def __init__(self, name, email, password,remember_me, is_Admin):
        self.id = 0
        self.name = name
        self.email = email
        self.password = password
        self.remember_me = remember_me
        self.is_Admin = is_Admin


users = []

user12  = User('juan','email','password',True,False)
users.append(user12)
user123  = User(' juan','email','password',True,False)
users.append(user123)
print(users)
if any(user.name == 'juan' for user in users):
    print('si')