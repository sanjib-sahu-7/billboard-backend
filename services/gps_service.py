def check_gps_violation(gps, allowed_zones):
    """
    gps: {"lat":..., "lon":...}
    allowed_zones: list of dicts with lat_min, lat_max, lon_min, lon_max
    Returns True if location is outside allowed zones
    """
    if not gps: 
        return False  # No GPS info, optional: treat as violation

    for zone in allowed_zones:
        if (zone['lat_min'] <= gps['lat'] <= zone['lat_max'] and
            zone['lon_min'] <= gps['lon'] <= zone['lon_max']):
            return False
    return True
