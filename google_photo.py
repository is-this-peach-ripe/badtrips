import googlemaps
import random
import os.path

KEY = "AIzaSyDAciMKDEcZASMZ1IkCr73wYycJxDcG1lY"
c = googlemaps.Client(key=KEY, timeout=2)


def get_photo(name, coord):
    fname = "static/" + name.replace(" ", "") + ".jpeg"
    if os.path.isfile(fname):
        print("from cache")
        return fname
    else:
        return "/static/burger.jpg"
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
        return "/static/burger.jpg"
    else:
        photo = c.places_photo(photo['photo_reference'], max_width=1000, max_height=1000)
        f = open(fname, 'wb')
        for chunk in photo:
            if chunk:
                f.write(chunk)
        f.close()
    return fname