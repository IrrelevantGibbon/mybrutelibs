from enum import Enum, auto


class _Supers(Enum):
    THIEF = auto()
    BRUTE = auto()
    MEDECINE = auto()
    NET = auto()
    BOMB = auto()
    GRAB = auto()
    SHOUT = auto()
    HYPNO = auto()
    DOWNPOUR = auto()
    TRAPPER = auto()


class _Followers(Enum):
    DOG_0 = auto()
    DOG_1 = auto()
    DOG_2 = auto()
    PANTHER = auto()
    BEAR = auto()


class _Weapons(Enum):
    HANDS = auto()
    KNIFE = auto()
    SWORD = auto()
    LANCE = auto()
    STICK = auto()
    TRIDENT = auto()
    AXE = auto()
    SCIMETAR = auto()
    HAMMER = auto()
    BIG_SWORD = auto()
    FAN = auto()
    SHURIKEN = auto()
    FANGS = auto()
    WOOD_CLUB = auto()
    IRON_CLUB = auto()
    BONE_CLUB = auto()
    FLAIL = auto()
    WHIP = auto()
    SAI = auto()
    POIREAU = auto()
    MUG = auto()
    POELE = auto()
    POUSSIN = auto()
    HALBERD = auto()
    TROMBONNE = auto()
    KEYBOARD = auto()
    NOODLES = auto()
    RACKET = auto()


class _Permanent(Enum):
    SUPER_FORCE = auto()
    SUPER_AGILITY = auto()
    SUPER_SPEED = auto()
    SUPER_LIFE = auto()
    IMMORTALITY = auto()
    BLADE_MASTER = auto()
    BRAWL_MASTER = auto()
    VIGILANCE = auto()
    PUGNACITY = auto()
    TWISTER = auto()
    SHIELD = auto()
    ARMOR = auto()
    LEATHER_SKIN = auto()
    UNTOUCHABLE = auto()
    VANDALISM = auto()
    CHOC = auto()
    BLUNT_MASTER = auto()
    MERCILESS = auto()
    SURVIVAL = auto()
    LEAD_BONES = auto()
    BALLERINA = auto()
    STAYER = auto()
    WARM_BLOODED = auto()
    INCREVABLE = auto()
    DIESEL = auto()
    COUNTER = auto()
    IRON_HEAD = auto()


class _Status(Enum):
    ST_BRUTE = auto()
    ST_NET = auto()


class _WeaponType(Enum):
    Throw = auto()
    Brawl = auto()


class _StrikeType(Enum):
    Fist = auto()
    Slash = auto()
    Estoc = auto()
    Whip = auto()


class BonusSlot:
    def __init__(self, data):
        self.id = data["id"]
        self.w = data["w"]


class _Bonus:
    def __init__(self, id):
        self.id = id


class Permanent(_Bonus):
    pass


class Super(_Bonus):
    pass


class Followers(_Bonus):
    pass


class Weapons(_Bonus):
    pass


class Weap:
    def __init__(self, data):
        self.id = data["id"]
        self.toss = data["toss"]
        self.deg = data["deg"]
        self.tempo = data["tempo"]
        self.rip = data["rip"]
        self.zone = data["zone"]
        self.rap = data["rap"]
        self.dod = data["dod"]
        self.per = data["per"]
        self.par = data["par"]
        self.combo = data["combo"]
        self.dt = data["dt"]
        self.dis = data["dis"]
        self.type = data["type"]
        self.anim = data["anim"]


class Sup:
    def __init__(self, data):
        self.id = data["id"]
        self.toss = data["toss"]
        self.use = data["use"]


