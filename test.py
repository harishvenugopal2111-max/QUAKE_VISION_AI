from utils.api import get_live_earthquakes

df = get_live_earthquakes()

print(df.head())
print(df.shape)