from rich import print as rprint
from sqlmodel import Session, select

from db import Hero, Team, engine


def update_heroes():
    with Session(engine) as session:
        hero_spider_boy = session.exec(select(Hero).where(Hero.name == "Spider-Boy")).one()
        rprint(f"Teams : {session.exec(select(Team)).all()}")
        team_z_force = session.exec(select(Team).where(Team.name == "Z-Force")).one()

        team_z_force.heroes.append(hero_spider_boy)
        session.add(team_z_force)
        session.commit()

        rprint("Updated Spider-Boy's Teams:", hero_spider_boy.teams)
        rprint("Z-Force heroes:", team_z_force.heroes)

        hero_spider_boy.teams.remove(team_z_force)
        session.add(team_z_force)
        session.commit()

        rprint("Reverted Z-Force's heroes:", team_z_force.heroes)
        rprint("Reverted Spider-Boy's teams:", hero_spider_boy.teams)
