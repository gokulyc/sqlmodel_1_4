from db import engine, Hero, Team
from sqlmodel import Session, select
from rich import print as rprint


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