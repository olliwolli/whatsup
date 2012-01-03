import time
from watch import *

class EventLog:
    
    def __init__(self):
        self.events = []
        
    def add(self, event):
        self.events.append([event, time.localtime()])
        
    def get_events(self):
        return self.events
    
    def to_s(self):
        s = ""
        for e in self.events:
            s = s + event_to_s(e[0]) + " "+ time.strftime(_("%H:%M:%S - %d/%m/%Y"), e[1]) +"\n"
        return s