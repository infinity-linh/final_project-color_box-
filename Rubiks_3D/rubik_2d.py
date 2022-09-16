import copy
SIDES = 6
import time

class State:
    def __init__(self, size=3, c=None):
        self.size = size
        self.actions = ['front', 'back', 'left', 'right', 'top', 'bottom']
        if c:
            self.d = c
            self.__front__ = c["front"]
            self.__back__ = c["back"]
            self.__left__ = c["left"]
            self.__right__ = c["right"]
            self.__top__ = c["top"]
            self.__bottom__ = c["bottom"]
            self.__sides__ = [self.front(), self.back(), self.left(), self.right(), self.top(), self.bottom()]
            return
        self.__front__ = [['W','W','W'],['W','W','W'],['W','W','W']]
        self.__back__ = [['Y','Y','Y'],['Y','Y','Y'],['Y','Y','Y']]
        self.__top__ = [['R','R','R'],['R','R','R'],['R','R','R']]
        self.__bottom__ = [['O','O','O'],['O','O','O'],['O','O','O']]
        self.__left__ = [['B','B','B'],['B','B','B'],['B','B','B']]
        self.__right__ = [['G','G','G'],['G','G','G'],['G','G','G']]
        self.__sides__ = [self.front(), self.back(), self.left(), self.right(), self.top(), self.bottom()]
        self.d = {"front": self.front(), "back": self.back(), "left": self.left(),\
            "right": self.right(), "top": self.top(), "bottom": self.bottom()}