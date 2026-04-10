"""
Utility functions for ZoneDelivery
- Geolocation helpers
- Order management helpers
- Location validation
"""

import math
from decimal import Decimal
from django.conf import settings
from .models import Zone


def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate distance between two coordinates using Haversine formula
    Returns distance in meters
    
    Args:
        lat1, lon1: User location
        lat2, lon2: Zone center location
    
    Returns:
        float: Distance in meters
    """
    R = 6371000  # Earth's radius in meters
    
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = (math.sin(delta_phi / 2) ** 2 + 
         math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    distance = R * c
    return distance


def check_location_in_zones(latitude, longitude):
    """
    Check which zones contain the given location
    
    Args:
        latitude: User latitude
        longitude: User longitude
    
    Returns:
        dict: {
            'zones': list of zones user is in,
            'is_in_service': bool if in any zone,
            'service_zones': list of all zones with distance info
        }
    """
    zones = Zone.objects.filter(is_active=True)
    
    service_zones = []
    zones_inside = []
    
    for zone in zones:
        if zone.latitude and zone.longitude:
            distance = calculate_distance(
                latitude, longitude, 
                zone.latitude, zone.longitude
            )
            is_inside = distance <= zone.radius
            
            zone_info = {
                'zone_id': zone.id,
                'zone_name': zone.name,
                'is_inside': is_inside,
                'distance': round(distance, 2),
                'radius': zone.radius,
                'delivery_charge': str(zone.delivery_charge),
            }
            
            service_zones.append(zone_info)
            
            if is_inside:
                zones_inside.append(zone)
    
    return {
        'zones': zones_inside,
        'is_in_service': len(zones_inside) > 0,
        'service_zones': service_zones,
    }


def get_delivery_charge_for_zone(zone_id):
    """
    Get delivery charge for a specific zone
    
    Args:
        zone_id: Zone ID
    
    Returns:
        Decimal: Delivery charge
    """
    try:
        zone = Zone.objects.get(id=zone_id)
        return zone.delivery_charge
    except Zone.DoesNotExist:
        return Decimal('0')


def format_address_for_display(latitude, longitude, address_formatted=None):
    """
    Format address for display
    
    Args:
        latitude: Location latitude
        longitude: Location longitude
        address_formatted: Formatted address from Google Maps
    
    Returns:
        str: Formatted address
    """
    if address_formatted:
        return address_formatted
    else:
        return f"Lat: {latitude:.6f}, Lng: {longitude:.6f}"


def get_google_maps_api_key():
    """
    Get Google Maps API key from settings
    
    Returns:
        str: API key or None
    """
    api_key = getattr(settings, 'GOOGLE_MAPS_API_KEY', None)
    
    # Don't expose dummy key in production
    if api_key and 'YOUR_API_KEY_HERE' not in api_key:
        return api_key
    return None


def validate_coordinates(latitude, longitude):
    """
    Validate latitude and longitude values
    
    Args:
        latitude: User latitude
        longitude: User longitude
    
    Returns:
        tuple: (is_valid, error_message)
    """
    try:
        lat = float(latitude)
        lng = float(longitude)
        
        if -90 <= lat <= 90 and -180 <= lng <= 180:
            return True, None
        else:
            return False, "Invalid coordinate range"
    except (ValueError, TypeError):
        return False, "Invalid coordinate format"


def is_delivery_possible(latitude, longitude):
    """
    Check if delivery is possible at given coordinates
    
    Args:
        latitude: Location latitude
        longitude: Location longitude
    
    Returns:
        dict: {
            'is_possible': bool,
            'message': str,
            'zone': Zone object or None
        }
    """
    # Validate coordinates first
    is_valid, error = validate_coordinates(latitude, longitude)
    if not is_valid:
        return {
            'is_possible': False,
            'message': f"Invalid location: {error}",
            'zone': None
        }
    
    # Check zones
    result = check_location_in_zones(latitude, longitude)
    
    if result['is_in_service']:
        zone = result['zones'][0]  # First available zone
        return {
            'is_possible': True,
            'message': f"Delivery available in {zone.name} zone",
            'zone': zone
        }
    else:
        return {
            'is_possible': False,
            'message': "Location is outside our service zones",
            'zone': None
        }
