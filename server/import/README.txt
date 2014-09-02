Insert medium specification file and the medium itself inside this directory.
Afterwards, start importer.py, which will import all media inside this directory and DELETE them.

A medium specification file is build like the following:

[file]
filename=testfile.webm
extension=webm

[info]
media_type=Movie/Series/Music/Whaever
name=<<title goes here>>
genre=genretype
length=length of the medium in seconds
description=<<description for medium goes here>>

Such a file has to end in *.medium for the importer to include it.


