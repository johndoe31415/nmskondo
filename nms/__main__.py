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
from .MultiCommand import MultiCommand
from .ActionShowInventory import ActionShowInventory
from .ActionSortStorage import ActionSortStorage
from .ActionUnpackPSARC import ActionUnpackPSARC

mc = MultiCommand()

def genparser(parser):
	parser.add_argument("-m", "--mode", choices = [ "full", "idonly" ], default = "full", help = "Show different aspects of inventories. Can be one of %(choices)s, defaults to %(default)s.")
	parser.add_argument("-v", "--verbose", action = "count", default = 0, help = "Increase verbosity. Can be specified multiple times.")
	parser.add_argument("savefile", metavar = "filename", type = str, help = "Specifies the savegame filename.")
mc.register("showinventory", "Show inventory", genparser, action = ActionShowInventory, aliases = [ "inv" ])

def genparser(parser):
	parser.add_argument("-f", "--force", action = "store_true", help = "Overwrite temporary files or backup files if they already exist.")
	parser.add_argument("-v", "--verbose", action = "count", default = 0, help = "Increase verbosity. Can be specified multiple times.")
	parser.add_argument("savefile", metavar = "filename", type = str, help = "Specifies the savegame filename.")
mc.register("sortstorage", "Sort storage inventories", genparser, action = ActionSortStorage)

def genparser(parser):
	parser.add_argument("-r", "--regex", metavar = "regex", help = "Only process files which match this regex. By default, all files are chosen.")
	parser.add_argument("-o", "--output-dir", metavar = "dirname", help = "Uncompress files in this directory. If not given, just list files.")
	parser.add_argument("-v", "--verbose", action = "count", default = 0, help = "Increase verbosity. Can be specified multiple times.")
	parser.add_argument("pakfile", metavar = "filename", nargs = "+", help = "PAK file(s) to unpack.")
mc.register("unpack", "Unpack PSARC (*.pak) archive", genparser, action = ActionUnpackPSARC)

mc.run(sys.argv[1:])
