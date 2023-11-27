from db import engine, Hero, Team
from sqlmodel import Session, select
from rich import print as rprint


def update_heroes_del_rel():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == "Spider-Boy")
        result = session.exec(statement)
        hero_spider_boy = result.one()

        hero_spider_boy.team = None
        session.add(hero_spider_boy)
        session.commit()

        session.refresh(hero_spider_boy)
        rprint("Spider-Boy without team:", hero_spider_boy)