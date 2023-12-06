#!/usr/bin/python
# Autoren: Florin Curiger, Enrique Munoz und Karma Khamritshang
# -------------------------------------------------------------

import requests

url = "https://twelve-data1.p.rapidapi.com/stocks"

querystring = {"exchange":"NASDAQ","format":"json"}

headers = {
	"X-RapidAPI-Key": "d6019f25cemsh8222ae809faa173p1d93c4jsn1e1718278767",
	"X-RapidAPI-Host": "twelve-data1.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())