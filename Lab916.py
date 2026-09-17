import requests


# A Census API URL always has this shape:
# https://api.census.gov/data/{year}/{dataset}?get={variables}&for={geography}

YEAR = 2020
DATASET = "dec"
URL= f"https://api.census.gov/data/{YEAR}/{DATASET}"
API_KEY = "117161b093bc52158ea736159835419e409da344"

params = {
        "get": "NAME,P1_001N",
        "for": "state:*",
        "key": API_KEY,
}

response = requests.get(URL, params=params)


if response.status_code != 200:
        print(f"Request failed ({response.status_code})")
        print(response.text)
        raise SystemExit(1)
data = response.json()

#The API returns a list of lists. The first row is the column headers.
data = response.json()
print(data)
header  = data[0]
rows = data[1:]

print(f"Got {len(rows)} rows back.")

print(header)
for row in rows:
        print(row)
