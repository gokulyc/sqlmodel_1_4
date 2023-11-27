from typing import Optional

from sqlmodel import Field, Session, SQLModel, create_engine, select, or_, col
from rich import print as rprint
import sqlalchemy as sa

class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None, index=True)


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# engine = create_engine(sqlite_url, echo=True)
engine = create_engine(sqlite_url)

def drop_tables():
    SQLModel.metadata.reflect(engine)
    SQLModel.metadata.drop_all(engine)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def print_objs(objs: list[SQLModel]):
    for i, obj in enumerate(objs):
        print(f"Hero {i}:", obj)


def create_heroes():
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
    hero_3 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)
    hero_4 = Hero(name="Tarantula", secret_name="Natalia Roman-on", age=32)
    hero_5 = Hero(name="Black Lion", secret_name="Trevor Challa", age=35)
    hero_6 = Hero(name="Dr. Weird", secret_name="Steve Weird", age=36)
    hero_7 = Hero(name="Captain North America", secret_name="Esteban Rogelios", age=93)

    with Session(engine) as session:
        session.add(hero_1)
        session.add(hero_2)
        session.add(hero_3)
        session.add(hero_4)
        session.add(hero_5)
        session.add(hero_6)
        session.add(hero_7)
        print("After adding to the session")
        print_objs([hero_1, hero_2, hero_3])
        session.commit()
        print("After committing the session")
        print_objs([hero_1, hero_2, hero_3])

        print("After committing the session, show IDs")
        print("Hero 1 ID:", hero_1.id)
        print("Hero 2 ID:", hero_2.id)
        print("Hero 3 ID:", hero_3.id)

        print("After committing the session, show names")
        print("Hero 1 name:", hero_1.name)
        print("Hero 2 name:", hero_2.name)
        print("Hero 3 name:", hero_3.name)

        session.refresh(hero_1)
        session.refresh(hero_2)
        session.refresh(hero_3)

        print("After refreshing the heroes")
        print("Hero 1:", hero_1)
        print("Hero 2:", hero_2)
        print("Hero 3:", hero_3)

    print("After the session closes")
    print_objs([hero_1, hero_2, hero_3])


def select_heroes():
    with Session(engine) as sess:
        statement = select(Hero).where(Hero.name == "Deadpond")
        statement2 = select(Hero).where(Hero.name != "Deadpond")
        rprint(f"Exp : {Hero.name == 'Deadpond'}")
        results = sess.exec(statement)
        # for hero in results:
        #     rprint(hero)
        heroes = results.all()
        rprint(heroes)

        results = sess.exec(statement2)
        heroes = results.all()
        rprint(heroes)

        statement3 = select(Hero).where(Hero.age > 35)
        results = sess.exec(statement3)
        rprint(f"{str(statement3)} \n ------------------------")
        for hero in results:
            rprint(hero)

        statement4 = select(Hero).where(Hero.age >= 35)
        results = sess.exec(statement4)
        rprint(f"{str(statement4)} \n ------------------------")
        for hero in results:
            rprint(hero)

        statement5 = select(Hero).where(Hero.age < 35)
        results = sess.exec(statement5)
        rprint(f"{str(statement5)} \n ------------------------")
        for hero in results:
            rprint(hero)

        statement6 = select(Hero).where(Hero.age <= 35)
        results = sess.exec(statement6)
        rprint(f"{str(statement6)} \n ------------------------")
        for hero in results:
            rprint(hero)

        statement7 = select(Hero).where(Hero.age >= 35).where(Hero.age < 40)
        # statement7 = select(Hero).where(Hero.age >= 35, Hero.age < 40)
        results = sess.exec(statement7)
        rprint(f"{str(statement7)} \n ------------------------")
        for hero in results:
            rprint(hero)

        statement8 = select(Hero).where(or_(Hero.age >= 35, Hero.age < 40))
        results = sess.exec(statement8)
        rprint(f"{str(statement8)} \n ------------------------")
        for hero in results:
            rprint(hero)
        
        statement9 = select(Hero).where(col(Hero.age) >= 35)
        results = sess.exec(statement9)
        rprint(f"{str(statement9)} \n ------------------------")
        for hero in results:
            rprint(hero)

        #  Read one Row 0<= rows <=1

        statement10 = select(Hero).where(col(Hero.age) >= 95)
        results = sess.exec(statement10)
        rprint(f"{str(statement10)} \n ------------------------")
        hero = results.first()
        rprint(f"Hero: {hero}")

        #  Read one Row rows=1
        statement11 = select(Hero).where(col(Hero.age) >= 95)
        results = sess.exec(statement11)
        rprint(f"{str(statement11)} \n ------------------------")
        try:
            hero = results.one()
        except sa.exc.NoResultFound as e:
            rprint(f"Warning : {e}")
        else:
            rprint(f"Hero: {hero}")
        
        # Select by Id
        statement12 = select(Hero).where(Hero.id == 1)
        results = sess.exec(statement12)
        hero = results.first()
        rprint("Hero:", hero)

        # Select by Id with .get()
        hero = sess.get(Hero, 1)
        rprint("Hero:", hero)
        hero = sess.get(Hero, 99)
        rprint("Hero:", hero)
        # LIMIT and OFFSET
        statement13 = select(Hero).limit(3).offset(3)
        results = sess.exec(statement13)
        heroes = results.all()
        rprint(heroes)

        statement14 = select(Hero).limit(3).offset(6)
        results = sess.exec(statement14)
        heroes = results.all()
        rprint(heroes)

def main():
    # drop_tables()
    # create_db_and_tables()
    # create_heroes()
    select_heroes()


if __name__ == "__main__":
    main()
