#!/bin/bash

original_midi="$1"
python extract.py $original_midi
./pred/FCM notes/$original_midi.notes $2 > new_notes/$original_midi
python write.py new_notes/$original_midi $3
timidity generated/$original_midi

