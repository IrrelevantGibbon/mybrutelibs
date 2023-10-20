from typing import Any, List
from rand import Rand
from data import _Followers, _Supers, _Weapons, _WeaponType, Data, Weap, Sup
from gladiator import Gladiator
from enum import Enum, auto


class TeamStat:
    DODGE = auto()
    PARADE = auto()
    DISARM = auto()
    RIPOSTE = auto()
    COUNTER = auto()
    FOL_FRAG = auto()
    DAMAGE_MAX = auto()
    STRIKE = auto()
    MISSILE_LIGHT = auto()


class Team:
    def __init__(self, stats: List[int] = []):
        self.stats: List[int] = []


class Action:
    def __init__(self, id: int):
        self.id = id


class AddFighter(Action):
    name = "AddFighter"

    def __init__(self, id: int, team: Team, glad: Gladiator):
        super().__init__(id)
        self.team = team
        self.glad = glad


class AddFollower(Action):
    name = "AddFollower"

    def __init__(self, id: int, team: Team, follower: _Followers):
        super().__init__(id)
        self.team = team
        self.follower = follower


class MoveTo(Action):
    name = "MoveTo"

    def __init__(self, glad_id: int, opponent_id: int):
        super().__init__(glad_id)
        self.opponent_id = opponent_id


class MoveBack(Action):
    name = "MoveBack"

    def __init__(self, glad_id: int):
        super().__init__(glad_id)


class Glad:
    def __init__(self, gladiator: Gladiator, team: Team) -> None:
        self.flkeep = False
        self.retry_attack = False
        self.counter = False
        self.time_limit = None
        self.sabotage = None
        self.f_ballerina = gladiator.flBallerina
        self.status = []
        self.keep = 0.0
        self.ct = 0.25 + (20 / (10 * gladiator.speed_())) * 0.75
        self.gd: Gladiator = gladiator
        self.default_wp: Weap = Data.weapons()[0]
        self.wp: Weap = self.default_wp
        self.life = gladiator.lifeMax_()
        self.init = gladiator.startInit + gladiator.seed.rand_() * 10
        self.weapons: List[Weap] = self.get_gladiator_weapons()
        self.supers: List[Sup] = self.get_gladiator_weapons()
        self.team = team
        self.life_log = []
        self.fl_survival = gladiator.flSurvival
        self.shield_level = gladiator.shieldLevel
        self.parry = gladiator.parry

    def get_gladiator_weapons(self) -> List[Weap]:
        gladiator_weapons = []
        for weapon in self.weapons:
            for weap in Data.weapons():
                if weap.id == weapon:
                    gladiator_weapons.append(weap)
        return gladiator_weapons

    def get_gladiator_supers(self) -> List[Sup]:
        gladiator_supers = []
        for super_ in self.supers:
            for sup in Data.supers():
                if sup.id == super_:
                    gladiator_supers.append(sup)
        return gladiator_supers


