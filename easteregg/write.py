from midiutil.MidiFile import MIDIFile
from sys import argv

values = {
        "C":0,
        "C#":1,
        "D":2,
        "D#":3,
        "E":4,
        "F":5,
        "F#":6,
        "G":7,
        "G#":8,
        "A":9,
        "A#":10,
        "B":11,
        "B-":11,
}

def convertNote(note):
        return ((int(note[-1:]) + 1) * 12) + values[note[:-1]]
        
notes_and_duration = []
track    = 0
channel  = 0
time     = 0   # In beats
tempo    = int(argv[2])  # In BPM
volume   = 100 # 0-127, as per the MIDI standard

MyMIDI = MIDIFile(2)
MyMIDI.addTempo(0, time, tempo)
MyMIDI.addTempo(1, time, tempo)


counter = 0

with open(name=argv[1]) as f:
        lines = f.readlines()
for line in lines:
        try:
                #print line
                line = line.replace(" ", "")
                if len(line) != 0:
                        parts = line.split(",")
                        notes_and_duration.append((parts[0], float(parts[1])))
        except:
                continue

for note in notes_and_duration:
        if(note[0] != "Rest"):
                print note[1]
                MyMIDI.addNote(track, channel, convertNote(note[0]), time+note[1], note[1], volume)
        print note[0]
        time = time + note[1]
        if counter >= 100:
                break

track    = 1
time     = 0

#for i in range(0, len(notes_and_duration)):
#        MyMIDI.addNote(track, channel, 10, time, 0.1, volume)
#        time = time+1

with open("generated/" + argv[1].split('/')[1], "wb") as output_file:
        MyMIDI.writeFile(output_file)
