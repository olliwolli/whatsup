#taken from http://blogmatrix.blogmatrix.com/:entry:blogmatrix-2007-12-05-0000/

import sys
import os
import os.path

import pyinotify

event_name_map = {
				"IN_CREATE" 	: 	[	_(" was created")	, _("Creation")		],
			   	"IN_DELETE" 	: 	[	_(" was deleted")	, _("Deletion")		],
			   	"IN_ACCESS" 	: 	[	_(" was accessed")	, _("Access")		],
			   	"IN_MODIFY" 	: 	[	_(" was modified")	, _("Modification")	],
			   	"IN_OPEN"   	: 	[	_(" was opened")	, _("Open")			]
			  }

def pathname_to_s(event):
	if not event.is_dir:
		return event.path+"/"+event.name
	else:
		return event.path

def event_perfect(event):
	return event_name_map[event.event_name][0]

def event_nomen(event):
	return event_name_map[event.event_name][1]

def event_to_s(event):
 	return pathname_to_s(event)+event_perfect(event)

class watch:

	def __init__(self, path, *av, **ad):
		self.notifier = None
		self.paths = [ path ] + list(av)

		self.mask = 0
		self.mask |= ( ad.get('all') or ad.get('access') ) and pyinotify.EventsCodes.IN_ACCESS or 0
		self.mask |= ( ad.get('all') or ad.get('attrib') ) and pyinotify.EventsCodes.IN_ATTRIB or 0
		self.mask |= ( ad.get('all') or ad.get('close_nowrite') ) and pyinotify.EventsCodes.IN_CLOSE_NOWRITE or 0
		self.mask |= ( ad.get('all') or ad.get('close_write') ) and pyinotify.EventsCodes.IN_CLOSE_WRITE or 0
		self.mask |= ( ad.get('all') or ad.get('create') ) and pyinotify.EventsCodes.IN_CREATE or 0
		self.mask |= ( ad.get('all') or ad.get('delete') ) and pyinotify.EventsCodes.IN_DELETE or 0
		self.mask |= ( ad.get('all') or ad.get('delete_self') ) and pyinotify.EventsCodes.IN_DELETE_SELF or 0
		self.mask |= ( ad.get('all') or ad.get('dont_follow') ) and pyinotify.EventsCodes.IN_DONT_FOLLOW or 0
		self.mask |= ( ad.get('all') or ad.get('ignored') ) and pyinotify.EventsCodes.IN_IGNORED or 0
		self.mask |= ( ad.get('all') or ad.get('isdir') ) and pyinotify.EventsCodes.IN_ISDIR or 0
		self.mask |= ( ad.get('all') or ad.get('mask_add') ) and pyinotify.EventsCodes.IN_MASK_ADD or 0
		self.mask |= ( ad.get('all') or ad.get('modify') ) and pyinotify.EventsCodes.IN_MODIFY or 0
		self.mask |= ( ad.get('all') or ad.get('move_self') ) and pyinotify.EventsCodes.IN_MOVE_SELF or 0
		self.mask |= ( ad.get('all') or ad.get('moved_from') ) and pyinotify.EventsCodes.IN_MOVED_FROM or 0
		self.mask |= ( ad.get('all') or ad.get('moved_to') ) and pyinotify.EventsCodes.IN_MOVED_TO or 0
		self.mask |= ( ad.get('all') or ad.get('onlydir') ) and pyinotify.EventsCodes.IN_ONLYDIR or 0
		self.mask |= ( ad.get('all') or ad.get('open') ) and pyinotify.EventsCodes.IN_OPEN or 0
		self.mask |= ( ad.get('all') or ad.get('q_overflow') ) and pyinotify.EventsCodes.IN_Q_OVERFLOW or 0
		self.mask |= ( ad.get('all') or ad.get('unmount') ) and pyinotify.EventsCodes.IN_UNMOUNT or 0

	def __iter__(self):
		wm = pyinotify.WatchManager()
		queued = []

		class PTmp(pyinotify.ProcessEvent):
			def process_default(self, event):
				queued.append(event)

		self.notifier = pyinotify.Notifier(wm, PTmp())

		for path in self.paths:
			wdd = wm.add_watch(path, self.mask, rec=True)

		while True:
			self.notifier.process_events()
			if self.notifier.check_events():
				self.notifier.read_events()

			while queued:
				yield	queued.pop(0)

	def __del__(self):
		if self.notifier:
			self.notifier.stop()