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
class Game(DirectObject):

	def __init__(self):
		self.count_tree=0
		self.playVideo("intro.mp4")
		base.disableMouse()
		self.environ = loader.loadModel("models/scene.egg.pz")
		self.objects=loader.loadModel("models/objects.egg")
		self.plants=loader.loadModel("models/plants.egg")
		self.plants.reparentTo(render)
		self.objects.reparentTo(render)
		self.environ.reparentTo(render)
		self.makeSkyBox()
		
		
		self.makingActor()
		self.makeRacers()
		self.controlSkater()

		self.makeLights()
		self.makeWater()
		#self.controlRacer()
		self.addCollisions()
		self.addDuck()
		#self.makeRacingai()
		self.tree_array={}
		self.stone_array={}
		self.count_stone=0
		self.isSitted=False
		self.bench={}
		self.count_bench=0;
		self.AddBench(-40,-30)
		self.AddBench(-40,-40,180)
		self.AddBench(40,-30)
		self.AddBench(40,-40,180)
		self.AddBench(40,30)
		self.AddBench(40,40,180)
		self.AddBench(-40,30)
		self.AddBench(-40,40,180)



		for i in range(-70,70,6):
				#for j in range (-80,-70,3):
					self.AddTree(i,-65)
		for i in range(-70,70,6):
				#for j in range (-80,-70,3):
					self.AddTree(i+5,-70)			
		for i in range(-70,70,6):
				#for j in range (60,70,3):
					self.AddTree(i,65)
		for i in range(-70,70,6):
				#for j in range (60,70,3):
					self.AddTree(i+5,70)
		for j in range(-70,70,6):
				#for i in range (60,70,3):
					self.AddTree(65,j)
		for j in range(-70,70,6):
				#for i in range (60,70,3):
					self.AddTree(70,j+5)
		for j in range(-70,70,6):
				#for i in range (-80,-70,3):
					self.AddTree(-70,j)
		for j in range(-70,70,6):
				#for i in range (-80,-70,3):
					self.AddTree(-65,j+5)
		self.initailState()

		render.setShaderAuto()
	def playVideo(self,src):
		tex = MovieTexture("name")
		assert tex.read(src), "Failed to load video!"
		cm = CardMaker("My Fullscreen Card");
		cm.setFrameFullscreenQuad()
		cm.setUvRange(tex)
		card = NodePath(cm.generate())
		card.reparentTo(render2d)
		card.setTexture(tex)
		card.setTexScale(TextureStage.getDefault(), tex.getTexScale())
		sound=loader.loadSfx(src)
		tex.synchronizeTo(sound)
		tex.setLoop(False)
		sound.play()
		def  myTask(task):
			i=14
			if(src=='talk.mp4'):
				i=7

			if (int(tex.getTime()) >=i):
				#print "Stoping"
				card.remove()
				return task.done
			# if myMovieTexture.getTime() == myMovieLength:
			# 	print "movie puri"
			return task.cont
		taskMgr.add(myTask, "Task")
	
	def addDuck(self):
		
		self.duck={}
		
		self.count_duck=0

		self.interval1={};self.interval11={}
		self.interval2={};self.interval22={}
		for i in range(0,3,1):
			self.duck[self.count_duck]=loader.loadModel("models/duck.egg")
			self.duck[self.count_duck].setScale(random.uniform(5,7))
			self.duck[self.count_duck].setZ(0.65)
			self.duck[self.count_duck].setX(i*3-3)
			self.duck[self.count_duck].reparentTo(render)
			self.interval1[self.count_duck]= self.duck[self.count_duck].posInterval(10,Point3(i*3-3, random.uniform(0,12),0.65),startPos=Point3(i*3-3,-1*random.uniform(0,12),0.65))
			self.interval11[self.count_duck]=self.duck[self.count_duck].hprInterval(0.1, Vec3(0, 0, 0))
			self.interval2[self.count_duck]= self.duck[self.count_duck].posInterval(10,Point3(i*3-3,-1*random.uniform(0,12),0.65),startPos=Point3(i*3-3,random.uniform(0,12),0.65))
			self.interval22[self.count_duck]=self.duck[self.count_duck].hprInterval(0.1, Vec3(180, 0, 0))
			if(self.count_duck==0):
				self.mySequence=Sequence(self.interval1[self.count_duck], name="duck")
			self.mySequence.append(self.interval11[self.count_duck])
			self.mySequence.append(self.interval2[self.count_duck])
			self.mySequence.append(self.interval22[self.count_duck])

			self.count_duck=self.count_duck+1
		self.mySequence.loop()

		
	def makeSkyBox(self):
		#colour = (0.5,0.8,0.5)
		
		self.skybox=loader.loadModel("models/skybox.egg")
		self.skybox.reparentTo(render)
		self.skybox.setLightOff(1)
		self.skybox.setZ(-10)
		self.skybox.setScale(140,140,70)
	def makingActor(self):
		self.skater = Actor("models/scater.egg",{"fall":"models/scaterfall.egg","skate":"models/scater.egg",
			"walk":"models/scaterwalk.egg","run":"models/scaterrun.egg","sit":"models/scatersit.egg"})

		self.skater.setPos(-20.67,-41.99,0)
		self.skater.setScale(0.075,0.075,0.075)
		#self.skater.setH(180)
		self.skater.reparentTo(render)
	def makeWater(self):
		
		self.water = loader.loadModel("models/water.egg")
		self.water.setPos(0,0,1)
		self.water.setShader(loader.loadShader('shaders/water.sha'))
		self.water.setShaderInput('wateranim', Vec4(0.03, -0.015, 64.0, 0))
		self.water.setShaderInput('waterdistort', Vec4(0.4, 4.0, 0.25, 0.45))
		self.water.setShaderInput('time', 0)
		buffer = base.win.makeTextureBuffer('waterBuffer', 512, 512)
		#buffer.setClearColor(Vec4(0.3, 0.3, 1, 1))
		cfa = CullFaceAttrib.makeReverse()
		rs = RenderState.make(cfa)
		self.watercamNP = base.makeCamera(buffer)
		self.watercamNP.reparentTo(render)
		cam = self.watercamNP.node()
		cam.getLens().setFov(base.camLens.getFov())
		cam.getLens().setNear(1)
		cam.getLens().setFar(5000)
		cam.setInitialState(rs)
		self.waterPlane = Plane(Vec3(0, 0,  1), Point3(0, 0, 0))
		planeNode = PlaneNode('waterPlane')
		planeNode.setPlane(self.waterPlane)
		#cam.lookAt(0,0,-1)
		cam.setTagStateKey('Clipped')
		tex0 = buffer.getTexture()
		tex0.setWrapU(Texture.WMClamp)
		tex0.setWrapV(Texture.WMClamp)
		ts0 = TextureStage('reflection')

		self.water.setTexture(ts0, tex0)
		tex1 = loader.loadTexture('texture/water.png')
		ts1 = TextureStage('distortion')
		self.water.setTexture(ts1, tex1)
		self.keyMap={};
		self.keyMap["sit"]=0
		self.keyMap["call"]=0
		self.keyMap["left"]=0
		self.keyMap["forward"]=0
		self.keyMap["right"]=0
		taskMgr.add(self.waterUpdate, "waterTask")
		
		taskMgr.add(self.cameraControl,"cameraControl")



		self.water.reparentTo(render)
	def controlSkater(self):

		self.isMoving = False
		self.floater = NodePath(PandaNode("floater"))
		self.floater.reparentTo(render)

		self.accept("arrow_up", self.setKey,  ["forward",1])
		self.accept("arrow_up-repeat",self.setKey,  ["forward",1])
		self.accept("arrow_up-up",self.setKey, ["forward",0])
		self.accept("arrow_down", self.setKey,  ["forward",-1])
		self.accept("arrow_down-repeat",self.setKey,  ["forward",-1])
		self.accept("arrow_down-up",self.setKey, ["forward",0])
		self.accept("e",self.setKey,["sit",1])
		self.accept("q",self.setKey,["sit",0])
		self.accept("c",self.setKey,["call",1])
		#self.accept("c-up",self.setKey,["call",0])
		
		
		self.accept("arrow_left", self.setKey, ["left",1])
		self.accept("arrow_left-repeat",self.setKey, ["left",1])
		self.accept("arrow_left-up",self.setKey,["left",0])
		self.accept("arrow_right", self.setKey, ["right",1])
		self.accept("arrow_right-repeat",self.setKey, ["right",1])
		self.accept("arrow_right-up",self.setKey,["right",0])
		self.accept("escape", sys.exit)
	def makeRacers(self):
		#self.floater=0
		self.racers={}
		self.racersCount=0
		self.racers[self.racersCount] = Actor("models/scater.egg",{"skate":"models/scater.egg",
			"walk":"models/scaterwalk.egg","sit":"models/scatersit.egg","standup":"models/scaterstandup.egg"})
		self.racers[self.racersCount].setTexture(loader.loadTexture("texture/racer.tga"),1)
		self.racers[self.racersCount].setPos(-30,30,0)
		self.racers[self.racersCount].setScale(0.075,0.075,0.075)
		#self.racers[self.racersCount].setH(90)
		self.racers[self.racersCount].reparentTo(render)
		#self.racerMoveTo(self.racersCount,-60,0)
		#self.interval={}
		#self.controlRacer(self.racersCount)
		

		
		#self.racersCount=self.racersCount+1
	def racerMoveTo(self,no,x,y,direcation,anim='skate'):
		if(x-self.racers[no].getX()!=0):
			self.angle=atan(float(y-self.racers[no].getY())/float(x-self.racers[no].getX()))+90
			if(x<self.racers[no].getX()):
				self.angle=self.angle+90

		else:
			if(y>self.racers[no].getY()):
				self.angle=180
			if(y<self.racers[no].getY()):
				self.angle=0
		self.racers[no].setH(self.angle*180/pi)
		self.interval= self.racers[no].posInterval(direcation,Point3(x,y,0),startPos=self.racers[no].getPos())
		#self.pace = Sequence(interval,name="skatePose")
		self.interval.start()
		#s		while (interval.isPlaying())
		self.racers[no].loop(anim)

		#while (self.racers[no].getY()!=y and self.racers[no].getX()!=x):
		#	self.racers[no].setY(self.racers[no], -100 * globalClock.getDt())
	def controlRacer(self,no):
		self.pointNo=1;
		
		taskMgr.add(self.controlRacerTask, "race")
		self.racers[self.racersCount].setPos(-12.3668,42.92,0)
		self.racerMoveTo(no,-12.3668,42.92,3)
		#y={42.92,10.61,-4.685,-29.29,-41.99,-45,-40.87,-33.22,-17.81,-1.14,21.30,36.82,45.5}
		#for i in range(0,13,1):
			#self.racerMoveTo(self.racersCount,x[i],y[0],7)
			#time.sleep(7)
	def controlRacerTask(self,task):
		if(self.interval.isPlaying()==False and self.exploringMode==False):			
			self.racerMoveTo(self.racersCount,self.x[self.pointNo],self.y[self.pointNo],2)
			self.pointNo=(self.pointNo+1)%13

			#print self.pointNo
		#time.sleep(7)
			
		return task.cont
	def addCollisions(self):
		self.cTrav = CollisionTraverser()

		self.skaterGroundRay = CollisionRay()
		self.skaterGroundRay.setOrigin(0,0,1000)
		self.skaterGroundRay.setDirection(0,0,-1)
		self.skaterGroundCol = CollisionNode('skater')
		self.skaterGroundCol.addSolid(self.skaterGroundRay)
		self.skaterGroundCol.addSolid(CollisionTube(0,0,0,0,0,50,10))
		#self.skaterGroundCol.setFromCollideMask(BitMask32.bit(0))
		#self.skaterGroundCol.setIntoCollideMask(BitMask32.allOff())
		self.skaterGroundColNp = self.skater.attachNewNode(self.skaterGroundCol)
		self.skaterGroundHandler = CollisionHandlerQueue()
		self.cTrav.addCollider(self.skaterGroundColNp, self.skaterGroundHandler)
		#self.skaterGroundColNp.show()
		#self.cTrav.showCollisions(render)
		self.angle=180/pi;
		self.isFall=False
	def setKey(self,key,value):
		self.keyMap[key] = value
	def Move(self,task):
		

		if(self.isSitted ):
			if(self.keyMap['sit']==0):
				self.isSitted=False
				self.skater.pose("walk",12)

				self.isMoving = False
			return task.cont

		startpos = self.skater.getPos()
		if (self.keyMap["left"]!=0):
			self.skater.setH(self.skater.getH() + 100 * globalClock.getDt())
			
		if (self.keyMap["right"]!=0):
			self.skater.setH(self.skater.getH() - 100 * globalClock.getDt())
			
		#if (self.keyMap["right"]!=0):
		#    self.ralph.setH(self.ralph.getH() - 300 * globalClock.getDt())
		dx=100
		if(self.raceingStart==True):
			dx=150
		if (self.keyMap["forward"]!=0):
			if(self.exploringMode==False and self.raceingStart==True and self.startingTime>=3):
				self.skater.setY(self.skater, -dx * globalClock.getDt())
			else:
				if(self.exploringMode==True):
					self.skater.setY(self.skater, -dx * globalClock.getDt())

		
		
		if (self.keyMap["forward"]!=0) :
				
				if self.isMoving == False:
					if self.exploringMode==True:
						self.skater.loop("walk")
					else:
						self.skater.loop("skate")
					self.isMoving = True
		else:
			#if self.isSitted:
				#	@self.skater.loop("sit")
				if self.isMoving :
					#if(self.skater.getCurrentAnim()=='skate'):
						self.skater.stop()
						self.skater.pose("walk",12)
						self.isMoving = False
				
					
		"""
		if(self.isFall==True):
			if(self.skater.getCurrentAnim()=='fall'):
				if(self.skater.getCurrentFrame('fall')>=20):
					self.isFall=False
					self.skater.pose("skate",5)"""
					




		for i in range(0,self.count_bench,1):
				x=self.bench[i].getX()
				y=self.bench[i].getY()
				X=self.skater.getX();Y=self.skater.getY();

				dist=sqrt((x-X)*(x-X)+(y-Y)*(y-Y))
				if(dist<=5):
					if(self.isSitted==False and self.keyMap['sit']==1):
						self.skater.stop()
						self.skater.setPos(self.bench[i].getPos())
						#self.skater.setY(self.skater.getY()+3)
						self.skater.setH(self.bench[i].getH()+270)
						self.skater.play('sit')
						self.isSitted=True
		if(self.isMoving==True):	
			"""if(self.isFall==True):
				if(self.skater.getCurrentFrame('fall')==25):
					self.isFall=False"""


			self.cTrav.traverse(render)

			entries = []
			for i in range(self.skaterGroundHandler.getNumEntries()):
				entry = self.skaterGroundHandler.getEntry(i)
				entries.append(entry)
			entries.sort(lambda x,y: cmp(y.getSurfacePoint(render).getZ(),
									 x.getSurfacePoint(render).getZ()))
			print entries[0].getIntoNode().getName()
			if (len(entries)>0 and entries[0].getIntoNode().getName() == "character"):

				
					self.skater.setZ(entries[0].getSurfacePoint(render).getZ())
				

			else:
				self.skater.setPos(startpos)
			

					
				
				#self.skater.setPos(startpos)

				#self.skater.play('fall')
				#self.isFall=True

					
				
		
		return task.cont

	def AddBench(self,x,y,angle=0):
		self.bench[self.count_bench]=loader.loadModel("models/bench.egg")
		self.bench[self.count_bench].reparentTo(render)
		self.bench[self.count_bench].setH(angle)
		
		self.bench[self.count_bench].setPos(x,y,0)
		self.bench[self.count_bench].setTexture(loader.loadTexture("texture/wood.jpg"),1)
		self.count_bench=self.count_bench+1
		#self.bench[self.count_bench].setScale(0.03,0.03,0.03)
	def AddTree(self,x,y):
		self.tree_array[self.count_tree]=loader.loadModel("models/smalltree.egg")
		self.tree_array[self.count_tree].reparentTo(render)
		self.tree_array[self.count_tree].setPos(x,y,-2)
		self.tree_array[self.count_tree].setScale( random.uniform(0.01,0.02),random.uniform(0.01, 0.02),random.uniform(0.01, 0.02))
		self.tree_array[self.count_tree].setTexture(loader.loadTexture("models/smalltree.png"),1)
		self.tree_array[self.count_tree].setTransparency(TransparencyAttrib.MDual)
		self.tree_array[self.count_tree].setShaderAuto()
		self.tree_array[self.count_tree].setColor(VBase4(0.5+random.uniform(0,0.5),1,0.5+random.uniform(0,0.5),1))
		self.count_tree=self.count_tree+1
	def AddStone(self,x,y):
		self.stone_array[self.count_stone]=loader.loadModel("models/stone1.egg")
		self.stone_array[self.count_stone].reparentTo(render)
		self.stone_array[self.count_stone].setPos(x,y,0)
		self.stone_array[self.count_stone].setH(random.uniform(0,360))
		self.stone_array[self.count_stone].setTexture(loader.loadTexture("texture/Stone_2_DiffuseMap.jpg"),1)
		self.stone_array[self.count_stone].setScale(random.uniform(0.005,0.015))
		self.stone_array[self.count_stone].setShaderAuto()
		
		self.count_stone=self.count_stone+1
	def cameraControl(self,task):
		self.floater.setPos(self.skater.getPos())
		self.floater.setZ(self.skater.getZ() + 10.0)
		#camera.lookAt(self.floater)
		
		return task.cont
	def waterUpdate(self,task):
		self.slnp.lookAt(self.skater)
		#print self.skater.getX(),self.skater.getY()
		base.camera.setPos(self.skater.getPos())
		base.camera.setZ(self.skater.getZ() + 10.0)
		base.camera.setY(self.skater.getY() - 30*sin((-self.skater.getH()-90)*pi/180))
		base.camera.setX(self.skater.getX() + 30*cos((-self.skater.getH()-90)*pi/180))
		if base.mouseWatcherNode.hasMouse():
			x=base.mouseWatcherNode.getMouseX()
			y=base.mouseWatcherNode.getMouseY()
			base.camera.lookAt(self.skater.getX() ,self.skater.getY(),self.skater.getZ()+((y+1)/2)*10+0.5)  
		
		#base.camera.setH(self.skater.getH())
		#base.camera.lookAt(self.skater)
		mc = base.camera.getMat()
		mf = self.waterPlane.getReflectionMat()
		self.mc = base.camera.getMat()
		mf = self.waterPlane.getReflectionMat()
		self.watercamNP.setMat(mc * mf)
		self.water.setShaderInput('time', task.time)
		return task.cont
	def makeLights(self):
		slight = Spotlight('slight')
		slight.setColor(VBase4(1, 1, 1, 1))
		lens = PerspectiveLens()
		slight.setLens(lens)
		#slight.setFov(90)
		self.slnp = render.attachNewNode(slight)
		self.slnp.setPos(0, 0, 70)
		self.ambientLight=AmbientLight('AmbientLight')
		self.ambientLight.setColor(VBase4(0.3, 0.3, 0.3, 0.3))
		#
		self.ambientNP = render.attachNewNode(self.ambientLight)
		
		render.setLight(self.ambientNP)
		render.setLight(self.slnp)
		#render.setLight(self.ambientNP)
	def racingInteraction(self,task):
		if(self.raceingStart==True):
			self.startingTime=task.time
		x=self.racers[self.racersCount].getX()
		y=self.racers[self.racersCount].getY()
		X=self.skater.getX();Y=self.skater.getY();
		dist=sqrt((x-X)*(x-X)+(y-Y)*(y-Y))
		
		if(self.exploringMode==False):
			if((task.time-self.startedTime)<=3):
				self.txt.setText(str(int(task.time-self.startedTime)))
				#self.keyMap["forward"]=0
				self.isRacing=True
			else:
				self.txt.setText("")
		if(dist<=5):
			if(self.keyMap["call"]==1 and self.raceingStart==False):
				self.racers[self.racersCount].play('standup')
				
				self.raceingStart=True
			else:
				if(self.keyMap["call"]==1 and self.raceingStart==True):
				
					 

					if(self.racers[self.racersCount].getAnimControl('standup').isPlaying()==False and self.exploringMode==True):
						self.startedTime=task.time

						#self.playVideo('talk.mp4')
						
						#mytimer.setY(0)
						self.exploringMode=False
						self.skater.setH(0)
						self.skater.setPos(-15.3668,44,0)
						self.controlRacer(self.racersCount)
		#print self.skater.getX(),self.skater.getY()

		if(
			self.exploringMode==False and self.skater.getX()>=-5 and self.skater.getX()<=5 and self.skater.getY()>=42 and self.skater.getY()<=55):
			
			self.exploringMode=True
			self.raceingStart=False
			self.txt.setText("Finish \n You Win")
			self.finishTime=task.time;
			self.interval.finish()
			self.racers[self.racersCount].setPos(-40,-30,0)
			self.keyMap["call"]=0
			self.skater.setPos(-15.3668,44,0)
			self.racers[self.racersCount].setH(self.bench[0].getH()+270)
			self.racers[self.racersCount].pose('standup',0)
		if(self.exploringMode==False and  self.racers[self.racersCount].getX()>=-5 and self.racers[self.racersCount].getX()<=5 
			and self.racers[self.racersCount].getY()>=42 and self.racers[self.racersCount].getY()<=55):
			
			self.exploringMode=True
			self.raceingStart=False
			

			self.txt.setText("  Finish \n You Lose")
			self.finishTime=task.time;
			self.interval.finish()
			self.racers[self.racersCount].setPos(-40,-30,0)
			self.keyMap["call"]=0
			
			self.racers[self.racersCount].setH(self.bench[0].getH()+270)
			self.racers[self.racersCount].pose('standup',0)
		
		if(task.time-self.finishTime>=1 and self.finishTime!=0):
		
			self.txt.setText("")




		return task.cont
	def initailState(self):
		OnscreenText(text="[1] Press E for sit ", style=1, fg=(1,1,1,1),pos=(-1.75, 0.9), align=TextNode.ALeft, scale = 0.06)
		OnscreenText(text="[2] Press Q for stand", style=1, fg=(1,1,1,1),pos=(-1.75, 0.8), align=TextNode.ALeft, scale = 0.06)
		OnscreenText(text="[3] Press C for Challenge", style=1, fg=(1,1,1,1),pos=(-1.75, 0.7), align=TextNode.ALeft, scale = 0.06)
		self.finishX=0
		self.finishTime=0
		map_data = Image.open("texture/map.png") 
		pix_data = map_data.load()
		for i in range(0,80,3):
			for j in range (0,80,3):
				#print pix_data[i,j]
				if pix_data[i,j]==0:
					self.AddStone(i-40,j-40)
				else:
					if pix_data[i,j]==3:
						self.AddTree(i-40,j-40)




				
		self.txt=OnscreenText(text="", style=1, fg=(1,1,1,1),pos=(0, 0), align=TextNode.ALeft, scale = 0.06)
		self.raceingStart=False
		self.exploringMode=True

		self.racers[self.racersCount].setPos(-40,-30,0)
		self.racers[self.racersCount].setH(self.bench[0].getH()+270)
		self.racers[self.racersCount].pose('standup',0)
		self.x={};
		self.x[0]=-12.3668;self.x[1]=-19.79;self.x[2]=-21.90;self.x[3]=-26.53;self.x[4]=-20.67;
		self.x[5]=-3;self.x[6]=13.93;self.x[7]=22.65;self.x[8]=24.74;self.x[9]=24.38;
		self.x[10]=18.65;self.x[11]=12.10;self.x[12]=-1.92;

		#x={-12.3668,-19.79,-21.90,-26.53,-20.67,-3,13.93,22.65,24.74,24.38,18.65,12.10,-1.92}
		self.y={}
		self.y[0]=42.92;self.y[1]=10.61;self.y[2]=-4.685;self.y[3]=-29.29;self.y[4]=-41.99;
		self.y[5]=-45;self.y[6]=-40.87;self.y[7]=-33.22;self.y[8]=-17.81;self.y[9]=-1.14;
		self.y[10]=21.30;self.y[11]=36.82;self.y[12]=45.5
		taskMgr.add(self.Move,"moveTask")
		taskMgr.add(self.racingInteraction,"moveTask")

		#print "init"
#g = Game()
#run()
