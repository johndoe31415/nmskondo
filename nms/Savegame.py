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

import os
import json
from .Inventory import Inventory
from .DB import DB

class MappedDict():
	@classmethod
	def _deobfuscate_key(cls, key):
		db = DB.get()
		if key in db["revjsonkeys"]:
			key = "#" + db["revjsonkeys"][key]
		return key

	@classmethod
	def _obfuscate_key(cls, key):
		if key.startswith("#"):
			return DB.get()["jsonkeys"][key[1:]]
		else:
			return key

	@classmethod
	def _filter(cls, obj, key_handler):
		if isinstance(obj, dict):
			result = { }
			for (key, value) in obj.items():
				key = key_handler(key)
				result[key] = cls._filter(value, key_handler)
			return result
		elif isinstance(obj, list):
			return [ cls._filter(item, key_handler) for item in obj ]
		else:
			return obj

	@classmethod
	def deobfuscate(cls, obj):
		return cls._filter(obj, cls._deobfuscate_key)

	@classmethod
	def obfuscate(cls, obj):
		return cls._filter(obj, cls._obfuscate_key)

class Savegame():
	def __init__(self, filename):
		self._stat = os.stat(filename)
		with open(filename) as f:
			raw_data = json.loads(f.read().rstrip("\x00"))
			self._data = MappedDict.deobfuscate(raw_data)

	@property
	def storage_inventories(self):
		for i in range(1, 11):
			name = "#storage_%02d" % (i)
			yield Inventory(name, self._data["#player_data"][name])

	@property
	def inventories(self):
		for name in [ "#inventory", "#inventory_cargo", "#inventory_tech" ]:
			yield Inventory(name, self._data["#player_data"][name])
		yield from self.storage_inventories

	def write(self, filename):
		with open(filename, "w") as f:
			json.dump(MappedDict.obfuscate(self._data), f)
			f.write("\x00")
		os.utime(filename, (self._stat.st_atime, self._stat.st_mtime))

	def pretty_print(self, output_filename):
		with open(output_filename, "w") as f:
			json.dump(self._data, f, sort_keys = True, indent = 4)
