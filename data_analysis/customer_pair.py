import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file containing product and unique customer pair counts
df = pd.read_csv('data_analysis/num_unique_customer_pair_per_product.csv')

# Sort the DataFrame in descending order by the number of customer pairs and select the top 5 products
top5 = df.sort_values(by='num_customer_pair', ascending=False).head(5)

# Create a bar chart
plt.figure(figsize=(10, 6))
bars = plt.bar(top5['Product'], top5['num_customer_pair'], color='skyblue')

# Add value labels on each bar
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, height, f'{int(height)}', 
             ha='center', va='bottom', fontsize=10)

plt.xlabel('Product')
plt.ylabel('Number of Unique Customer Pairs')
plt.title('Top 5 Products with Most Unique Customer Pairs')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
