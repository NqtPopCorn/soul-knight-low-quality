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

PLAYER_SPEED = 5
ENEMY_SPEED = 2
ENEMY_SCOPE = 160
BULLET_SPEED = 10

#chinh lai khoang thoi gian giua cac lan ban
GLOCK_DELAY = 240
GLOCK_SCOPE = 280
WEAPON_SIZE = 42

RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

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

# maps = [
#     {
#         "num_enemies": 3,
#         "mappingpos": [0, 0],
#         "tilemap": [
#             'BBBBBBBBBBBBBBBBBBBB',
#             'B..................B',
#             'B..................B',
#             'B....BBB......E....B',
#             'B..................B',
#             'B..................B',
#             'B..........P.......B',
#             'B..................B',
#             'B.....BBB..........B',
#             'B.......B..........B',
#             'B.......B..........B',
#             'B..........E.E.....B',
#             'B..................B',
#             'B..................B',
#             'BBBBBBBBBBBBBBBBBBBB'
#         ]
#     }, 
#     {
#         "mappingpos": [1,0],
#         "tilemap": hpipemap
#     },
#     {
#         "mappingpos": [2, 0],
#         "tilemap": [
#             'BBBBBBBBBBBBBBBBBBBB',
#             'B..................B',
#             'B..................B',
#             'B....BBB......E....B',
#             'B..................B',
#             'B..................B',
#             'B..................B',
#             'B..................B',
#             'B.....BBB..........B',
#             'B.......B..........B',
#             'B.......B..........B',
#             'B..........E.E.....B',
#             'B..................B',
#             'B..................B',
#             'BBBBBBBBBBBBBBBBBBBB'
#         ]
#     },
#         {
#             "mappingpos": [2,1],
#             "tilemap": vpipemap
#         },
#     {
#         "mappingpos": [2, 2],
#         "tilemap": [
#             'BBBBBBBBBBBBBBBBBBBB',
#             'B..................B',
#             'B..................B',
#             'B....BBB......E....B',
#             'B..................B',
#             'B..................B',
#             'B..................B',
#             'B..................B',
#             'B.....BBB..........B',
#             'B.......B..........B',
#             'B.......B..........B',
#             'B..........E.E.....B',
#             'B..................B',
#             'B..................B',
#             'BBBBBBBBBBBBBBBBBBBB'
#         ]
#     },
#         {
#             "mappingpos": [2, -1],
#             "tilemap": vpipemap
#         },
#     {
#         "mappingpos": [2, -2],
#         "tilemap": [
#             'BBBBBBBBBBBBBBBBBBBB',
#             'B..................B',
#             'B..................B',
#             'B....BBB......E....B',
#             'B..................B',
#             'B..................B',
#             'B..................B',
#             'B..................B',
#             'B.....BBB..........B',
#             'B.......B..........B',
#             'B.......B..........B',
#             'B..........E.E.....B',
#             'B..................B',
#             'B..................B',
#             'BBBBBBBBBBBBBBBBBBBB'
#         ]
#     }
# ]

tilemaps = [
    [
        'BBBBBBBBBBBBBBBBBBBB',
        'B..................B',
        'B..................B',
        'B....BBB......E....B',
        'B..................B',
        'B..................B',
        'B..........P.......B',
        'B..................B',
        'B.....BBB..........B',
        'B.......B..........B',
        'B.......B..........B',
        'B..........E.E.....B',
        'B..................B',
        'B..................B',
        'BBBBBBBBBBBBBBBBBBBB'
    ], 
        # hpipemap,
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
        # vpipemap,
    
        # vpipemap,
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

# others = [
#     (0,0),
#     (1,0),
#     (2,0),
#     (2,1),
#     (2,2),
#     (2, -1),
#     (2, -2)
# ]