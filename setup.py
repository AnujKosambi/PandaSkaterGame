from distutils.core import setup
import py2exe
import direct.directbase.DirectStart
from panda3d.core import CollisionTraverser,CollisionNode
from panda3d.core import CollisionHandlerQueue,CollisionRay
from panda3d.core import Filename,AmbientLight,DirectionalLight
from panda3d.core import PandaNode,NodePath,Camera,TextNode
from direct.interval.LerpInterval import LerpPosInterval
from panda3d.core import Vec3,Vec4,BitMask32
from panda3d.core import *
from direct.gui.OnscreenText import OnscreenText
from direct.actor.Actor import Actor
from direct.showbase.DirectObject import DirectObject
from direct.interval.IntervalGlobal import Sequence
import random, sys, os, math 
from pandac.PandaModules import Plane
from pandac.PandaModules import PlaneNode
from math import pi, sin, cos ,sqrt,atan
import Image
import time

setup(console=['play.py'])