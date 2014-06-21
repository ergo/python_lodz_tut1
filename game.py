import logging
import random

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


class Fightable(object):
    def take_damage(self, damage):
        log.warning("damaged %s for %s" % (self, damage))
        self.health -= damage

    def attack(self):
        return random.randint(1, 10)

    def test_dodge(self):
        return self.base_agility/2 >= random.randint(1, 100)

class Hero(Fightable):
    class_endurance = 10
    class_strength = 10
    class_agility = 10


    def __init__(self, name):
        self.name = name
        self.calc_stats()
        self.health = self.max_health
        log.info("created %s" % self)

    def calc_stats(self):
        self.base_endurance = Hero.class_endurance
        self.base_strength = Hero.class_strength
        self.base_agility = Hero.class_agility
        self.max_health = self.base_endurance * 3

    def __str__(self):
        return u"""<Hero "%s", health: %s>""" % (self.name, self.health)


class FightController(object):
    def __init__(self, heroes):
        self.heroes = heroes
        self.current_hero_ix = 0

    def change_turn(self):
        self.current_hero_ix = 0 if self.current_hero_ix else 1

    def select_winner(self):
        return self.heroes[0] if self.heroes[0].health > 0 else self.heroes[1]

    @property
    def attacker(self):
        return self.heroes[self.current_hero_ix]

    @property
    def defender(self):
        return self.heroes[0 if self.current_hero_ix else 1]

    def run(self):
        while self.heroes[0].health > 0 and self.heroes[1].health > 0:
            damage = self.attacker.attack()
            if self.defender.test_dodge():
                log.info("dodged attack: %s" % self.defender)
                continue
            self.defender.take_damage(damage)
            self.change_turn()

hero = Hero("Dude1")
hero2 = Hero("Dude2")

fight_instance = FightController([hero, hero2])
fight_instance.run()
log.info('Winner is %s' % fight_instance.select_winner())