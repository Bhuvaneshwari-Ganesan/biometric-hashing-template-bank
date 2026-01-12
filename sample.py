a={"name":"arun","contact":"9677419222","email":"arun@gmail.com"}

print(a)
print(type(a))
print(len(a))

for x in a:
    print(x,a[x])

a["address"]="trichy"
print(a)

a["address"]="madurai"
print(a)

a.pop("address")
print(a)

name=a.get("name")
print(name)











