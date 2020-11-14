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

import copy
import collections
from .DB import DB

class InventoryItem():
	_DB = DB.get()["items"]

	def __init__(self, data):
		self._data = data

	@property
	def dbentry(self):
		return self._DB.get(self.identifier)

	@property
	def name(self):
		entry = self.dbentry
		if entry is not None:
			return entry.name

	@property
	def raw_data(self):
		return self._data

	@property
	def quantity(self):
		return self._data["#quantity"]

	@property
	def max_quantity(self):
		return self._data["#max_quantity"]

	@property
	def identifier(self):
		return self._data["#identifier"]

	@property
	def merge_key(self):
		return (self.identifier, self._data["eVk"])

	def template(self, quantity):
		clone = copy.deepcopy(self._data)
		clone["#position"] = { }
		clone["#quantity"] = quantity
		return InventoryItem(clone)

	def __repr__(self):
		if self.name is not None:
			return "%d / %d %s" % (self.quantity, self.max_quantity, self.name)
		else:
			return "%d / %d %s" % (self.quantity, self.max_quantity, self.identifier)

class Inventory():
	_AvailableSlot = collections.namedtuple("AvailableSlot", [ "x", "y" ])
	def __init__(self, name, data):
		self._name = name
		self._data = data
		self._available_slots = [ self._AvailableSlot(slot["#x"], slot["#y"]) for slot in self._data["#available_slots"] ]
		self._available_slots.sort(key = lambda slot: (slot.y, slot.x))
		self._available_slots = tuple(self._available_slots)

	@property
	def name(self):
		return self._name

	@property
	def width(self):
		return self._data["#width"]

	@property
	def height(self):
		return self._data["#height"]

	@property
	def slot_count(self):
		return len(self._available_slots)

	@property
	def all_slots(self):
		return self._available_slots

	@property
	def occupied_slots(self):
		return [ self._AvailableSlot(item["#position"]["#x"], item["#position"]["#y"]) for item in self._data["#content"] ]

	@property
	def free_slots(self):
		return sorted(set(self.all_slots) - set(self.occupied_slots), key = lambda slot: (slot.y, slot.x))

	def clear(self, slot):
		self._data["#content"] = [ item for item in self._data["#content"] if ((item["#position"]["#x"] != slot.x) or (item["#position"]["#y"] != slot.y)) ]

	def remove(self, item):
		slot = self._AvailableSlot(x = item.raw_data["#position"]["#x"], y = item.raw_data["#position"]["#y"])
		self.clear(slot)

	def put(self, item, slot):
		self.clear(slot)
		next_item_data = item.raw_data
		next_item_data["#position"]["#x"] = slot.x
		next_item_data["#position"]["#y"] = slot.y
		self._data["#content"].append(next_item_data)

	def dump(self):
		print("Inventory %s:" % (self.name))
		for item in self:
			print("    %s" % (item))
		print()

	def __iter__(self):
		for item in self._data["#content"]:
			yield InventoryItem(item)
