import json
import requests

#Open the updated_query.txt json.
with open("updated_query.json", "r") as f:
  payload = f.read()


url = "https://search.rcsb.org/rcsbsearch/v2/query"
response = requests.post(url, json=payload)

if response.status_code == 200:
  # Parse the JSON response
  data = json.loads(response.text)
  # Print the results
  for hit in data["hits"]:
    print(hit["pdb_id"])
else:
  print("Error:", response.status_code)