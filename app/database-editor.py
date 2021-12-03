from main import db, Shirt
import pprint

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
    pprint.pprint(Shirt.query.all())

def data():
    image = input("Zadej cestu k fotce: ")
    imageCart = input("Zadej cestu k fotce v košíku: ")
    name = input("Zadej název: ")
    description = input("Zadej popis: ")
    color = input("Zadej barvu: ")
    size = input("Zadej velikost: ")
    cost = input("Zadej cenu: ")
    stock = input("Kolik toho je na skladě: ")
    collection = input("V jaké je to kolekci:")
    return image,imageCart,name,description,color,size,cost,stock,collection

def clear():
    Shirt.query.delete()
    db.session.commit()
    print("Vymazáno")

def change():
    print(Shirt.query.all())
    id = int(input("Vyber ID:"))
    shirt = Shirt.query.filter_by(id=id).all()
    print(shirt)
    image,imageCart,name,description,color,size,cost,stock,collection = data()
    if image != "":
        shirt[0].image = image
    if imageCart != "":
        shirt[0].imageCart = imageCart;
    if name != "":
        shirt[0].name = name
    if description != "":
        shirt[0].description = description
    if color != "":
        shirt[0].color = color
    if size != "":
        shirt[0].size = size
    if cost != "":
        shirt[0].cost = cost
    if stock != "":
        shirt[0].stock = stock
    if collection != "":
        shirt[0].collection = collection
    print(shirt)
    db.session.commit()

def add():
    image,imageCart,name,description,color,size,cost,stock,collection = data()
    shirt = Shirt(image=image,imageCart=imageCart,name=name,description=description,color=color,size=size,cost=cost,stock=stock,collection=collection)
    db.session.add(shirt)
    db.session.commit()
    print("Úspěšně přidáno")
    print(Shirt.query.filter_by(name=name).one())


if __name__ == '__main__':
    main()