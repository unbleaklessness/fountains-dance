from fountain import Fountain, Color

class Patterns(object):
	"""docstring for Patterns"""
	f = Fountain()
	start_time = 0

	
	def get_pattern(self):
		#Call other pattern depending params
		pass

	def full_leap(self):
		commands =[]
		var = []
		delta_time = 1000
		for i in range(12):
		    var.append( self.f.turn_on_pumps(self.start_time,i) )
		    var.append( self.f.turn_off_pumps(self.start_time + delta_time,i) )
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
		    for i in range(12):
		        var.append(self.f.turn_on_pumps(period_duration* p  + self.start_time,(1,i) ) )
		        var.append(self.f.turn_on_pumps(period_duration* p  + self.start_time,(3,i) ) )
		        
		    commands.append( self.f.combine(*var) )
		    var = []
		    for i in range(12):
		        var.append(self.f.turn_on_pumps( period_duration* p  + self.start_time + period_duration / 2, (2,i) ) )
		        var.append(self.f.turn_off_pumps(period_duration* p  + self.start_time + period_duration / 2,(1,i) ) )
		        var.append(self.f.turn_off_pumps(period_duration* p  + self.start_time + period_duration / 2,(3,i) ) )
		        
		    
		    commands.append( self.f.combine(*var) )        
		    var = []
		    for i in range(12): 
		        var.append(self.f.turn_off_pumps(period_duration* p  + self.start_time + period_duration , (2,i) ) )
		    commands.append( self.f.combine(*var) )
		    var = []   
		#End
		
		return commands


p = Patterns()
commands = p.huge_waves() 
out = file("partiture.txt","w")
for i in range(len(commands) ):
    out.write(commands[i])
out.close()