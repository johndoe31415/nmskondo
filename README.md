# nmskondo
nmskondo is a tool for the computer game "No Man's Sky" which allows you to
sort your inventory across multiple storage boxes and also offers to decompile
the .pak PSARC archives in order to get to internal game data.

## Usage
Please see the help page, it's pretty straightforward:
```
Syntax: ./nmskondo.py [command] [options]

Available commands:
    showinventory      Show inventory
    sortstorage        Sort storage inventories
    unpack             Unpack PSARC (*.pak) archive

Options vary from command to command. To receive further info, type
    ./nmskondo.py [command] --help
```

Sorting storage:
```
usage: ./nmskondo.py sortstorage [-f] [-v] [--help] filename

Sort storage inventories

positional arguments:
  filename       Specifies the savegame filename.

optional arguments:
  -f, --force    Overwrite temporary files or backup files if they already exist.
  -v, --verbose  Increase verbosity. Can be specified multiple times.
  --help         Show this help page.
```

Unpacking of PSARC:
```
usage: ./nmskondo.py unpack [-r regex] [-o dirname] [-v] [--help] filename [filename ...]

Unpack PSARC (*.pak) archive

positional arguments:
  filename              PAK file(s) to unpack.

optional arguments:
  -r regex, --regex regex
                        Only process files which match this regex. By default, all files are chosen.
  -o dirname, --output-dir dirname
                        Uncompress files in this directory. If not given, just list files.
  -v, --verbose         Increase verbosity. Can be specified multiple times.
  --help                Show this help page.
```

## License
GNU GPL-3
