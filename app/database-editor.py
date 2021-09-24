from main import db, Shirt

def main():
    print("Chceš měnit nebo přidat ?")
    choice = int(input("1. Měnit, 2. Přidat \n3. Smazat databázi, 4. Vypsat celou databázi: "))
    if choice == 1:
        change()
    elif choice == 2:
        add()
    elif choice == 3:
        clear()
    elif choice == 4:
        print_database()
    else:
        print("FUCK U")
        exit(1)

def print_database():
    print(Shirt.query.all())

def data():
    name = input("Zadej název: ")
    color = input("Zadej barvu: ")
    size = input("Zadej velikost: ")
    cost = int(input("Zadej cenu: "))
    stock = int(input("Kolik toho je na skladě: "))
    collection = input("V jaké je to kolekci:")
    return name,color,size,cost,stock,collection

def clear():
    Shirt.query.delete()
    db.session.commit()
    print("Vymazáno")

def change():
    print(Shirt.query.all())
    id = int(input("Vyber ID:"))
    shirt = Shirt.query.filter_by(id=id).all()
    print(shirt)
    name,color,size,cost,stock,collection = data()
    shirt[0].name = name
    shirt[0].color = color
    shirt[0].size = size
    shirt[0].cost = cost
    shirt[0].stock = stock
    shirt[0].collection = collection
    print(shirt)
    db.session.commit()

def add():
    name,color,size,cost,stock,collection = data()
    shirt = Shirt(name=name,color=color,size=size,cost=cost,stock=stock,collection=collection)
    db.session.add(shirt)
    db.session.commit()
    print("Úspěšně přidáno")
    print(Shirt.query.filter_by(name=name).one())


if __name__ == '__main__':
    main()