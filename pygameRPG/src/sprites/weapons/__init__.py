"""Weapons package - Contains all weapon and projectile classes"""

from sprites.weapons.bullet import Bullet
from sprites.weapons.gun import Gun
from sprites.weapons.glock import Glock
from sprites.weapons.ak47 import AK47
from sprites.weapons.sniper import Sniper
from sprites.weapons.attack import Attack

__all__ = ['Bullet', 'Gun', 'Glock', 'AK47', 'Sniper', 'Attack']
