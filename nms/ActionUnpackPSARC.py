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
import contextlib
import re
from .BaseAction import BaseAction
from .PSArchive import PSArchive

class ActionUnpackPSARC(BaseAction):
	def _sorted_table(self, arc):
		table = [ (index, filename) for (filename, index) in arc.filetable.items() ]
		if self._regex is not None:
			table = [ (index, filename) for (index, filename) in table if self._regex.fullmatch(filename) ]
		table.sort()
		return table

	def _uncompress_archive(self, arc, output_dir):
		for (index, filename) in self._sorted_table(arc):
			filename = filename.lstrip("/")
			full_filename = output_dir + "/" + filename
			full_dirname = os.path.dirname(full_filename)
			with contextlib.suppress(FileExistsError):
				os.makedirs(full_dirname)
			arc.write_fileno(index, full_filename)

	def _list_archive(self, arc):
		for (index, filename) in self._sorted_table(arc):
			print("   %3d: %s" % (index, filename))

	def _unpack(self, filename):
		with PSArchive(filename) as arc:
			print("%s" % (filename))
			if self._args.output_dir is None:
				self._list_archive(arc)
			else:
				self._uncompress_archive(arc, self._args.output_dir)

	def run(self):
		if self._args.regex is None:
			self._regex = None
		else:
			self._regex = re.compile(self._args.regex, flags = re.IGNORECASE)
		for filename in self._args.pakfile:
			self._unpack(filename)
