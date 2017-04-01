from madmom.features import notes
import os,sys

f = open("test.txt","r")
note = notes.load_notes(f)
notes.write_midi(note,"test.mid")
