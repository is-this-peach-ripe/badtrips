'''
piece = converter.parse(sys.argv[1])

all_parts = []
out = ""
i = 0;
for part in piece.parts:
  part_tuples = []
  #print(str(i) + "- " + str(part[0].bestName()))
  print(str(i) + "- " + str(type(part[0]).__name__))
  i+=1
'''

from music21 import converter,instrument, midi, stream # or import *
s = converter.parse('generated/the_moon2.mid')

#s.parts[0].insert(0, instrument.BassDrum())
#print s.parts[0].partAbbreviation

part = stream.Part()
print part.partName is None
part.insert(0, instrument.Clarinet())
print part.partName
#s.parts[1].insert(0, instrument.BassDrum())


mf = midi.translate.streamToMidiFile(s)
mf.open('generated/clarinet.mid', 'wb')
mf.write()
mf.close()