WIN_WIDTH = 640
WIN_HEIGHT = 480

CAMERA_SIZE = 16
TILE_SIZE = 32


PLAYER_LAYER = 3
BLOCK_LAYER = 2
GROUND_LAYER = 1
ENERMY_LAYER = 4
BULLET_LAYER = 5
GUN_LAYER = 6
MAP_LAYER = 0
UI_LAYER = 10

PLAYER_SPEED = 5
ENEMY_SPEED = 2
ENEMY_SCOPE = 160
BULLET_SPEED = 10

#chinh lai khoang thoi gian giua cac lan ban
GLOCK_DELAY = 240
GLOCK_SCOPE = 280
WEAPON_SIZE = 42
AK47_DELAY = 100
AK47_SCOPE = 400

RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
GREY = (128, 128, 128)
BROWN = (255,160, 85)
DARK_BROWN = (101,67,33)

FPS = 60

hpipemap = [
    '',
    '',
    '',
    '',
    'BBBBBBBBBBBBBBBBBBBB',
    '....................',
    '....................',
    '....................',
    '....................',
    '....................',
    'BBBBBBBBBBBBBBBBBBBB',
    '',
    '',
    '',
    ''
]

vpipemap = [
    '      B......B',
    '      B......B',
    '      B......B',
    '      B......B',
    '      B......B',
    '      B......B',
    '      B......B',
    '      B......B',
    '      B......B',
    '      B......B',
    '      B......B',
    '      B......B',
    '      B......B',
    '      B......B',
    '      B......B'
]

tilemaps = [
    [
        'BBBBBBBBBBBBBBBBBBBB',
        'B..................B',
        'B..................B',
        'B..................B',
        'B..................B',
        'B..................B',
        'B..................B',
        'B.........P........B',
        'B..................B',
        'B..................B',
        'B..................B',
        'B..................B',
        'B..................B',
        'B..................B',
        'BBBBBBBBBBBBBBBBBBBB'
    ], 
    [
        'BBBBBBBBBBBBBBBBBBBB',
        'B..................B',
        'B.....B......B.....B',
        'B.....B......BE....B',
        'B...BBB......BBB...B',
        'B..................B',
        'B..................B',
        'B........EE........B',
        'B..................B',
        'B..................B',
        'B...BBB......BBB...B',
        'B.....B......B.....B',
        'B.....B......B.....B',
        'B.............E.E..B',
        'BBBBBBBBBBBBBBBBBBBB'
    ],
    [
        'BBBBBBBBBBBBBBBBBBBB',
        'B..................B',
        'B..................B',
        'B....BBB......E....B',
        'B..................B',
        'B..................B',
        'B..................B',
        'B..................B',
        'B.....BBB..........B',
        'B.......B..........B',
        'B.......B..........B',
        'B..........E.E.....B',
        'B..................B',
        'B..................B',
        'BBBBBBBBBBBBBBBBBBBB'
    ],
    [
        'BBBBBBBBBBBBBBBBBBBB',
        'B..................B',
        'B..................B',
        'B....BBB......E....B',
        'B..................B',
        'B..................B',
        'B..................B',
        'B..................B',
        'B.....BBB..........B',
        'B.......B..........B',
        'B.......B..........B',
        'B..........E.E.....B',
        'B..................B',
        'B..................B',
        'BBBBBBBBBBBBBBBBBBBB'
    ]
]