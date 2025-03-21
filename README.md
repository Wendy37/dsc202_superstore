# Superstore Data Analysis Using PostgreSQL and Neo4j
## Team 8 Members
Junjie Sun - jus025@ucsd.edu
Wendi Tan - w1tan@ucsd.edu
Sirui Cao - sic038@ucsd.edu

## Overview

This project analyzes the Superstore dataset using both SQL (relational database) and Neo4j (graph database) to extract business insights on sales, customer behavior, product returns, and regional trends. Additionally, the analysis is visualized using Tableau and Matplotlib to better understand key metrics like shipping times, profit margins, and return rates.

## Features

- SQL Analysis: Structured queries to extract sales, profit, and return insights.

- Neo4j Graph Analysis: Relationship-based queries to analyze customer-product connections.

- Tableau Visualizations: Interactive dashboards for regional sales, return rates, and profitability.

- Python Data Visualization: Bar charts and stacked graphs for return rates and customer-product relationships.

## Dataset

The Superstore dataset consists of the following key tables:

- Orders: Contains order details, including order date, customer ID, product information, and financial metrics.

- Returns: Tracks returned orders and their statuses.

- People: Lists regional managers for different regions.

## Presentation

The presentation recording is in 'Presentation' folder. And here is the slide https://docs.google.com/presentation/d/1lcVcrGlUor4GmLndRokM8eRTloybTlZE0C2mEVl4fVI/edit?usp=sharing.

## Report
Report pdf file is located in Report folder.

## How to Run

To activate the virtual environment, run the following command:
```
source venv/bin/activate
```

After activating the virtual environment, install the required packages:
```
pip install -r requirements.txt
```


PostgreSQL: 
Neo4j: 
```
python3 ./graph_db.py
``` 
then 
```
python3 ./graph_analysis.py
```