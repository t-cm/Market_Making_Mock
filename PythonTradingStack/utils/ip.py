import requests
import uuid

def get_ip_address():
    """Get public IP address."""
    try:
        response = requests.get('https://httpbin.org/ip')
        return response.json()['origin']
    except Exception as e:
        print(f"Error getting IP address: {e}")
        return None

def get_location(ip):
    """Get location based on IP address."""
    try:
        response = requests.get(f'https://ipinfo.io/{ip}/json')
        return response.json()
    except Exception as e:
        print(f"Error getting location info: {e}")
        return None
    
def get_mac_address():
    """Get the MAC address of the computer."""
    try:
        mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) 
                        for elements in range(0,2*6,2)][::-1])
        return mac
    except Exception as e:
        print(f"Error getting MAC address: {e}")
        return None

def info():
    ip = get_ip_address()
    if ip:
        print(f"Your IP address is: {ip}")
        location = get_location(ip)
        if location:
            city = location.get('city', 'Unknown city')
            region = location.get('region', 'Unknown region')
            country = location.get('country', 'Unknown country')
            org = location.get('org', 'Unknown organization')
            print(f"You are located in: {city}, {region}, {country}")
            print(f"Your ISP is: {org}")

    mac = get_mac_address()
    if mac:
        print(f"Your MAC address is: {mac}")

def get_city():
    ip = get_ip_address()
    if ip:
        print(f"Your IP address is: {ip}")
        location = get_location(ip)
        if location:
            city = location.get('city', 'Unknown city')

    return city

if __name__ == '__main__':
    main()
