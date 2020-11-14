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

import re
import collections

class DB():
	_Item = collections.namedtuple("Item", [ "identifier", "item_type", "name", "order" ])
	__instance = None

	def __init__(self):
		self._db = { }
		self._db["jsonkeys"] = { }
		with open("identifiers.txt") as f:
			for line in f:
				line = line.strip(" \t\r\n").split()
				if len(line) == 2:
					(value, key) = line
					self._db["jsonkeys"][key] = value
		self._db["revjsonkeys"] = { value: key for (key, value) in self._db["jsonkeys"].items() }

		split_re = re.compile("\t+")
		self._db["items"] = { }
		with open("item_order.txt") as f:
			for (order, line) in enumerate(f):
				line = line.strip(" \t\r\n")
				if line.startswith("#") or (line == ""):
					continue
				line = split_re.split(line)
				if len(line) == 3:
					(identifier, item_type, name) = line
					item = self._Item(identifier = identifier, item_type = item_type, name = name, order = order)
					self._db["items"][item.identifier] = item


	@classmethod
	def get(cls):
		if cls.__instance is None:
			cls.__instance = cls()
		return cls.__instance._db
