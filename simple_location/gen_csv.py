
import csv

countries = ['Country A', 'Country B', 'Country C']
states_per_country = 5
cities_per_state = 10

# 1. Countries
with open('data/location.country.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['id', 'name'])
    for i, country_name in enumerate(countries):
        writer.writerow([f'country_{i}', country_name])

# 2. States
with open('data/location.state.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['id', 'name', 'country_id:id'])
    for i, country_name in enumerate(countries):
        for j in range(states_per_country):
            s_name = f"{country_name} State {j+1}"
            s_id = f"state_{i}_{j}"
            writer.writerow([s_id, s_name, f'country_{i}'])

# 3. Cities
with open('data/location.city.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['id', 'name', 'state_id:id'])
    for i, country_name in enumerate(countries):
        for j in range(states_per_country):
            for k in range(cities_per_state):
                city_name = f"{country_name} State {j+1} City {k+1}"
                city_id = f"city_{i}_{j}_{k}"
                s_id = f"state_{i}_{j}"
                writer.writerow([city_id, city_name, s_id])

print("CSV generation complete.")
