import sqlalchemy as sa
from rich import print as rprint
from sqlmodel import Session, col, or_, select

import m_2_m
from create import create_heroes, create_heroes_rel, create_heroes_rel_attrs  # noqa: F401
from db import Hero, Team, create_db_and_tables, drop_tables, engine, get_tables
from del_rel_attrs import update_heroes_del_rel  # noqa: F401
from select_queries import select_heroes_rel, select_heroes_rel_attrs_read  # noqa: F401


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


def update_heroes():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == "Spider-Boy")
        results1 = session.exec(statement)
        hero = results1.one()
        rprint("Hero:", hero)

        statement = select(Hero).where(Hero.name == "Captain North America")
        results2 = session.exec(statement)
        hero_2 = results2.one()
        rprint("Hero 2:", hero_2)

        hero.age = 16
        session.add(hero)

        hero_2.name = "Captain North America Except Canada"
        hero_2.age = 110
        session.add(hero_2)
        session.commit()

        session.refresh(hero)
        session.refresh(hero_2)

        rprint("Updated hero 1 :", hero)
        rprint("Updated hero 2:", hero_2)


def update_heroes_2():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == "Spider-Boy")
        results = session.exec(statement)
        hero_1 = results.one()
        print("Hero 1:", hero_1)

        statement = select(Hero).where(Hero.name == "Captain North America")
        results = session.exec(statement)
        hero_2 = results.one()
        print("Hero 2:", hero_2)

        hero_1.age = 16
        hero_1.name = "Spider-Youngster"
        session.add(hero_1)

        hero_2.name = "Captain North America Except Canada"
        hero_2.age = 110
        session.add(hero_2)

        session.commit()
        session.refresh(hero_1)
        session.refresh(hero_2)

        print("Updated hero 1:", hero_1)
        print("Updated hero 2:", hero_2)


def delete_heroes():
    update_heroes_2()
    with Session(engine) as session:
        rprint(session.exec(select(Hero)).all())
        statement = select(Hero).where(Hero.name == "Spider-Youngster")
        results = session.exec(statement)
        hero = results.one()
        rprint("Hero: ", hero)

        session.delete(hero)
        session.commit()

        rprint("Deleted hero:", hero)

        statement = select(Hero).where(Hero.name == "Spider-Youngster")
        results = session.exec(statement)
        hero = results.first()

        if hero is None:
            print("There's no hero named Spider-Youngster")


def update_heroes_rel():
    with Session(engine) as session:
        hero_spider_boy = session.get(Hero, 3)
        team_preventers = session.get(Team, 1)
        rprint(f"{hero_spider_boy} <-> {team_preventers} ")
        hero_spider_boy.team_id = team_preventers.id
        session.add(hero_spider_boy)
        session.commit()
        session.refresh(hero_spider_boy)
        rprint("Updated hero:", hero_spider_boy)


def update_heroes_rel_remove():
    """
    Remove Data Connections
    """
    with Session(engine) as session:
        hero_spider_boy = session.get(Hero, 3)

        hero_spider_boy.team_id = None
        session.add(hero_spider_boy)
        session.commit()
        session.refresh(hero_spider_boy)
        rprint("No longer Preventer:", hero_spider_boy)


def main():
    # drop_tables()
    # create_db_and_tables()
    get_tables()
    # create_heroes()
    # select_heroes()
    # update_heroes()
    # delete_heroes()
    # create_heroes_rel()
    # select_heroes_rel()
    # update_heroes_rel()
    # update_heroes_rel_remove()
    # create_heroes_rel_attrs()
    # select_heroes_rel_attrs_read()
    # update_heroes_del_rel()
    # m_2_m.create.create_heroes_m2m()
    # m_2_m.update_heroes()
    # m_2_m.link_model.create_heroes()
    m_2_m.link_model.update_heroes()

if __name__ == "__main__":
    main()
