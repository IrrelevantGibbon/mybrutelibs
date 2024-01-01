import random

from rand import Rand
from data import (
    _Followers,
    _Permanent,
    _Supers,
    _Weapons,
    _Bonus,
    Data,
    Fol,
    Permanent,
    Super,
    Weapons,
    Followers,
)
import data


class LvlUp:
    bonus: _Bonus | None
    caracs: list[int]

    def __init__(self, caracs: list[int], bonus: _Bonus | None = None):
        self.bonus = bonus
        self.caracs = caracs


class Gladiator:
    SHIELD_VALUE = 45  # static variable

    def __init__(self):
        self.flSurvival = False
        self.flVandalism = False
        self.flHeavyArms = False
        self.flLeadBones = False
        self.flBallerina = False
        self.flStayer = False
        self.flIncrevable = False
        self.flCounter = False
        self.flIronHead = False

        self.lvl = 0
        self.xp = 0
        self.id = 0

        self.name = ""

        self.fol = None  # _Followers

        self.force = 2
        self.agility = 2
        self.speed = 2
        self.lifeMax = 2

        self.multiForce = 1.0
        self.multiAgility = 1.0
        self.multiSpeed = 1.0
        self.multiLifeMax = 1.0

        self.startInit = 0
        self.counter = 0
        self.riposte = 0

        self.combo = 0
        self.armor = 0

        self.parry = 0
        self.dodge = 0
        self.disarm = 0
        self.accuracy = 0

        self.armorLevel = 0
        self.shieldLevel = 0
        self.stanceId = 0

        self.smid = 0

        self.defaultWeapon = _Weapons.HANDS  # _Weapons
        self.lastBonus = None  # _Bonus
        self.lastCarac = 0

        self.damageCoef = [1.0, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        self.bonus = []
        self.weapons = []
        self.followers = []
        self.supers = []

        self.bonusWeight = []  # list of dicts with id:_Bonus and w:Int
        self.caracWeight = []
        self.totalBonusWeight = 0

        self.seed: Rand  # using Python's random as a substitute for mt.Rand

        self.win = 0
        self.lose = 0

    def new(self, seed_id, name: str, fol=None):
        self.id = seed_id
        self.name = name
        self.fol = fol

        self.seed = Rand(0)
        self.seed.init_seed(seed_id)

        if fol != None:
            self.init_follower(fol)
            return

        self.init_destiny()
        self.init_caracs()
        return self

    def init_destiny(self):
        if self.seed.random(1000) == 0:
            self.stanceId = self.seed.random(2)

        self.caracWeight = [0, 0, 1, 1, 2, 2, 3, 3]
        for _ in range(3):
            self.caracWeight.append(self.seed.random(4))

        for i in Data.bonus_weights():
            self.bonusWeight.append({"id": i.id, "w": i.w})
            self.totalBonusWeight += i.w

        if self.seed.random(3) > 0:
            self.set_weight(Super(_Supers.THIEF), 0)
        if self.seed.random(3) > 0:
            self.set_weight(Super(_Supers.DOWNPOUR), 0)
        if self.seed.random(3) > 0:
            self.set_weight(Super(_Supers.HYPNO), 0)
        if self.seed.random(6) > 0:
            self.set_weight(Permanent(_Permanent.IMMORTALITY), 0)

        # RARE WEAPONS
        for wid in Data.rare_weapons():
            if self.seed.random(4) > 0:
                self.set_weight(Weapons(wid), 0)

        # INCAPACITY
        weapons_incapacities = Data.possible_incapacity_weapons()
        max_ = self.seed.random(3)
        for i in range(max_):
            self.set_weight(
                Weapons(
                    weapons_incapacities[self.seed.random(len(weapons_incapacities))]
                ),
                0,
            )

    def init_caracs(self):
        for _ in range(2):
            self.carac_up(
                self.caracWeight[self.seed.random(len(self.caracWeight))],
                self.seed.random(4),
            )

    def carac_up(self, c, inc):
        match c:
            case 0:
                self.force += inc
            case 1:
                self.agility += inc
            case 2:
                self.speed += inc
            case 3:
                self.lifeMax += inc

    def init_follower(self, followers: _Followers):
        datas: Fol = Data.followers()[followers._value_ - 1]

        self.lvl = 0
        self.damageCoef = [1.0, 1, 1, 1, 1, 1, 1, 1, 1, 1]

        self.bonus = []
        self.weapons = []
        self.followers = []
        self.supers = []

        self.force = datas.force
        self.agility = datas.agility
        self.speed = datas.speed
        self.lifeMax = datas.life_max

        self.armor = 0

        self.counter = datas.counter
        self.riposte = datas.riposte
        self.combo = datas.combo
        self.parry = datas.parry
        self.dodge = datas.dodge
        self.startInit = datas.init

        self.disarm = 0
        self.accuracy = 0

        self.defaultWeapon = datas.dw

    def set_weight(self, id, w):
        for i in self.bonusWeight:
            if i["id"].id == id.id:
                self.totalBonusWeight += w - i["w"]
                i["w"] = w
                return

    def win_game(self):
        self.xp += 3
        self.win += 1
        lvl_xp = self.can_level_up()
        if lvl_xp >= 0:
            self.next_level()
            self.xp = lvl_xp

    def lose_game(self):
        self.xp += 1
        self.lose += 1
        if self.can_level_up() >= 0:
            self.next_level()

    def can_level_up(self):
        return self.xp - self.lvl * 1.5 + 1

    def next_level(self):
        self.xp = 0
        self.lvl += 1

        up = self.get_level_up()

        bit = self.seed.random(2)

        if bit == 0 or bit == 1 and up.bonus is None:
            if len(up.caracs) == 1:
                self.carac_up(up.caracs[0], 3)
            else:
                self.carac_up(up.caracs[0], 2)
                self.carac_up(up.caracs[1], 1)
        else:
            self.seed.add_seed(self.seed.random(10007) + 131)
            self.add_bonus(up.bonus)

    def get_level_up(self) -> LvlUp:
        c0 = self.seed.random(4)
        bonus = None

        if self.lvl < 80 or self.seed.random(self.lvl) < 80:
            k = self.seed.random(self.totalBonusWeight)
            for i in self.bonusWeight:
                k -= i["w"]
                if k < 0:
                    bonus = i["id"]
                    break

            for bid in self.bonus:
                if bid.id == bonus.id:
                    bonus = None
                    break
        if bonus is not None:
            return LvlUp([c0], bonus)
        c1 = (c0 + 1 + self.seed.random(3)) % 4
        return LvlUp([c0, c1])

    def force_(self):
        return int(self.force * self.multiForce)

    def agility_(self):
        return int(self.agility * self.multiAgility)

    def speed_(self):
        return int(self.speed * self.multiSpeed)

    def lifeMax_(self):
        return 50 + int(self.lifeMax * self.multiLifeMax) + self.lvl

    def add_bonus(self, bonus):
        self.lastBonus = bonus
        self.bonus.append(bonus)

        mult = 1.5
        inc = 3

        match type(bonus):
            case data.Permanent:
                match bonus.id:
                    case _Permanent.SUPER_FORCE:
                        self.force += inc
                        self.multiForce += mult
                        self.set_weight(Permanent(bonus.id), 0)
                    case _Permanent.SUPER_AGILITY:
                        self.agility += inc
                        self.multiAgility += mult
                        self.set_weight(Permanent(bonus.id), 0)
                    case _Permanent.SUPER_SPEED:
                        self.speed += inc
                        self.multiSpeed += mult
                        self.set_weight(Permanent(bonus.id), 0)
                    case _Permanent.SUPER_LIFE:
                        self.lifeMax += inc
                        self.multiLifeMax += mult
                        self.set_weight(Permanent(bonus.id), 0)
                    case _Permanent.IMMORTALITY:
                        self.multiLifeMax *= 3.5
                        self.multiForce *= 0.75
                        self.multiAgility *= 0.75
                        self.multiSpeed *= 0.75
                    case _Permanent.BLADE_MASTER:
                        self.damageCoef[1] += 0.5
                    case _Permanent.BRAWL_MASTER:
                        self.damageCoef[0] += 1.0
                    case _Permanent.VIGILANCE:
                        self.counter += 1
                    case _Permanent.PUGNACITY:
                        self.riposte += 30
                    case _Permanent.TWISTER:
                        self.combo += 20
                    case _Permanent.SHIELD:
                        self.parry += self.SHIELD_VALUE
                        self.shieldLevel = 1
                    case _Permanent.ARMOR:
                        self.armor += 1
                        self.multiSpeed *= 0.9
                        self.armorLevel += 1
                    case _Permanent.LEATHER_SKIN:
                        self.armor += 2
                    case _Permanent.UNTOUCHABLE:
                        self.dodge += 30
                    case _Permanent.VANDALISM:
                        self.flVandalism = True
                    case _Permanent.CHOC:
                        self.disarm += 50
                    case _Permanent.BLUNT_MASTER:
                        self.flHeavyArms = True
                    case _Permanent.MERCILESS:
                        self.accuracy += 30
                    case _Permanent.SURVIVAL:
                        self.flSurvival = True
                    case _Permanent.LEAD_BONES:
                        self.flLeadBones = True
                    case _Permanent.BALLERINA:
                        self.flBallerina = True
                    case _Permanent.STAYER:
                        self.flStayer = True
                    case _Permanent.WARM_BLOODED:
                        self.startInit -= 200
                    case _Permanent.INCREVABLE:
                        self.flIncrevable = True
                    case _Permanent.DIESEL:
                        self.speed += 5
                        self.multiSpeed *= 2.5
                        self.startInit += 200
                    case _Permanent.COUNTER:
                        self.flCounter = True
                        self.parry += 10
                    case _Permanent.IRON_HEAD:
                        self.flIronHead = True
            case data.Super:
                self.supers.append(bonus)
            case data.Weapons:
                self.weapons.append(bonus)
            case data.Followers:
                self.followers.append(bonus)
                match bonus.id:
                    case _Followers.DOG_0:
                        self.lifeMax -= 2
                    case _Followers.DOG_1:
                        self.lifeMax -= 2
                    case _Followers.DOG_2:
                        self.lifeMax -= 2
                    case _Followers.PANTHER:
                        self.lifeMax -= 6
                    case _Followers.BEAR:
                        self.lifeMax -= 8

                if self.lifeMax < 0:
                    self.lifeMax = 1
                if self.seed.random(1000) > 0:
                    if bonus.id == _Followers.PANTHER:
                        self.set_weight(Followers(_Followers.PANTHER), 0)
                    if bonus.id == _Followers.BEAR:
                        self.set_weight(Followers(_Followers.BEAR), 0)
