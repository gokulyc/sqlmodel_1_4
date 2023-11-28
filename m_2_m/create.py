from rich import print as rprint
from sqlmodel import Session

from db import Hero, Team, engine


def create_heroes_m2m():
    with Session(engine) as session:
        team_preventers = Team(name="Preventers", headquarters="Sharp Tower")
        team_z_force = Team(name="Z-Force", headquarters="Sister Margaret’s Bar")

        hero_deadpond = Hero(
            name="Deadpond",
            secret_name="Dive Wilson",
            teams=[team_z_force, team_preventers],
        )
        hero_rusty_man = Hero(
            name="Rusty-Man",
            secret_name="Tommy Sharp",
            age=48,
            teams=[team_preventers],
        )
        hero_spider_boy = Hero(
            name="Spider-Boy", secret_name="Pedro Parqueador", teams=[team_preventers]
        )
        session.add(hero_deadpond)
        session.add(hero_rusty_man)
        session.add(hero_spider_boy)
        session.commit()

        session.refresh(hero_deadpond)
        session.refresh(hero_rusty_man)
        session.refresh(hero_spider_boy)

        rprint("Deadpond:", hero_deadpond)
        rprint("Deadpond teams:", hero_deadpond.teams)
        rprint("Rusty-Man:", hero_rusty_man)
        rprint("Rusty-Man Teams:", hero_rusty_man.teams)
        rprint("Spider-Boy:", hero_spider_boy)
        rprint("Spider-Boy Teams:", hero_spider_boy.teams)
