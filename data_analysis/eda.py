import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from xplotter.insights import *
from xplotter.formatter import format_spines

orders_path = "./dataset/Orders.csv"
returns_path = "./dataset/Returns.csv"
people_path = "./dataset/People.csv"

orders_df = pd.read_csv(orders_path)
returns_df = pd.read_csv(returns_path)
people_df = pd.read_csv(people_path)
print("Orders Table Shape:", orders_df.shape)
print("Returns Table Shape:", returns_df.shape)
print("People Table Shape:", people_df.shape)
print("\nMissing Data Summary:")
print(orders_df.isnull().sum())
print(returns_df.isnull().sum())
print(people_df.isnull().sum())


fig = plt.figure(constrained_layout=True, figsize=(13, 10))
gs = GridSpec(2, 2, figure=fig)
ax1 = fig.add_subplot(gs[0, :])

# Lineplot - Total Orders of Superstore Over Time 
sns.lineplot(data=orders_df['Order Date'].value_counts().sort_index(), ax=ax1, 
             color='darkslateblue', linewidth=2)

format_spines(ax1, right_border=False)
  
for tick in ax1.get_xticklabels():
    tick.set_rotation(45)
ax1.set_title('Total Orders of Superstore Over Time ', size=14, color='dimgrey')


if 'Ship Date' in orders_df.columns:
    orders_df['Ship Date'] = pd.to_datetime(orders_df['Ship Date'], errors='coerce')

# pd.to_csv("Orders_Formatted.csv", index=False)


# Order Count by Region (Pie Chart)
if 'Region' in orders_df.columns:
    region_counts = orders_df['Region'].value_counts()
    plt.figure(figsize=(8, 6))
    region_counts.plot.pie(autopct='%1.1f%%', colors=sns.color_palette("viridis", len(region_counts)))
    plt.title("Order Count by Region")
    plt.ylabel("")
    plt.show()