class Arena:
    def __init__(self, base_seed: int) -> None:
        self.base_seed = base_seed
        self.seed: Rand
        self.current_init: float
        self.idr: int

        self.teams: list[Team] = []
        self.glads: list[Glad] = []
        self.cadavers: list[Glad] = []
        self.current_history: list[Action] = []
        self.handicap: list[int] = [0, 0]

        self.init()

    def init(self):
        self.seed = Rand(self.base_seed)
        self.idr = 0
        self.glads = []
        self.cadavers = []
        self.current_history = []
        self.teams = [Team(), Team()]

    def init_followers(self):
        for gladiator in self.glads:
            for follower in gladiator.gd.followers:
                self.add_follower(self.idr, gladiator.team, follower)
                self.idr += 1

    def add_gladiator(self, team: Team, gladiator: Gladiator):
        self.add_glad(team, gladiator)
        self.add_history(AddFighter(gladiator.id, team, gladiator))

    def add_glad(self, team: Team, glad: Gladiator):
        self.glads.append(Glad(glad, team))

    def add_follower(self, id, team, follower: _Followers):
        self.add_glad(team, Gladiator(id, None, follower))
        self.add_history(AddFollower(id, team, follower))

    def add_history(self, h: Action):
        self.current_history.append(h)

    def sort_glads_by_initiative(self):
        self.glads.sort(key=lambda x: x.init)

    def draw_super(self, gladiator: Glad, sup: int) -> _Supers | None:
        sum_ = 0
        for super_ in gladiator.supers:
            sum_ += super_.toss
        rnd = self.seed.random(sum_ + sup)
        sum_ = 0
        for super_ in gladiator.supers:
            sum_ += super_.toss
            if rnd <= sum_:
                return super_
        return None

    def use_super(self, super_: Sup, gladiator: Glad) -> bool:
        opponent = self.get_opponent(gladiator)

        match super_.id:
            case _Supers.THIEF:
                if not self.use_thief(gladiator, opponent):
                    return False
            case _Supers.BRUTE:
                if not self.use_brute(gladiator):
                    return False
            case _Supers.NET:
                self.use_net(gladiator, opponent)
            case _Supers.MEDECINE:
                if not self.use_medecine(gladiator):
                    return False
            case _Supers.BOMB:
                self.use_bomb(gladiator)
            case _Supers.GRAB:
                if not self.use_grab(gladiator, opponent):
                    return False
            case _Supers.SHOUT:
                if not self.use_shout(gladiator):
                    return False
            case _Supers.HYPNO:
                if not self.use_hypno(gladiator):
                    return False
            case _Supers.DOWNPOUR:
                self.use_downpour(gladiator, opponent)
            case _Supers.TRAPPER:
                self.use_trapper(gladiator)

        super_.use -= 1
        if super_.use == 0:
            gladiator.supers.remove(super_)
        return True

    def use_thief(self, gladiator: Glad, opponent: Glad) -> bool:
        if opponent.wp.id == opponent.default_wp.id:
            return False

        if gladiator.wp.id != gladiator.gd.defaultWeapon:
            if self.seed.random(4) > 0:
                return False
            self.trash_weapon(gladiator)

        opponent.weapons.remove(opponent.wp.id)
        gladiator.wp = opponent.wp
        gladiator.keep = 1
        gladiator.weapons.append(gladiator.wp)
        opponent.wp = opponent.default_wp
        # TODO ADD HISTORY
        opponent.init += 30 * opponent.ct
        return True

    def use_brute(self, gladiator: Glad) -> bool:
        if gladiator.status[0]:
            return False
        self.set_status(gladiator, 0, True)
        return True

    def use_net(self, gladiator: Glad, opponent: Glad) -> None:
        opponent_follower = self.get_opponent(gladiator)
        net_receiver = opponent_follower if opponent_follower is not None else opponent

        # TODO ADD HISTORY
        self.set_status(net_receiver, 1, True)

        net_receiver.init += (
            int(max(260 - pow(net_receiver.gd.force_(), 0.5) * 10, 50))
            if net_receiver.gd.fol is None
            else 100000
        )
        gladiator.init += 20 * gladiator.ct

    def use_medecine(self, gladiator: Glad) -> bool:
        damage = gladiator.gd.lifeMax_() - gladiator.life
        if damage < 50:
            return False
        life = int(damage * (0.25 * self.seed.rand_() * 0.25))
        # TODO ADD HISTORY
        gladiator.life += life
        gladiator.init += 15
        return True

    def use_bomb(self, gladiator: Glad) -> None:
        damage = 15 * self.seed.random(10)

        for opponent in self.glads:
            if opponent.team != gladiator.team:
                self.hit(opponent, damage)

        # TODO ADD HISTORY
        self.check_death()
        gladiator.init += 50 * gladiator.ct

    def use_grab(self, gladiator: Glad, opponent: Glad) -> bool:
        if gladiator.wp.id != gladiator.default_wp.id and self.seed.random(4) > 0:
            return False
        self.trash_weapon(gladiator)
        damage = self.get_grab_damage(gladiator, opponent) * 4
        damage = self.hit(opponent, damage)
        # TODO ADD HISTORY
        self.check_death()
        gladiator.init += 50 * gladiator.ct

    def use_shout(self, gladiator: Glad) -> bool:
        follower_flee = False
        for opponent_followers in self.glads:
            if (
                opponent_followers.team != gladiator.team
                and opponent_followers.gd.fol is not None
                and not opponent_followers.status[1]
                and self.seed.random(2) == 0
            ):
                self.glads.remove(opponent_followers)
                follower_flee = True
                # TODO ADD HISTORY
        return follower_flee

    def use_hypno(self, gladiator: Glad) -> bool:
        follower_hypno = False
        for opponent_followers in self.glads:
            if (
                opponent_followers.team != gladiator.team
                and opponent_followers.gd.fol is not None
                and not opponent_followers.status[1]
            ):
                opponent_followers.team = gladiator.team
                follower_hypno = True
                # TODO ADD HISTORY
        return follower_hypno

    def use_downpour(self, gladiator: Glad, opponent: Glad) -> None:
        if len(gladiator.weapons) > 2:
            weapons_to_throw = gladiator.weapons.copy()
            weapons_to_throw.remove(gladiator.wp)
            max_throw = len(weapons_to_throw) // 2
            for _ in range(max_throw):
                weapons_to_throw.pop(self.seed.random(len(weapons_to_throw)))
            damages = []
            for wp in weapons_to_throw:
                damage = int(
                    wp.deg
                    + gladiator.gd.force_() * 0.1
                    + gladiator.gd.agility_() * 0.15
                ) * (1 + self.seed.rand_() * 0.5)
                damage -= opponent.gd.armor
                if damage < 1:
                    damage = 1
                damage = self.hit(opponent, damage)
                damages.append(damage)
                gladiator.weapons.remove(wp)
            # TODO ADD HISTORY
            self.check_death()
            gladiator.init += 200 * gladiator.ct

    def use_trapper(self, gladiator: Glad) -> None:
        life_max = gladiator.gd.lifeMax_()
        if gladiator.life + 20 < life_max and len(self.cadavers) > 0:
            cad = self.cadavers.pop()
            c = 0.0
            match cad.gd.fol:
                case _Followers.DOG_0, _Followers.DOG_1, _Followers.DOG_2:
                    c = 0.2
                case _Followers.PANTHER:
                    c = 0.3
                case _Followers.BEAR:
                    c = 0.5
            heal = int(c * life_max)
            if gladiator.life + heal > life_max:
                heal = life_max - gladiator.life
            gladiator.life += heal
            gladiator.init += 15
            # TODO ADD HISTORY MOVETO
            # TODO ADD HISTORY EAT
            # TODO ADD HISTORY MOVEBACK

    def draw_weapon(self, gladiator: Glad, sup: int) -> _Weapons | None:
        if (
            self.hold_weapon(gladiator)
            and self.seed.random(len(gladiator.weapons) * 2) == 0
        ):
            return None
        sum_ = 0
        for weapon in gladiator.weapons:
            sum_ += weapon.toss
        rnd = self.seed.random(sum_ + sup)
        sum_ = 0
        for weapon in gladiator.weapons:
            sum_ += weapon.toss
            if rnd <= sum_:
                return weapon
        return None

    def hold_weapon(self, gladiator: Glad) -> bool:
        return gladiator.wp.id != gladiator.gd.defaultWeapon

    def trash_weapon(self, gladiator: Glad) -> None:
        gladiator.weapons.remove(gladiator.wp)
        ## TODO ADD HISTORY
        gladiator.wp = gladiator.default_wp

    def get_team(self, team: int, follower: bool = False) -> List[Glad]:
        team_glads = []
        for gladiator in self.glads:
            if gladiator.team == team and (
                (follower and gladiator.gd.fol is not None)
                or (not follower and gladiator.gd.fol is None)
            ):
                team_glads.append(gladiator)
        return team_glads

    def get_opponent(self, gladiator: Glad, follower: bool = False) -> Glad | None:
        opponent_team = self.get_team(1 - gladiator.team, follower)

        for opp in opponent_team:
            if opp.status[1]:
                opponent_team.remove(opp)
                break
        if len(opponent_team) == 0:
            return None
        return opponent_team[self.seed.random(len(opponent_team))]

    def throw_attacks(self, gladiator: Glad, opponent: Glad) -> None:
        damage = self.get_throw_damage(gladiator, opponent)

        if self.test_parade(gladiator, opponent, 10):
            damage = 0

        if self.test_esquive(gladiator, opponent, 2):
            damage = -1

        if damage > 0:
            damage = self.hit(opponent, damage)
            self.st(gladiator, TeamStat.STRIKE)
            self.st_dam_max(gladiator, damage)

        # TODO ADD HISTORY

        if gladiator.wp.type != _WeaponType.Throw:
            gladiator.weapons.remove(gladiator.wp)
            gladiator.wp = gladiator.default_wp
        else:
            self.st(gladiator, TeamStat.MISSILE_LIGHT)

        self.check_death()

    def test_counter(self, gladiator: Glad, opponent: Glad) -> bool:
        return (
            self.seed.rand_()
            < (opponent.gd.counter + (opponent.wp.zone - gladiator.wp.zone)) * 0.1
        )

    def test_parade(self, gladiator: Glad, opponent: Glad, c: float | None) -> bool:
        if opponent.status[1]:
            return False
        if c != 0:
            c = 1
        n = opponent.parry + opponent.wp.par - gladiator.wp.par
        return self.seed.rand_() * c < n * 0.1

    def test_esquive(self, gladiator: Glad, opponent: Glad, c: float | None) -> bool:
        if opponent.status[1]:
            return False
        if c != 0:
            c = 1

        if opponent.f_ballerina:
            opponent = False
            return True

        agg = min(max(-40, (opponent.gd.agility_() - gladiator.gd.agility_()) * 2), 40)
        n = min(
            opponent.gd.dodge
            + opponent.wp.dodge
            + agg
            - (gladiator.gd.accuracy + gladiator.wp.rap),
            90,
        )
        return self.seed.rand_() * c < n * 0.1

    def test_riposte(self, gladiator: Glad, opponent: Glad):
        if opponent.counter:
            opponent.counter = False
            return True

        n = opponent.gd.riposte + opponent.wp.rip
        return self.seed.rand_() < n * 0.1

    def st(self, gladiator: Glad, stat: Any) -> None:
        if gladiator.gl.fol is not None:
            return
        self.teams[gladiator.team].stats[stat] += 1

    def tst(self, team: int, stat: Any) -> None:
        self.teams[team].stats[stat] += 1

    def st_dam_max(self, gladiator: Glad, dam: int) -> None:
        if gladiator.gd.fol is not None:
            return
        stats = self.teams[gladiator.team].stats
        if dam > stats[TeamStat.DAMAGE_MAX]:
            stats[TeamStat.DAMAGE_MAX] = dam

    def attack(self, gladiator: Glad, opponent: Glad) -> None:
        if gladiator.life <= 0:
            return

        damage = self.get_brawl_damage(gladiator, opponent)

        if self.test_parade(gladiator, opponent, None):
            damage = 0
            self.st(opponent, TeamStat.PARADE)
            if opponent.gd.flCounter:
                opponent.counter = True

        if self.test_esquive(gladiator, opponent, None):
            damage = -1
            self.st(opponent, TeamStat.DODGE)

        sab = None
        dis = False
        dis_shield = False
        if (
            damage >= 0
            and opponent.shield_level > 0
            and gladiator.gd.disarm + gladiator.wp.dis > self.seed.random(300)
        ):
            self.st(gladiator, TeamStat.DISARM)
            dis_shield = True
            opponent.shield_level = 0
            opponent.parry -= Gladiator.SHIELD_VALUE

    def attacks(self, gladiator: Glad, opponent: Glad) -> None:
        fl_riposte = not opponent.status[1]

        self.attack(gladiator, opponent)

        combo = (
            gladiator.gd.combo + gladiator.wp.combo + gladiator.gd.agility_()
        ) * 0.01

        while self.seed.rand_() < combo or gladiator.retry_attack:
            if opponent.counter:
                break
            combo *= 0.5
            gladiator.retry_attack = False
            self.attack(gladiator, opponent)

        self.check_death()
        if fl_riposte and self.test_riposte(gladiator, opponent):
            self.st(gladiator, TeamStat.RIPOSTE)
            self.attack(opponent, gladiator)

    def set_status(self, gladiator: Glad, sid: int, flag: bool) -> None:
        gladiator.status[sid] = flag
        # TODO ADD HISTORY

    def hit(self, gladiator: Glad, damage: int) -> int:
        if gladiator.status[1]:
            self.remove_net(gladiator)

        if gladiator.gd.flIncrevable:
            max = round(gladiator.gd.lifeMax_() / 5)
            if damage > max:
                damage = max
                # TODO ADD HISTORY

        gladiator.life -= damage

        if gladiator.fl_survival and gladiator.life <= 0:
            gladiator.life = 1
            gladiator.fl_survival = False

        gladiator.life_log.append(damage)
        return damage

    def remove_net(self, gladiator: Glad) -> None:
        self.set_status(gladiator, 1, False)
        gladiator.init = self.current_init + 50

    def get_grab_damage(self, gladiator: Glad, opponent: Glad | None) -> int:
        damage = int(
            (10 + gladiator.gd.force_() * 0.6) * (0.8 + self.seed.rand_() * 0.4)
        )
        if gladiator.status[0]:
            damage *= 2
        if opponent is not None:
            damage -= opponent.gd.armor
        if damage < 1:
            damage = 1
        return damage

    def get_brawl_damage(self, gladiator: Glad, opponent: Glad | None) -> int:
        coef = 0.2 + gladiator.wp.deg * 0.05
        damage = (gladiator.wp.deg + gladiator.gd.force_() * coef) * (
            0.8 + self.seed.rand_() * 0.4
        )
        if gladiator.status[0]:
            damage *= 2
        damage *= gladiator.gd.damageCoef[gladiator.wp.dt]

        if opponent is not None:
            if opponent.gd.flLeadBones and gladiator.wp.dt == 4:
                damage *= 0.7
                damage -= opponent.gd.armor

        if damage < 1:
            damage = 1
        return int(damage)

    def get_throw_damage(self, gladiator: Glad, opponent: Glad | None) -> int:
        damage = int(
            gladiator.wp.ged
            + gladiator.gd.force_() * 0.1
            + gladiator.gd.agility_() * 0.15
        ) * (1 + self.seed.rand_() * 0.5)
        if opponent is not None:
            damage -= opponent.gd.armor
        if damage < 1:
            damage = 1
        return damage

    def get_main_glad(self, team: int) -> Glad:
        for gladiator in self.glads:
            if gladiator.team == team and gladiator.gd.fol is None:
                return gladiator

    def is_alive(self, team: int) -> bool:
        return self.get_main_glad(team).life > 0

    def action(self, gladiator: Glad):
        super_ = self.draw_super(gladiator, 10)
        if super_ is not None and self.use_super(super_, gladiator):
            return

        if self.hold_weapon(gladiator):
            gladiator.flkeep = True

        weapon_ = self.draw_weapon(gladiator, 10)
        if self.seed.rand_() < gladiator.keep:
            gladiator.keep *= 0.5
            weapon_ = None

        if weapon_ is not None and weapon_ != gladiator.wp:
            gladiator.flkeep = False
            if self.hold_weapon(gladiator):
                self.trash_weapon(gladiator)
            gladiator.wp = weapon_
            gladiator.keep = 0.5
            sab = gladiator.wp == gladiator.sabotage
            if sab:
                gladiator.weapons.remove(gladiator.wp)
                gladiator.wp = gladiator.default_wp
                gladiator.init += 100
                gladiator.sabotage = None
                return

        opponent = self.get_opponent(gladiator)
        attack_type = gladiator.wp.type
        if (
            gladiator.wp.type == _WeaponType.Brawl
            and gladiator.flkeep
            and self.hold_weapon(gladiator)
            and self.seed.random(gladiator.wp.deg) == 0
        ):
            attack_type = _WeaponType.Throw

        match attack_type:
            case _WeaponType.Brawl:
                self.add_history(MoveTo(gladiator.gd.id, opponent.gd.id))

                if not opponent.status[1] and self.test_counter(gladiator, opponent):
                    self.st(opponent, 1)  # TODO COUNTER
                    self.attack(gladiator, opponent)
                    return
                else:
                    self.attacks(gladiator, opponent)

                if gladiator.life <= 0:
                    self.add_history(MoveBack(gladiator.gd.id))

                self.add_history(MoveBack(gladiator.gd.id))
            case _WeaponType.Throw:
                self.throw_attacks(gladiator, opponent)

        tp = gladiator.wp.tempo * gladiator.ct + self.seed.random(10)
        if gladiator.gd.flHeavyArms and gladiator.wp.dt == 4:
            tp *= 0.75

        gladiator.init += tp

        if gladiator.status[0]:
            self.set_status(gladiator, 0, False)

    def fight(self):
        self.init_followers()

        for gladiator in self.glads:
            gladiator.init += self.handicap[gladiator.team]

        for _ in range(1000):
            self.sort_glads_by_initiative()
            self.current_init = self.glads[0].init
            self.check_death()
            if self.check_end():
                self.end_fight()
                break

    def check_death(self):
        pass

    def check_end(self):
        pass

    def end_fight(self):
        pass
