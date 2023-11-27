from rich import print as rprint
from sqlmodel import Session, select

from db import Hero, Team, engine


def select_heroes_rel():
    with Session(engine) as session:
        statement = select(Hero, Team).where(Hero.team_id == Team.id)
        results = session.exec(statement)
        for hero, team in results:
            rprint("Hero:", hero, "Team:", team)

        rprint("Using Joins...\n**********")

        statement = select(Hero, Team).join(Team)
        results = session.exec(statement)
        for hero, team in results:
            rprint("Hero:", hero, "Team:", team)

        rprint("Using Left Outer Join...\n**********")

        statement = select(Hero, Team).join(Team, isouter=True)
        results = session.exec(statement)
        for hero, team in results:
            rprint("Hero:", hero, "Team:", team)

        rprint("If we only put the Team in the .join() and not in the select() function, we would not get the team data\n**********")

        statement = select(Hero).join(Team).where(Team.name == "Preventers")
        results = session.exec(statement)
        for hero in results:
            rprint("Preventer Hero:", hero)

def select_heroes_rel_attrs_read():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == "Spider-Boy")
        result = session.exec(statement)
        hero_spider_boy = result.one()
        rprint("Spider-Boy's team again:", hero_spider_boy.team)

        statement = select(Team).where(Team.name == "Preventers")
        result = session.exec(statement)
        team_preventers = result.one()

        rprint("Preventers heroes:", team_preventers.heroes)
