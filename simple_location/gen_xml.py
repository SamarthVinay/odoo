
countries = ['Country A', 'Country B', 'Country C']
states_per_country = 5
cities_per_state = 10

xml = ['<?xml version="1.0" encoding="utf-8"?>', '<odoo>', '<data>']

for i, country_name in enumerate(countries):
    c_id = f"country_{i}"
    xml.append(f'<record id="{c_id}" model="location.country"><field name="name">{country_name}</field></record>')
    
    for j in range(states_per_country):
        s_name = f"{country_name} State {j+1}"
        # Make ids unique
        s_id = f"state_{i}_{j}"
        xml.append(f'<record id="{s_id}" model="location.state"><field name="name">{s_name}</field><field name="country_id" ref="{c_id}"/></record>')
        
        for k in range(cities_per_state):
            city_name = f"{country_name} State {j+1} City {k+1}"
            city_id = f"city_{i}_{j}_{k}"
            xml.append(f'<record id="{city_id}" model="location.city"><field name="name">{city_name}</field><field name="state_id" ref="{s_id}"/></record>')

xml.append('</data>')
xml.append('</odoo>')

print("\n".join(xml))
