import json
import os
import requests
import time
from dotenv import load_dotenv
load_dotenv()

ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
TOKEN = os.getenv('TOKEN')
X_DEFAULT_TOKEN = os.getenv('X_DEFAULT_TOKEN')

# Function to get the nearest warehouse location


def get_nearest_warehouse(lat, lon):
    headers = {
        "access_token": ACCESS_TOKEN,
        "token": TOKEN,
        "x_default_token": X_DEFAULT_TOKEN,
    }
    url = f"https://getirx-client-api-gateway.getirapi.com/main?lat={lat}&lon={lon}"
    response = requests.get(url, headers=headers)
    data = response.json()
    if "result" not in data or data["result"]["message"] != "SUCCESS!!!":
        print(url, data["result"], "data" in data and "mainWarehouse" in data["data"]
              and data["data"]["mainWarehouse"])
    else:
        print("OK", url)
    return response.json()


# Define a range of latitudes and longitudes to cover Istanbul
# Approximate range for Istanbul
min_lat, max_lat = 40.85, 41.2  # Approximate range for Istanbul
min_lon, max_lon = 28.65, 29.35

# Step sizes to create a grid (adjust for density)
lat_step = 0.01
lon_step = 0.01

# Calculate the number of iterations
lat_iterations = int((max_lat - min_lat) / lat_step) + 1
lon_iterations = int((max_lon - min_lon) / lon_step) + 1

# Total number of iterations
total_iterations = lat_iterations * lon_iterations

# Collect all warehouse locations
# Collect all warehouse locations
warehouses = {}
unique_warehouses = []
lat = min_lat
i = 0
while lat <= max_lat:
    lon = min_lon
    while lon <= max_lon:
		i+=1
        try:
            print(total_iterations, "iterations left")
            total_iterations -= 1
            result = get_nearest_warehouse(lat, lon)
            # Assuming each warehouse has a unique 'id' field
            warehouse = result and result["data"]["mainWarehouse"] if "data" in result and "mainWarehouse" in result["data"] else None
            warehouse_id = warehouse and warehouse["id"]
            if warehouse_id and warehouse_id not in warehouses:
				warehouse["last_lat"] = lat
				warehouse["last_lon"] = lon
				warehouse["i"] = i
                warehouses[warehouse_id] = warehouse
                unique_warehouses.append(warehouse)
        except Exception as e:
            print(e)
        lon += lon_step
        time.sleep(0.1)  # To avoid overwhelming the server
		if i % 100 == 0:
			with open('warehouses.json', 'w', encoding="utf-8") as f:
				json.dump(unique_warehouses, f, indent=4, ensure_ascii=False)
    lat += lat_step
