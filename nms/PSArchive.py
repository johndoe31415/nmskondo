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

import zlib
import struct
import collections
from .NamedStruct import NamedStruct

class PSArchive():
	_PSARC_HEADER = NamedStruct((
		("L", "magic"),
		("H", "version_major"),
		("H", "version_minor"),
		("L", "compression_type"),
		("L", "toc_length"),
		("L", "toc_entry_size"),
		("L", "toc_entries"),
		("L", "block_size"),
		("L", "archive_flags"),
	), struct_extra = ">")
	_TOC_ENTRY = NamedStruct((
		("16s", "md5"),
		("L", "zindex"),
		("5s", "length"),
		("5s", "offset"),
	), struct_extra = ">")
	_BLOCK_ENTRY = NamedStruct((
		("H", "size"),
	), struct_extra = ">")

	_CompressedBlock = collections.namedtuple("CompressedBlock", [ "offset", "length" ])

	def __init__(self, filename):
		self._filename = filename
		self._f = None
		self._entries = None
		self._zblocks = None
		self._filetable = None

	@property
	def file_count(self):
		return len(self._entries)

	@property
	def filetable(self):
		if self._filetable is None:
			self._filetable = self._parse_filetable()
		return self._filetable

	def __enter__(self):
		self._f = open(self._filename, "rb")
		self._header = self._PSARC_HEADER.unpack_from_file(self._f)
		assert(self._header.magic == 0x50534152)
		assert(self._header.version_major == 1)
		assert(self._header.version_minor == 4)
		assert(self._header.compression_type == 0x7a6c6962)

		self._entries = [ ]
		for i in range(self._header.toc_entries):
			entry = self._TOC_ENTRY.unpack_from_file(self._f)
			self._entries.append(entry)

		zblocks = [ ]
		zblock_count = (self._header.toc_length - self._f.tell()) // self._BLOCK_ENTRY.size
		for i in range(zblock_count):
			block = self._BLOCK_ENTRY.unpack_from_file(self._f)
			zblocks.append(block)

		self._zblocks = [ ]
		for (entry_no, entry) in enumerate(self._entries):
			offset = int.from_bytes(entry.offset, byteorder = "big")
			if entry_no < len(self._entries) - 1:
				last_block = self._entries[entry_no + 1].zindex
			else:
				last_block = len(zblocks)
			contents = [ ]
			for zblock in zblocks[entry.zindex : last_block]:
				compressed_block = self._CompressedBlock(offset = offset, length = zblock.size)
				offset += compressed_block.length
				contents.append(compressed_block)
			self._zblocks.append(contents)
			if len(contents) == 0:
				offset += int.from_bytes(entry.length, byteorder = "big")

		self._filetable = None
		return self

	def _parse_filetable(self):
		content = self.read_fileno(0)
		return { line: index for (index, line) in enumerate(content.decode("utf-8").split("\n"), 1) }

	def read_fileno_chunked(self, index):
		entry = self._entries[index]
		zblocks = self._zblocks[index]
		offset = int.from_bytes(entry.offset, byteorder = "big")
		length = int.from_bytes(entry.length, byteorder = "big")
		if len(zblocks) == 0:
			self._f.seek(offset)
			compressed_data = self._f.read(length)
			uncompressed_data = zlib.decompress(compressed_data)
			yield uncompressed_data
			return

		assert(offset == zblocks[0].offset)
		for zblock in zblocks:
			self._f.seek(zblock.offset)
			compressed_data = self._f.read(zblock.length)
			try:
				uncompressed_data = zlib.decompress(compressed_data)
			except zlib.error as e:
				print("Decompression error in file %d: %s" % (index, str(e)))
				return
			yield uncompressed_data

	def read_fileno(self, index):
		return b"".join(self.read_fileno_chunked(index))

	def read(self, filename):
		fileno = self.filetable[filename]
		return self.read_fileno(fileno)

	def write_fileno(self, index, filename):
		print(index, filename)
		with open(filename, "wb") as f:
			for chunk in self.read_fileno_chunked(index):
				f.write(chunk)

	def __exit__(self, *args):
		self._f.close()

if __name__ == "__main__":
	with PSArchive("/tmp/NMSARC.FCA6A6EA.pak") as f:
		print(f.filetable)
