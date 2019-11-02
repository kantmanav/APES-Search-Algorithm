import requests

url = "http://0.0.0.0:8081/api/apes"
payload = {
"task": "search",
"data": [
		{
			"question": "What is the change in the genetic composition of a population over time?",
			"elastic_index": "chapter5"
		}
	]
}

r = requests.post(url=url, json=payload)
print (r.json())
