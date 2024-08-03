
import pandas as pd
import itertools
import googlemaps


gmaps = googlemaps.Client(key='')

# Load the data
data = pd.read_csv('data_supply_chain_data.csv')

# Create a list of IDs for Cartesian product
ls_ids = data['id'].tolist()  # Convert to list for cartesian product

# Create Cartesian product of IDs
cartesian_prod = list(itertools.product(ls_ids, ls_ids))

# Create DataFrame
df = pd.DataFrame(cartesian_prod, columns=['From', 'To'])
df["Time"] = None
df["From Addr"] = None
df["From city"] = None
df["To Addr"] = None
df["To city"] = None


# Function to get address and city from ID
def get_address_and_city(df, id):
    row = df[df['id'] == id]
    if not row.empty:
        return row['Address'].values[0], row['City'].values[0]
    else:
        return None, None


# Populate addresses and cities
for index, row in df.iterrows():
    from_addr, from_city = get_address_and_city(data, row['From'])
    to_addr, to_city = get_address_and_city(data, row['To'])

    df.at[index, 'From Addr'] = from_addr
    df.at[index, 'From city'] = from_city
    df.at[index, 'To Addr'] = to_addr
    df.at[index, 'To city'] = to_city

    if row['From'] == row['To']:
        df.at[index, 'Time'] = 0
        continue

    # Request directions
    directions_result = gmaps.directions(
        from_addr,
        to_addr,
        mode="transit"
    )

    if directions_result:
        df.at[index, 'Time'] = directions_result[0]["legs"][0]["duration"]["value"] / 3600
    else:
        df.at[index, 'Time'] = None

# Save DataFrame to CSV
df.to_csv('dist_matrix.csv', index=False)

