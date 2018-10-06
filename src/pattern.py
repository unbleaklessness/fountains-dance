from fountain import Fountain, Color

class Patterns(object):
	"""docstring for Patterns"""
	f = Fountain()
	collors = ('r','g','b','y','m','c','w')
	start_time = 0
	duration = 10000
	count_of_elem = 15

	
	def get_pattern(self, start_time, duration, range):
		#range:
		#	0 - easy
		#	1 - medium
		#	2 - hight
		self.start_time = start_time
		self.duration = duration
		if range == 0:
			return self.rest()
		if range == 1:
			return self.pattern1()
		if range == 2:
			return self.huge_waves()

	def full_leap(self):
		commands =[]
		var = []
		for i in range(self.count_of_elem):
		    var.append( self.f.turn_on_pumps(self.start_time,i) )
		    var.append( self.f.turn_off_pumps(self.start_time + self.duration,i) )
		commands.append( self.f.combine( *var[0::2]) )
		commands.append( self.f.combine( *var[1::2]) )

		return commands

	def huge_waves(self):
		period_duration = 5000
		#Count of periods
		peroids = 5
		#commands list
		commands =[]
		var = []
		#body

		for p in range(peroids):
		    for i in range(self.count_of_elem):
		        var.append(self.f.turn_on_pumps(period_duration* p  + self.start_time,(1,i) ) )
		        var.append(self.f.turn_on_pumps(period_duration* p  + self.start_time,(3,i) ) )
		        
		    commands.append( self.f.combine(*var) )
		    var = []
		    for i in range(self.count_of_elem):
		        var.append(self.f.turn_on_pumps( period_duration* p  + self.start_time + period_duration / 2, (2,i) ) )
		        var.append(self.f.turn_off_pumps(period_duration* p  + self.start_time + period_duration / 2,(1,i) ) )
		        var.append(self.f.turn_off_pumps(period_duration* p  + self.start_time + period_duration / 2,(3,i) ) )
		        
		    
		    commands.append( self.f.combine(*var) )        
		    var = []
		    for i in range(self.count_of_elem): 
		        var.append(self.f.turn_off_pumps(period_duration* p  + self.start_time + period_duration , (2,i) ) )
		    commands.append( self.f.combine(*var) )
		    var = []   
		#End
		
		return commands

	def pattern1(self):
		commands = []
		colors = ("c","m","y")
		delta_time = self.duration /  3
		commands.append( "%s\tl10:y|m10:sf(15)|m1x1:sf(30)|m1x2:sf(30)|l1x1:r|l1x2:r|m2x1:sf(30)|m2x2:sf(30)|l2x1:c|l2x2:c|m3x1:sf(30)|m3x2:sf(30)|l3x1:m|l3x2:m\n" % self.f.format_milliseconds(self.start_time) )
		new_time = self.start_time + 500
		for i in range(1,4):
			commands.append("%s\tm%dx1:sf(100)|m%dx2:sf(100)|l1x1:%s|l1x2:%s|l2x1:%s|l2x2:%s|l3x1:%s" % ( self.f.format_milliseconds(new_time),i,i,colors[(i-1) % 3],colors[(i-1) % 3],colors[i % 3],colors[i % 3],colors[(i+1) % 3]) )
			if i!=1:
				commands.append( "|m%dx1:sf(30)|m%dx2:sf(30)" % (i-1,i-1) )
			commands.append("\n")
			new_time += delta_time
		commands.append("%s\tm1:off|m2:off|m3:off|m10:off\n" % self.f.format_milliseconds(new_time) )

		return commands

	def rest(self): 
		commands =[]
		commands.append("%s\tm7:on|m11:on|snake1:cwave(10,10)|snake2:cwave(10,10)|octagon1:cwave(10,10)|octagon2:cwave(10,10)|octagon3:cwave(10,10)|lsnake1:cLight(10,10,2)|lsnake2:cLight(10,10,2)\n" %  self.f.format_milliseconds(self.start_time) )
		commands.append("%s\tm7:off|lsnake1:off|lsnake2:off|m11:off|lsnake1:k|lsnake2:k" % self.f.format_milliseconds(self.start_time + self.duration ) )

		return commands

	def set_lamps(self,color):
		commands =[]
		var = []
		for i in range(self.count_of_elem):
			var.append("%s\tl%d:%s\n" % ( self.f.format_milliseconds(self.start_time  ), i, color ))
		commands.append( self.f.combine( *var ))
		return commands
	

p = Patterns()
commands = p.get_pattern(4500,1000,1)

out = file("partiture.txt","w")
for i in range(len(commands) ):
    out.write(commands[i])
out.close()