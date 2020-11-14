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

import sys
import os
import collections
import contextlib
from .BaseAction import BaseAction
from .Savegame import Savegame

class ActionSortStorage(BaseAction):
	def _is_mergable(self, item):
		if set(item.raw_data.keys()) != set(['#classification', '#identifier', '#quantity', '#max_quantity', 'eVk', 'b76', '#position']):
			return False
		if set(item.raw_data["#classification"].keys()) != set([ "#category" ]):
			return False
		if item.raw_data["b76"] is not True:
			return False
		return True

	def _group_items(self, items):
		grouped = collections.defaultdict(list)
		for item in items:
			grouped[item.merge_key].append(item)
		return grouped

	def _merge_items(self, items):
		grouped = self._group_items(items)
		merged = [ ]
		for items in grouped.values():
			ref_item = items[0]
			total_quantity = sum(item.quantity for item in items)
			max_quantity = ref_item.max_quantity

			left_quantity = total_quantity
			while left_quantity > 0:
				next_quantity = max_quantity if (left_quantity >= max_quantity) else left_quantity
				left_quantity -= next_quantity
				merged.append(ref_item.template(next_quantity))
		return merged

	def _sort_items(self, items):
		def item_key(item):
			if item.dbentry is None:
				return (9999, item.identifier, -item.quantity)
			else:
				return (item.dbentry.order, item.identifier, -item.quantity)
		items.sort(key = item_key)

	def run(self):
		self._save = Savegame(self._args.savefile)
		boxes = list(self._save.storage_inventories)

		merge_items = [ ]
		for box in boxes:
			for item in box:
				if self._is_mergable(item):
					merge_items.append(item)
					box.remove(item)
		merged_items = self._merge_items(merge_items)
		self._sort_items(merged_items)

		try:
			for box in boxes:
				for free_slot in box.free_slots:
					item = merged_items.pop(0)
					box.put(item, free_slot)
		except IndexError:
			# All finished!
			pass

		for box in boxes:
			box.dump()

		sorted_file = self._args.savefile + "_sorted"
		backup_file = self._args.savefile + ".bak"
		if self._args.force:
			with contextlib.suppress(FileNotFoundError):
				os.unlink(sorted_file)
			with contextlib.suppress(FileNotFoundError):
				os.unlink(backup_file)
		else:
			if os.path.exists(sorted_file):
				print("Refusing to overwrite: %s" % (sorted_file))
				sys.exit(1)
			if os.path.exists(backup_file):
				print("Refusing to overwrite: %s" % (backup_file))
				sys.exit(1)


		self._save.write(sorted_file)
		os.rename(self._args.savefile, backup_file)
		os.rename(sorted_file, self._args.savefile)
