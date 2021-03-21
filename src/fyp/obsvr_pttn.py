from typing import List 

class Observer: 
	# call by device and pass itself as argument 
	def update(self,publisher : 'Publisher') -> None : 
		pass 

class Publisher: 
	def __init__(self):
		self.observer_queue:List['Observer'] = [] 

	def attach_observer(self, observer: Observer) -> None :
		self.observer_queue.append(observer)

	def notify_all_observer(self):
		for observer in self.observer_queue: 
			observer.update(self)

	def __del__(self): 
		self.observer_queue.clear()
