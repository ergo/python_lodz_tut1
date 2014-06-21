# AUTHOR: Radomir Dopieralski
# Thx

import logging
import random


logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


class Fighting(object):
    def __init__(self, base_agility, base_strength):
        self.base_agility = base_agility
        self.base_strength = base_strength

    def attack(self, attackee):
        ferocity = random.randint(1, 100) * 2
        if not attackee.fighting.defend(ferocity):
            damage = random.randint(1, 10)
            log.warning("damaged %s for %s" % (attackee, damage))
            attackee.life.take_damage(damage)
        else:
            log.info("dodged attack: %s" % attackee)

    def defend(self, ferocity):
        return self.base_agility >= ferocity


class Life(object):
    def __init__(self, max_health):
        self.max_health = max_health
        self.health = max_health

    def is_alive(self):
        return self.health > 0

    def take_damage(self, damage):
        self.health -= damage


class Hero(object):
    class_endurance = 10
    class_strength = 10
    class_agility = 10

    def __init__(self, name):
        self.name = name
        self.life = Life(self.class_endurance * 3)
        self.fighting = Fighting(self.class_agility, self.class_strength)
        log.info("created %s" % self)

    def __str__(self):
        return u"""<Hero "%s", health: %s>""" % (self.name, self.life.health)


class FightController(object):
    def __init__(self, heroes):
        self.heroes = heroes
        self.attacker = heroes[0]

    def other_hero(self, hero):
        for other_hero in self.heroes:
            if hero != other_hero and other_hero.life.is_alive():
                break
        return other_hero

    def select_winner(self):
        for hero in self.heroes:
            if hero.life.is_alive():
                break
        return hero

    def continue_combat(self):
        return all(hero.life.is_alive() for hero in self.heroes)

    def run(self):
        while self.continue_combat():
            defender = self.other_hero(self.attacker)
            self.attacker.fighting.attack(defender)
            self.attacker = defender


combat = FightController([
    Hero("Krwawy Urlyk"),
    Hero("Helmut Straszliwy"),
    ])
combat.run()
log.info('The winner is %s' % combat.select_winner())
