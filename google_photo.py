import googlemaps
import random
import os.path

KEY = "AIzaSyDAciMKDEcZASMZ1IkCr73wYycJxDcG1lY"
c = googlemaps.Client(key=KEY)


def get_photo(name, coord):
    fname = "static/" + name.replace(" ", "") + ".jpeg"
    if os.path.isfile(fname):
        return fname
    photo = None
    r = c.places(name, location=coord, radius=50000)
    #print(r['results'])
    for b in r['results']:
        if b['name'] == name:
            if 'photos' in b:
                photo = random.choice(b['photos'])
                break
    if photo is None:
        print("No photos...")
        return ""
    else:
        photo = c.places_photo(photo['photo_reference'], max_width=5000, max_height=5000)
        f = open(fname, 'wb')
        for chunk in photo:
            if chunk:
                f.write(chunk)
        f.close()
    return fname