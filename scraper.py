#!/usr/bin/env python3
"""
eBird Alert Scraper
Fetches notable bird observations from eBird API and stores historical data
"""

import os
import json
import requests
from datetime import datetime
from typing import List, Dict, Any

# Configuration
EBIRD_API_KEY = os.environ.get('EBIRD_API_KEY')
HOTSPOT_ID = 'L197353'  # The eBird hotspot ID
API_BASE_URL = 'https://api.ebird.org/v2'
DATA_DIR = 'data'
HISTORICAL_FILE = os.path.join(DATA_DIR, 'historical.json')
LATEST_FILE = os.path.join(DATA_DIR, 'latest.json')


def fetch_notable_observations(hotspot_id: str, days_back: int = 7) -> List[Dict[str, Any]]:
    """
    Fetch notable observations from eBird API for a specific hotspot

    Args:
        hotspot_id: The eBird hotspot identifier
        days_back: Number of days back to search (default 7)

    Returns:
        List of observation dictionaries
    """
    if not EBIRD_API_KEY:
        raise ValueError("EBIRD_API_KEY environment variable not set")

    # Try notable observations for hotspot
    url = f'{API_BASE_URL}/data/obs/{hotspot_id}/recent/notable'
    headers = {'X-eBirdApiToken': EBIRD_API_KEY}
    params = {'back': days_back}

    print(f"Fetching notable observations from {url}")
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        # If hotspot doesn't work, try getting location info first
        print(f"Hotspot endpoint returned 404, trying location details...")
        loc_url = f'{API_BASE_URL}/ref/hotspot/info/{hotspot_id}'
        loc_response = requests.get(loc_url, headers=headers)

        if loc_response.status_code == 200:
            loc_info = loc_response.json()
            # Try using region code instead
            region_code = loc_info.get('subnationalCode') or loc_info.get('countryCode')
            if region_code:
                print(f"Trying region code: {region_code}")
                url = f'{API_BASE_URL}/data/obs/{region_code}/recent/notable'
                response = requests.get(url, headers=headers, params=params)
                if response.status_code == 200:
                    # Filter by hotspot location
                    all_obs = response.json()
                    return [obs for obs in all_obs if obs.get('locId') == hotspot_id]

        raise Exception(f"Failed to fetch observations: {response.status_code} - {response.text}")
    else:
        raise Exception(f"API request failed: {response.status_code} - {response.text}")


def process_observation(obs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process and clean observation data

    Args:
        obs: Raw observation dictionary from API

    Returns:
        Processed observation dictionary
    """
    return {
        'species_common_name': obs.get('comName', ''),
        'species_scientific_name': obs.get('sciName', ''),
        'species_code': obs.get('speciesCode', ''),
        'location_name': obs.get('locName', ''),
        'location_id': obs.get('locId', ''),
        'latitude': obs.get('lat'),
        'longitude': obs.get('lng'),
        'observation_date': obs.get('obsDt', ''),
        'observation_reviewed': obs.get('obsReviewed', False),
        'observation_valid': obs.get('obsValid', True),
        'observer_id': obs.get('userDisplayName', 'Unknown'),
        'subspecies_common_name': obs.get('subId', ''),
        'how_many': obs.get('howMany'),
        'checklist_id': obs.get('subId', '')
    }


def load_historical_data() -> List[Dict[str, Any]]:
    """Load historical data from JSON file"""
    if os.path.exists(HISTORICAL_FILE):
        with open(HISTORICAL_FILE, 'r') as f:
            return json.load(f)
    return []


def save_data(observations: List[Dict[str, Any]]):
    """
    Save observations to both historical and latest data files

    Args:
        observations: List of processed observations
    """
    timestamp = datetime.utcnow().isoformat() + 'Z'

    # Prepare current scrape data
    current_data = {
        'timestamp': timestamp,
        'hotspot_id': HOTSPOT_ID,
        'observation_count': len(observations),
        'observations': observations
    }

    # Save latest data (overwrites)
    with open(LATEST_FILE, 'w') as f:
        json.dump(current_data, f, indent=2)
    print(f"Saved {len(observations)} observations to {LATEST_FILE}")

    # Load and update historical data
    historical = load_historical_data()
    historical.append(current_data)

    with open(HISTORICAL_FILE, 'w') as f:
        json.dump(historical, f, indent=2)
    print(f"Updated historical data with {len(historical)} total scrapes")


def main():
    """Main scraper function"""
    print(f"Starting eBird scraper at {datetime.utcnow().isoformat()}")
    print(f"Hotspot ID: {HOTSPOT_ID}")

    try:
        # Fetch notable observations
        raw_observations = fetch_notable_observations(HOTSPOT_ID)
        print(f"Fetched {len(raw_observations)} notable observations")

        # Process observations
        processed = [process_observation(obs) for obs in raw_observations]

        # Save data
        save_data(processed)

        print("Scraping completed successfully!")

    except Exception as e:
        print(f"Error during scraping: {e}")
        raise


if __name__ == '__main__':
    main()
