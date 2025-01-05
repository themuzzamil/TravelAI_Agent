import requests
from TravelAI.settings import tavily_search, GOMAP_API_KEY, llm

def getdistance(origin:str,destination:str):
    """
     Provide the distance and time by taking origin and destination
    """
    
    params = {
        "origin": origin,
        "destination": destination,
        "mode": "driving",  # Options: driving, walking, bicycling, transit
        "units": "metric",  # Options: metric or imperial
        "language": "en",  # Response language
        "region": "pk",  # Region biasing
        "alternatives": "true",  # Include alternative routes
        "avoid": "highways",  # Options: tolls, highways, ferries
        "traffic_model": "best_guess",  # Options: best_guess, pessimistic, optimistic
        "departure_time": "now",# Use 'now' or a UNIX timestamp
        "key": GOMAP_API_KEY,
        
    }

  
    url = "https://maps.gomaps.pro/maps/api/directions/json"

    try:
        
        response = requests.get(url, params=params)
        data = response.json()

        
        if data.get("status") == "OK":
            
            route = data["routes"][0]
            leg = route["legs"][0]

            
            distance = leg["distance"]["text"]
            duration = leg["duration"]["text"]
            return(f"Route Information\n Distance = {distance}\nTime = {duration}")

           

        else:
            return (f"API Error: {data.get('status')} - {data.get('error_message', 'No details provided')}")

    except Exception as e:
        return (f"Error occurred: {e}")
    
def search_nearby_places(destination: str, radius: int, place_type: str):
    """
    Search for nearby places using the gomaps.pro API and return specific details:
    name, address, rating, open_now status, and coordinates (latitude and longitude).
    """
    geocode_url = f'https://maps.gomaps.pro/maps/api/geocode/json?address={destination}&key={GOMAP_API_KEY}'
    try:
        geocode_response = requests.get(geocode_url)
        if geocode_response.status_code == 200:
            geocode_data = geocode_response.json()
            if geocode_data['status'] == 'OK' and geocode_data['results']:
                lat = geocode_data['results'][0]['geometry']['location']['lat']
                lng = geocode_data['results'][0]['geometry']['location']['lng']
                location = f"{lat},{lng}"
            else:
                return "Error: No results found for the given address."
        else:
            return f"Error: Failed to retrieve geocode information. Status code: {geocode_response.status_code}"

    except Exception as e:
        return f"Error: Geocoding request failed. Exception: {str(e)}"

    
    places_url = "https://maps.gomaps.pro/maps/api/place/nearbysearch/json"
    params = {
        "location": location,
        "radius": radius,  
        "type": place_type,
        "key": GOMAP_API_KEY,
    }

    try:
        places_response = requests.get(places_url, params=params)
        if places_response.status_code == 200:
            places_data = places_response.json()
            if places_data.get("status") == "OK":
                places = places_data.get("results", [])
                if not places:
                    return "No places found in the specified area."

              
                extracted_places = []
                for place in places:
                    place_details = {
                        "name": place.get("name", "No name available"),
                        "address": place.get("vicinity", "No address available"),
                        "rating": place.get("rating", "No rating available"),
                        "open_now": place.get("opening_hours", {}).get("open_now", "Not specified"),
                        "coordinates": place.get("geometry", {}).get("location", {})
                    }
                    extracted_places.append(place_details)
                return extracted_places

            else:
                return f"Error: API returned status {places_data.get('status')}. Message: {places_data.get('error_message', 'No error message')}"
        else:
            return f"Error: Failed to retrieve places. Status code: {places_response.status_code}"

    except Exception as e:
        return f"Error: Places request failed. Exception: {str(e)}"


def search(destination:str):
    """
    Perform a search using TavilySearchResults based on the user's destination city.
    """
    prompt = f"""
    Information about {destination} like news,events and famous places of destination
    """
    query = tavily_search(prompt)  
    return query


tool = [getdistance,search,search_nearby_places]
llm_tool = llm.bind_tools(tool)
