from music21 import *
import sys

piece = converter.parse(sys.argv[1])

all_parts = []
out = ""
i = 0;
for part in piece.parts:
  part_tuples = []
  #print(str(i) + "- " + str(part[0].bestName()))
  print(str(i) + "- " + str(type(part[0]).__name__))
  
  
  i+=1

choice = int(raw_input("Number: "))  
for event in piece.parts[choice]:
  for y in event.contextSites():
    if y[0] is part:
      offset = y[1]
  if getattr(event, 'isNote', None) and event.isNote:
    #part_tuples.append((event.nameWithOctave, event.quarterLength, offset))
    out += str(event.nameWithOctave) + ", " + str(event.quarterLength) + ";"
  if getattr(event, 'isRest', None) and event.isRest:
    #part_tuples.append(('Rest', event.quarterLength, offset))
    out += "Rest, " + str(event.quarterLength) + ";"

file = open("notes/" + sys.argv[1] + ".notes", "w")
file.write(out)
file.close()
