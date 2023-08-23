import requests
import pandas as pd
from bs4 import BeautifulSoup
import datetime 

def load_html(url):
    headers = {
        'User-Agent': 'Your User Agent String'  # Replace with an appropriate User-Agent
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
    


month_conv = {
    'januari' : 1,
    'februari' : 2,
    'mars' : 3,
    'april' : 4,
    'maj' : 5,
    'juni' : 6,
    'juli' : 7,
    'augusti' : 8,
    'september' : 9,
    'oktober' : 10,
    'november' : 11,
    'december' : 12
}

def extract_rooms(room_text):
    if "rum" in room_text:
        room_parts = room_text.split(" ")
        for part in room_parts:
            if "rum" in part:
                rooms = part.replace(",", ".").replace("&nbsp;", "").replace("rum", "")
                try:
                    return float(rooms)
                except ValueError:
                    return 0.0
    return 0.0

def extract_date_format(date_str):
    try:
        date_arr = date_str.split(' ')

        day   = int(date_arr[1])
        month = month_conv[date_arr[2]]
        year  = int(date_arr[3])

        date = datetime.date(year, month, day)

    except:
        print('Error to extract date: %s' % date_str)
        date = None

    return date

def extract_values_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    results = []

    listings = soup.find_all('li', class_='sold-results__normal-hit')
    for listing in listings:
        data_element = listing.find('span', class_='hcl-label--sold-at')
        data = data_element.text.strip() if data_element else ""
        date = extract_date_format(data)

        address_element = listing.find('h2', class_='sold-property-listing__heading')
        address = address_element.text.strip() if address_element else ""

        avgift_element = listing.find('div', class_='sold-property-listing__fee')
        avgift_text = avgift_element.text.strip() if avgift_element else ""
        try:
            avgift = int(avgift_text.replace(" ", "").replace("\xa0", "").replace("kr/mån", "")) if avgift_text else 0
        except ValueError as avgift_error:
            print(f"Error extracting avgift: {avgift_error}")
            avgift = avgift_text

        slutpris_element = listing.find('span', class_='hcl-text hcl-text--medium')
        slutpris_text = slutpris_element.text.strip() if slutpris_element else ""
        try:
            slutpris = int(slutpris_text.replace(" ", "").replace("\xa0", "").replace("kr", "").replace("Slutpris", "")) if slutpris_text else 0
        except ValueError as slutpris_error:
            print(f"Error extracting slutpris: {slutpris_error}")
            slutpris = slutpris_text

        sqm_pris_element = listing.find('div', class_='sold-property-listing__price-per-m2')
        sqm_pris_text = sqm_pris_element.text.strip() if sqm_pris_element else ""
        try:
            sqm_pris = int(sqm_pris_text.replace(" ", "").replace("\xa0", "").replace("kr/m²", "")) if sqm_pris_text else 0
        except ValueError as sqm_pris_error:
            print(f"Error extracting sqm_pris: {sqm_pris_error}")
            sqm_pris = sqm_pris_text

        name_element = listing.find('span', class_='sold-property-listing__first')
        name = name_element.text.strip() if name_element else ""

        size_element = listing.find('div', class_='sold-property-listing__area')
        size_text = size_element.text.split('\n')[1].strip()
        try:
            size_parts = size_text.split()
            size_numeric = float(size_parts[0].replace(",", ".")) if size_parts[0] else 0.0
        except ValueError as size_error:
            print(f"Error extracting size: {size_error}")
            size_numeric = size_text
        
        room_text = size_element.text.split('\n')[-2].strip()
        try:
            rooms = extract_rooms(room_text)
        except :
            print(f"Error extracting rooms: %s" % room_text)
            rooms = 0.0

        results.append({
            "data": data,
            "date": date,
            "address": address,
            "avgift": avgift,
            "slutpris": slutpris,
            "sqm_pris": sqm_pris,
            "name": name,
            "size": size_numeric,
            "size_plus" : 'NaN',
            "rooms": rooms
        })

    return results



if __name__ == "__main__":
    url = input("Enter the URL: ")

    html_content = load_html(url)

    if html_content:
        print("Successfully lead data from %s" % url)
        # print(html_content)
    else:
        print("Failed to fetch HTML content.")