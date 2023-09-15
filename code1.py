import requests

url = "https://linkedin-profiles1.p.rapidapi.com/extract"

querystring = {"url":"https://ca.linkedin.com/in/paulmeade","html":"1"}

headers = {
	"X-RapidAPI-Key": "a4f269e18emsha89bef224263fb4p1deff7jsn3b2d4ccaa791",
	"X-RapidAPI-Host": "linkedin-profiles1.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())