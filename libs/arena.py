from typing import List
from rand import Rand
from data import _Followers, _Supers, _Weapons
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
        self.gd = gladiator
        self.wp = gladiator.defaultWeapon
        self.life = gladiator.lifeMax_()
        self.init = gladiator.startInit + self.seed.rand_() * 10
        self.weapons = [i.id for i in gladiator.weapons]
        self.supers = [i.id for i in gladiator.supers]
        self.team = team
        self.life_log = []


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
        pass

    def use_super(self, super: _Supers, gladiator: Glad) -> bool:
        pass
    
    def draw_weapon(self, gladiator: Glad, wp: int) -> _Weapons | None:
        pass
    
    def hold_weapon(self, gladiator: Glad) -> bool:
        pass
    
    def trash_weapon(self, gladiator: Glad) -> None:
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
            # if 

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
