from typing import Any, List
from rand import Rand
from data import _Followers, _Supers, _Weapons, _WeaponType, Data, Weap, Sup
from gladiator import Gladiator


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
        self.ct = 0.25 + (20 / (10 * gladiator.speed)) * 0.75
        self.gd: Gladiator = gladiator
        self.default_wp: Weap = Data.weapons()[0]
        self.wp: Weap = self.default_wp
        self.life = gladiator.lifeMax_()
        self.init = gladiator.startInit + gladiator.seed.rand_() * 10
        self.weapons: List[Weap] = self.get_gladiator_weapons()
        self.supers: List[Sup] = self.get_gladiator_weapons()
        self.team = team
        self.life_log = []

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
            int(max(260 - pow(net_receiver.gd.force, 0.5) * 10, 50))
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
        pass

    def draw_weapon(self, gladiator: Glad, wp: int) -> _Weapons | None:
        pass

    def hold_weapon(self, gladiator: Glad) -> bool:
        pass

    def trash_weapon(self, gladiator: Glad) -> None:
        pass

    def get_opponent(self, gladiator: Glad, follower: bool = False) -> Glad:
        pass

    def throw_attacks(self, gladiator: Glad, opponent: Glad) -> None:
        pass

    def test_counter(self, gladiator: Glad, opponent: Glad) -> bool:
        pass

    def st(self, opponent: Glad, stat: Any) -> bool:
        pass

    def attack(self, gladiator: Glad, opponent: Glad) -> None:
        pass

    def attacks(self, gladiator: Glad, opponent: Glad) -> None:
        pass

    def set_status(self, gladiator: Glad, sid: int, flag: bool) -> None:
        pass

    def hit(self, opponent: Glad, damage: int) -> int:
        pass

    def get_grab_damage(self, gladiator: Glad, opponent: Glad) -> int:
        pass

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

    def check_death(self):
        pass

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

    def check_end(self):
        pass

    def end_fight(self):
        pass
