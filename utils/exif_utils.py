from PIL import Image, ExifTags

def extract_exif_location(image_path):
    try:
        img = Image.open(image_path)
        exif = img._getexif()
        if not exif: return None
        gps = {}
        for tag, value in exif.items():
            decoded = ExifTags.TAGS.get(tag, tag)
            if decoded == "GPSInfo":
                for t in value:
                    gps[ExifTags.GPSTAGS.get(t, t)] = value[t]
        if not gps: return None

        def conv(coord):
            d = coord[0][0] / coord[0][1]
            m = coord[1][0] / coord[1][1]
            s = coord[2][0] / coord[2][1]
            return d + m / 60 + s / 3600

        lat = conv(gps['GPSLatitude'])
        if gps.get('GPSLatitudeRef') != 'N': lat = -lat
        lon = conv(gps['GPSLongitude'])
        if gps.get('GPSLongitudeRef') != 'E': lon = -lon
        return {"lat": lat, "lon": lon}
    except:
        return None
