#	nmskondo - Tools for the game "No Man's Sky"
#	Copyright (C) 2020-2020 Johannes Bauer
#
#	This file is part of nmskondo.
#
#	nmskondo is free software; you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation; this program is ONLY licensed under
#	version 3 of the License, later versions are explicitly excluded.
#
#	nmskondo is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with nmskondo; if not, write to the Free Software
#	Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#	Johannes Bauer <JohannesBauer@gmx.de>

from .BaseAction import BaseAction
from .Savegame import Savegame

class ActionShowInventory(BaseAction):
	def run(self):
		self._save = Savegame(self._args.savefile)
		for inventory in self._save.inventories:
			if self._args.mode == "full":
				print("%s:" % (inventory.name))
				for item in inventory:
					print("   %s" % (item))
				print()
			elif self._args.mode == "idonly":
				for item in inventory:
					print("%s" % (item.identifier))
			else:
				raise NotImplementedError(self._args.mode)
