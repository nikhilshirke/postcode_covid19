import pandas as pd
import folium

# TODO: Fetch cases csv on a daily basis
# https://data.nsw.gov.au/data/datastore/dump/21304414-1ff1-4243-a5d2-f52778048b29?bom=True
df1 = pd.read_csv(
    'covid-19-cases-by-notification-date-and-postcode-local-health-district-and-local-government-area.csv')
df2 = pd.read_csv('australian_postcodes.csv')
df2[(df2 != 0).all(1)]
df2 = df2[df2['state'] == 'NSW']
# Sum of cases for postcode
state_count = df1.groupby('postcode').count()

# state_count['postcode'] = state_count.index

df = state_count.merge(df2, how='left', on='postcode')
# long = df['long'] != 0
df = df[df['long'] != 0]
df = df.dropna()
# df

# NSW map
m = folium.Map([-33.8688, 151.2093])
for index, row in df.iterrows():
    if not row['long']:
        print(row['postcode'])
    marker_color = 'darkred'
    fill_color = 'darkpurple'

    folium.Circle(
        location=[row['lat'], row['long']],
        popup=row['locality'],
        tooltip=f"Postcode={row['postcode']} Cases={row['notification_date']}",
        radius=row['notification_date'] * 30,
        color=marker_color,
        fill=True,
        fill_color=fill_color,
    ).add_to(m)

m.save('covid.html')