class Data:
    @staticmethod
    def weapons():
        return [
            Weap(
                {
                    "id": _Weapons.HANDS,
                    "toss": 10,
                    "deg": 5,
                    "tempo": 120,
                    "rip": 0,
                    "zone": 0,
                    "rap": 20,
                    "dod": 10,
                    "per": 0,
                    "par": -25,
                    "dis": 5,
                    "combo": 0,
                    "type": _WeaponType.Brawl,
                    "anim": _StrikeType.Fist,
                    "dt": 0,
                }
            ),
            Weap(
                {
                    "id": _Weapons.KNIFE,
                    "toss": 5,
                    "deg": 7,
                    "tempo": 60,
                    "rip": 0,
                    "zone": 0,
                    "rap": 50,
                    "dod": 10,
                    "per": 0,
                    "par": 0,
                    "dis": 0,
                    "combo": 30,
                    "type": _WeaponType.Brawl,
                    "anim": _StrikeType.Estoc,
                    "dt": 1,
                }
            ),
            Weap(
                {
                    "id": _Weapons.SWORD,
                    "toss": 5,
                    "deg": 10,
                    "tempo": 120,
                    "rip": 10,
                    "zone": 1,
                    "rap": 0,
                    "dod": 0,
                    "per": 0,
                    "par": 15,
                    "dis": 15,
                    "combo": 0,
                    "type": _WeaponType.Brawl,
                    "anim": _StrikeType.Slash,
                    "dt": 1,
                }
            ),
            Weap(
                {
                    "id": _Weapons.LANCE,
                    "toss": 2,
                    "deg": 12,
                    "tempo": 120,
                    "rip": -10,
                    "zone": 3,
                    "rap": 0,
                    "dod": 0,
                    "per": 0,
                    "par": 0,
                    "dis": 10,
                    "combo": 0,
                    "type": _WeaponType.Brawl,
                    "anim": _StrikeType.Estoc,
                    "dt": 2,
                }
            ),
            Weap(
                {
                    "id": _Weapons.STICK,
                    "toss": 3,
                    "deg": 6,
                    "tempo": 100,
                    "rip": 30,
                    "zone": 3,
                    "rap": 0,
                    "dod": 5,
                    "per": 0,
                    "par": 25,
                    "dis": 25,
                    "combo": 10,
                    "type": _WeaponType.Brawl,
                    "anim": _StrikeType.Estoc,
                    "dt": 2,
                }
            ),
            Weap(
                {
                    "id": _Weapons.TRIDENT,
                    "toss": 3,
                    "deg": 14,
                    "tempo": 140,
                    "rip": 5,
                    "zone": 3,
                    "rap": 0,
                    "dod": 0,
                    "per": 0,
                    "par": 0,
                    "dis": 20,
                    "combo": 0,
                    "type": _WeaponType.Brawl,
                    "anim": _StrikeType.Estoc,
                    "dt": 2,
                }
            ),
            Weap(
                {
                    "id": _Weapons.AXE,
                    "toss": 3,
                    "deg": 17,
                    "tempo": 150,
                    "rip": 0,
                    "zone": 1,
                    "rap": 0,
                    "dod": 0,
                    "per": 0,
                    "par": -10,
                    "dis": 0,
                    "combo": 0,
                    "type": _WeaponType.Brawl,
                    "anim": _StrikeType.Slash,
                    "dt": 3,
                }
            ),
            Weap(
                {
                    "id": _Weapons.SCIMETAR,
                    "toss": 3,
                    "deg": 10,
                    "tempo": 80,
                    "rip": 0,
                    "zone": 1,
                    "rap": 20,
                    "dod": 0,
                    "per": 0,
                    "par": 10,
                    "dis": 0,
                    "combo": 15,
                    "type": _WeaponType.Brawl,
                    "anim": _StrikeType.Slash,
                    "dt": 1,
                }
            ),
            Weap(
                {
                    "id": _Weapons.HAMMER,
                    "toss": 5,
                    "deg": 55,
                    "tempo": 230,
                    "rip": -20,
                    "zone": 1,
                    "rap": -30,
                    "dod": -40,
                    "per": 50,
                    "par": -50,
                    "dis": 10,
                    "combo": -40,
                    "type": _WeaponType.Brawl,
                    "anim": _StrikeType.Slash,
                    "dt": 4,
                }
            ),
            Weap(
                {
                    "id": _Weapons.BIG_SWORD,
                    "toss": 5,
                    "deg": 28,
                    "tempo": 180,
                    "rip": 0,
                    "zone": 2,
                    "rap": -10,
                    "dod": -20,
                    "per": -20,
                    "par": 0,
                    "dis": 10,
                    "combo": 0,
                    "type": _WeaponType.Brawl,
                    "anim": _StrikeType.Slash,
                    "dt": 1,
                }
            ),
            Weap(
                {
                    "id": _Weapons.FAN,
                    "toss": 5,
                    "deg": 4,
                    "tempo": 28,
                    "rip": 50,
                    "zone": 0,
                    "rap": 50,
                    "dod": 60,
                    "per": 0,
                    "par": -50,
                    "dis": -50,
                    "combo": 45,
                    "type": _WeaponType.Brawl,
                    "anim": _StrikeType.Slash,
                    "dt": 5,
                }
            ),
            Weap(
                {
                    "id": _Weapons.SHURIKEN,
                    "toss": 5,
                    "deg": 3,
                    "tempo": 12,
                    "rip": 0,
                    "zone": 0,
                    "rap": 0,
                    "dod": 15,
                    "per": 0,
                    "par": -10,
                    "dis": -50,
                    "combo": 30,
                    "type": _WeaponType.Throw,
                    "anim": _StrikeType.Fist,
                    "dt": 6,
                }
            ),
            Weap(
                {
                    "id": _Weapons.FANGS,
                    "toss": 10,
                    "deg": 3,
                    "tempo": 100,
                    "rip": 0,
                    "zone": 0,
                    "rap": 0,
                    "dod": 0,
                    "per": 0,
                    "par": 0,
                    "dis": 0,
                    "combo": 10,
                    "type": _WeaponType.Brawl,
                    "anim": _StrikeType.Fist,
                    "dt": 0,
                }
            ),
            Weap(
                {
                    "id": _Weapons.WOOD_CLUB,
                    "toss": 5,
                    "deg": 30,
                    "tempo": 200,
                    "rip": -30,
                    "zone": 1,
                    "rap": -35,
                    "dod": -30,
                    "per": 30,
                    "par": -30,
                    "dis": 10,
                    "combo": -60,
                    "type": _WeaponType.Brawl,
                    "anim": _StrikeType.Slash,
                    "dt": 4,
                }
            ),
            Weap(
                {
                    "id": _Weapons.IRON_CLUB,
                    "toss": 5,
                    "deg": 20,
                    "tempo": 150,
                    "rip": 0,
                    "zone": 1,
                    "rap": -5,
                    "dod": -10,
                    "per": 30,
                    "par": 0,
                    "dis": 10,
                    "combo": 0,
                    "type": _WeaponType.Brawl,
                    "anim": _StrikeType.Slash,
                    "dt": 4,
                }
            ),
            Weap(
                {
                    "id": _Weapons.BONE_CLUB,
                    "toss": 5,
                    "deg": 14,
                    "tempo": 160,
                    "rip": 0,
                    "zone": 1,
                    "rap": 0,
                    "dod": 0,
                    "per": 50,
                    "par": 0,
                    "dis": 10,
                    "combo": -10,
                    "type": _WeaponType.Brawl,
                    "anim": _StrikeType.Slash,
                    "dt": 4,
                }
            ),
            Weap(
                {
                    "id": _Weapons.FLAIL,
                    "toss": 5,
                    "deg": 36,
                    "tempo": 220,
                    "rip": 0,
                    "zone": 1,
                    "rap": -10,
                    "dod": -30,
                    "per": 150,
                    "par": -50,
                    "dis": -20,
                    "combo": 30,
                    "type": _WeaponType.Brawl,
                    "anim": _StrikeType.Slash,
                    "dt": 4,
                }
            ),
            Weap(
                {
                    "id": _Weapons.WHIP,
                    "toss": 5,
                    "deg": 10,
                    "tempo": 150,
                    "rip": -10,
                    "zone": 5,
                    "rap": 30,
                    "dod": 30,
                    "per": -20,
                    "par": -20,
                    "dis": 30,
                    "combo": 35,
                    "type": _WeaponType.Brawl,
                    "anim": _StrikeType.Whip,
                    "dt": 7,
                }
            ),
            Weap(
                {
                    "id": _Weapons.SAI,
                    "toss": 5,
                    "deg": 8,
                    "tempo": 60,
                    "rip": 0,
                    "zone": 0,
                    "rap": 25,
                    "dod": 10,
                    "per": 0,
                    "par": 30,
                    "dis": 100,
                    "combo": 30,
                    "type": _WeaponType.Brawl,
                    "anim": _StrikeType.Estoc,
                    "dt": 2,
                }
            ),
            Weap(
                {
                    "id": _Weapons.POIREAU,
                    "toss": 2,
                    "deg": 5,
                    "tempo": 110,
                    "rip": 100,
                    "zone": 1,
                    "rap": 100,
                    "dod": 0,
                    "per": 200,
                    "par": -50,
                    "dis": 0,
                    "combo": 200,
                    "type": _WeaponType.Brawl,
                    "anim": _StrikeType.Slash,
                    "dt": 4,
                }
            ),
            Weap(
                {
                    "id": _Weapons.MUG,
                    "toss": 2,
                    "deg": 8,
                    "tempo": 90,
                    "rip": 0,
                    "zone": 0,
                    "rap": 30,
                    "dod": 15,
                    "per": 0,
                    "par": -10,
                    "dis": 0,
                    "combo": 40,
                    "type": _WeaponType.Brawl,
                    "anim": _StrikeType.Estoc,
                    "dt": 0,
                }
            ),
            Weap(
                {
                    "id": _Weapons.POELE,
                    "toss": 2,
                    "deg": 17,
                    "tempo": 120,
                    "rip": 0,
                    "zone": 1,
                    "rap": 0,
                    "dod": 0,
                    "per": 0,
                    "par": 40,
                    "dis": 0,
                    "combo": -40,
                    "type": _WeaponType.Brawl,
                    "anim": _StrikeType.Slash,
                    "dt": 4,
                }
            ),
            Weap(
                {
                    "id": _Weapons.POUSSIN,
                    "toss": 2,
                    "deg": 5,
                    "tempo": 32,
                    "rip": 0,
                    "zone": 0,
                    "rap": 0,
                    "dod": 0,
                    "per": 0,
                    "par": -10,
                    "dis": 0,
                    "combo": 0,
                    "type": _WeaponType.Throw,
                    "anim": _StrikeType.Fist,
                    "dt": 6,
                }
            ),
            Weap(
                {
                    "id": _Weapons.HALBERD,
                    "toss": 2,
                    "deg": 24,
                    "tempo": 180,
                    "rip": 0,
                    "zone": 4,
                    "rap": -40,
                    "dod": 0,
                    "per": 0,
                    "par": 0,
                    "dis": 10,
                    "combo": 0,
                    "type": _WeaponType.Brawl,
                    "anim": _StrikeType.Slash,
                    "dt": 1,
                }
            ),
            Weap(
                {
                    "id": _Weapons.TROMBONNE,
                    "toss": 2,
                    "deg": 20,
                    "tempo": 250,
                    "rip": 0,
                    "zone": 2,
                    "rap": -10,
                    "dod": 0,
                    "per": 20,
                    "par": 20,
                    "dis": 50,
                    "combo": 30,
                    "type": _WeaponType.Brawl,
                    "anim": _StrikeType.Slash,
                    "dt": 4,
                }
            ),
            Weap(
                {
                    "id": _Weapons.KEYBOARD,
                    "toss": 2,
                    "deg": 7,
                    "tempo": 100,
                    "rip": 0,
                    "zone": 1,
                    "rap": 20,
                    "dod": 10,
                    "per": 0,
                    "par": 0,
                    "dis": 0,
                    "combo": 50,
                    "type": _WeaponType.Brawl,
                    "anim": _StrikeType.Slash,
                    "dt": 4,
                }
            ),
            Weap(
                {
                    "id": _Weapons.NOODLES,
                    "toss": 2,
                    "deg": 10,
                    "tempo": 45,
                    "rip": 0,
                    "zone": 0,
                    "rap": 0,
                    "dod": 10,
                    "per": 0,
                    "par": -10,
                    "dis": 0,
                    "combo": 30,
                    "type": _WeaponType.Throw,
                    "anim": _StrikeType.Fist,
                    "dt": 6,
                }
            ),
            Weap(
                {
                    "id": _Weapons.RACKET,
                    "toss": 2,
                    "deg": 6,
                    "tempo": 80,
                    "rip": 100,
                    "zone": 1,
                    "rap": 0,
                    "dod": 10,
                    "per": 0,
                    "par": 20,
                    "dis": 0,
                    "combo": 0,
                    "type": _WeaponType.Brawl,
                    "anim": _StrikeType.Slash,
                    "dt": 4,
                }
            ),
        ]

    @staticmethod
    def followers():
        return [
            {
                "force": 6,
                "agility": 5,
                "speed": 3,
                "lifeMax": -6,
                "counter": 0,
                "riposte": 0,
                "combo": 10,
                "parry": 0,
                "dodge": 0,
                "init": 10,
                "dw": _Weapons.FANGS,
            },  # DOG_0
            {
                "force": 6,
                "agility": 5,
                "speed": 3,
                "lifeMax": -6,
                "counter": 0,
                "riposte": 0,
                "combo": 10,
                "parry": 0,
                "dodge": 0,
                "init": 10,
                "dw": _Weapons.FANGS,
            },  # DOG_1
            {
                "force": 6,
                "agility": 5,
                "speed": 3,
                "lifeMax": -6,
                "counter": 0,
                "riposte": 0,
                "combo": 10,
                "parry": 0,
                "dodge": 0,
                "init": 10,
                "dw": _Weapons.FANGS,
            },  # DOG_2
            {
                "force": 23,
                "agility": 16,
                "speed": 24,
                "lifeMax": -4,
                "counter": 0,
                "riposte": 0,
                "combo": 60,
                "parry": 0,
                "dodge": 20,
                "init": 60,
                "dw": _Weapons.FANGS,
            },  # PANTHER
            {
                "force": 40,
                "agility": 2,
                "speed": 1,
                "lifeMax": 10,
                "counter": 0,
                "riposte": 0,
                "combo": -20,
                "parry": 0,
                "dodge": 0,
                "init": 360,
                "dw": _Weapons.HANDS,
            },
        ]

    @staticmethod
    def supers():
        return [
            Sup({"id": _Supers.THIEF, "toss": 8, "use": 2}),
            Sup({"id": _Supers.BRUTE, "toss": 5, "use": 1}),
            Sup({"id": _Supers.MEDECINE, "toss": 5, "use": 1}),
            Sup({"id": _Supers.NET, "toss": 5, "use": 1}),
            Sup({"id": _Supers.BOMB, "toss": 2, "use": 2}),
            Sup({"id": _Supers.GRAB, "toss": 2, "use": 1}),
            Sup({"id": _Supers.SHOUT, "toss": 8, "use": 2}),
            Sup({"id": _Supers.HYPNO, "toss": 3, "use": 1}),
            Sup({"id": _Supers.DOWNPOUR, "toss": 2, "use": 1}),
            Sup({"id": _Supers.TRAPPER, "toss": 20, "use": 4}),
        ]

    @staticmethod
    def bonus_weights():
        return [
            BonusSlot({"id": Permanent(_Permanent.SUPER_FORCE), "w": 60}),
            BonusSlot({"id": Permanent(_Permanent.SUPER_AGILITY), "w": 60}),
            BonusSlot({"id": Permanent(_Permanent.SUPER_SPEED), "w": 60}),
            BonusSlot({"id": Permanent(_Permanent.SUPER_LIFE), "w": 60}),
            BonusSlot({"id": Permanent(_Permanent.IMMORTALITY), "w": 1}),
            BonusSlot({"id": Permanent(_Permanent.BLADE_MASTER), "w": 10}),
            BonusSlot({"id": Permanent(_Permanent.BRAWL_MASTER), "w": 10}),
            BonusSlot({"id": Permanent(_Permanent.VIGILANCE), "w": 20}),
            BonusSlot({"id": Permanent(_Permanent.PUGNACITY), "w": 4}),
            BonusSlot({"id": Permanent(_Permanent.TWISTER), "w": 10}),
            BonusSlot({"id": Permanent(_Permanent.SHIELD), "w": 20}),
            BonusSlot({"id": Permanent(_Permanent.ARMOR), "w": 4}),
            BonusSlot({"id": Permanent(_Permanent.LEATHER_SKIN), "w": 30}),
            BonusSlot({"id": Permanent(_Permanent.UNTOUCHABLE), "w": 1}),
            BonusSlot({"id": Permanent(_Permanent.VANDALISM), "w": 3}),
            BonusSlot({"id": Permanent(_Permanent.CHOC), "w": 10}),
            BonusSlot({"id": Permanent(_Permanent.BLUNT_MASTER), "w": 5}),
            BonusSlot({"id": Permanent(_Permanent.MERCILESS), "w": 1}),
            BonusSlot({"id": Permanent(_Permanent.SURVIVAL), "w": 4}),
            BonusSlot({"id": Permanent(_Permanent.LEAD_BONES), "w": 4}),
            BonusSlot({"id": Permanent(_Permanent.BALLERINA), "w": 4}),
            BonusSlot({"id": Permanent(_Permanent.STAYER), "w": 4}),
            BonusSlot(
                {
                    "id": Permanent(_Permanent.WARM_BLOODED),
                    "w": 8,
                }
            ),
            BonusSlot(
                {
                    "id": Permanent(_Permanent.INCREVABLE),
                    "w": 3,
                }
            ),
            BonusSlot(
                {
                    "id": Permanent(_Permanent.DIESEL),
                    "w": 1,
                }
            ),
            BonusSlot(
                {
                    "id": Permanent(_Permanent.COUNTER),
                    "w": 10,
                }
            ),
            BonusSlot(
                {
                    "id": Permanent(_Permanent.IRON_HEAD),
                    "w": 4,
                }
            ),
            BonusSlot({"id": Super(_Supers.THIEF), "w": 10}),
            BonusSlot({"id": Super(_Supers.BRUTE), "w": 20}),
            BonusSlot({"id": Super(_Supers.MEDECINE), "w": 8}),
            BonusSlot({"id": Super(_Supers.NET), "w": 16}),
            BonusSlot({"id": Super(_Supers.BOMB), "w": 6}),
            BonusSlot({"id": Super(_Supers.GRAB), "w": 1}),
            BonusSlot({"id": Super(_Supers.SHOUT), "w": 4}),
            BonusSlot({"id": Super(_Supers.HYPNO), "w": 2}),
            BonusSlot({"id": Super(_Supers.DOWNPOUR), "w": 2}),
            BonusSlot(
                {
                    "id": Super(_Supers.TRAPPER),
                    "w": 4,
                }
            ),
            BonusSlot({"id": Followers(_Followers.DOG_0), "w": 20}),
            BonusSlot({"id": Followers(_Followers.DOG_1), "w": 8}),
            BonusSlot({"id": Followers(_Followers.DOG_2), "w": 2}),
            BonusSlot({"id": Followers(_Followers.BEAR), "w": 1}),
            BonusSlot({"id": Followers(_Followers.PANTHER), "w": 1}),
            BonusSlot({"id": Weapons(_Weapons.KNIFE), "w": 80}),
            BonusSlot({"id": Weapons(_Weapons.SWORD), "w": 100}),
            BonusSlot({"id": Weapons(_Weapons.LANCE), "w": 40}),
            BonusSlot({"id": Weapons(_Weapons.STICK), "w": 70}),
            BonusSlot({"id": Weapons(_Weapons.TRIDENT), "w": 10}),
            BonusSlot({"id": Weapons(_Weapons.AXE), "w": 40}),
            BonusSlot({"id": Weapons(_Weapons.SCIMETAR), "w": 6}),
            BonusSlot({"id": Weapons(_Weapons.HAMMER), "w": 3}),
            BonusSlot({"id": Weapons(_Weapons.BIG_SWORD), "w": 4}),
            BonusSlot({"id": Weapons(_Weapons.FAN), "w": 2}),
            BonusSlot({"id": Weapons(_Weapons.SHURIKEN), "w": 8}),
            BonusSlot({"id": Weapons(_Weapons.WOOD_CLUB), "w": 50}),
            BonusSlot({"id": Weapons(_Weapons.IRON_CLUB), "w": 6}),
            BonusSlot({"id": Weapons(_Weapons.BONE_CLUB), "w": 20}),
            BonusSlot({"id": Weapons(_Weapons.FLAIL), "w": 4}),
            BonusSlot({"id": Weapons(_Weapons.WHIP), "w": 3}),
            BonusSlot({"id": Weapons(_Weapons.SAI), "w": 6}),
            BonusSlot({"id": Weapons(_Weapons.POIREAU), "w": 2}),
            BonusSlot({"id": Weapons(_Weapons.MUG), "w": 2}),
            BonusSlot({"id": Weapons(_Weapons.POELE), "w": 2}),
            BonusSlot({"id": Weapons(_Weapons.POUSSIN), "w": 2}),
            BonusSlot({"id": Weapons(_Weapons.HALBERD), "w": 2}),
            BonusSlot({"id": Weapons(_Weapons.TROMBONNE), "w": 2}),
            BonusSlot({"id": Weapons(_Weapons.KEYBOARD), "w": 2}),
            BonusSlot({"id": Weapons(_Weapons.NOODLES), "w": 2}),
            BonusSlot({"id": Weapons(_Weapons.RACKET), "w": 2}),
        ]

    @staticmethod
    def rare_weapons():
        return [
            _Weapons.POIREAU,
            _Weapons.MUG,
            _Weapons.POELE,
            _Weapons.POUSSIN,
            _Weapons.TROMBONNE,
            _Weapons.KEYBOARD,
            _Weapons.NOODLES,
            _Weapons.RACKET,
        ]

    @staticmethod
    def possible_incapacity_weapons():
        return [
            _Weapons.KNIFE,
            _Weapons.SWORD,
            _Weapons.LANCE,
            _Weapons.STICK,
            _Weapons.TRIDENT,
            _Weapons.AXE,
            _Weapons.SCIMETAR,
            _Weapons.HAMMER,
            _Weapons.BIG_SWORD,
            _Weapons.FAN,
            _Weapons.SHURIKEN,
            _Weapons.WOOD_CLUB,
            _Weapons.IRON_CLUB,
            _Weapons.BONE_CLUB,
            _Weapons.FLAIL,
            _Weapons.WHIP,
        ]
