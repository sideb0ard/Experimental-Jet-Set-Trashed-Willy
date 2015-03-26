from gameObject import gameObject
from defines import GameDefines


class Ball(gameObject):
    _shape = "o"
    _y = 2
    _x = GameDefines._ballStartPos

    def __init__(self, gameobject):
        super(Ball, self).__init__(gameobject)
