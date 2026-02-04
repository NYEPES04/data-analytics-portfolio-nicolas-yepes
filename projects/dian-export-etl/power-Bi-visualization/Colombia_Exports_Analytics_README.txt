🇨🇴 Colombia Exports Analytics – Power BI Dashboard (2023–2025)

Overview
This project presents an analytical dashboard built on top of official Colombian foreign trade microdata (DIAN), designed to explore export performance, market diversification, and the use of trade agreements.

The dashboard shown in this repository focuses on Colombia–Ecuador trade flows as a first use case, but it is powered by a comprehensive analytical base covering all Colombian exports over the last three years. The underlying dataset and pipeline are intentionally designed to support advanced analytical use cases beyond visualization, including predictive modeling and machine learning.

Objectives
- Transform raw DIAN export microdata into a clean, scalable analytical dataset
- Enable evidence-based analysis of export destinations, product and sector composition, and use of trade agreements
- Provide a reproducible foundation for future analytical models (forecasting, regression, clustering, ML)

Data Source
Source: Colombian National Tax and Customs Authority (DIAN)
Coverage:
- ~3.7 million records
- 79 variables
- Last 3 years of Colombian exports
Granularity: Transaction-level export data

Analytical Pipeline
Technologies used:
- Python
- DuckDB
- SQL
- Power BI

Key features:
- Incremental processing of large datasets
- SQL-first analytical transformations
- Separation between analytical base and visualization layer

Dashboard Description
The Power BI dashboard presents an exploratory and descriptive analysis focused on Colombia–Ecuador trade.

Key insights:
- Ecuador is the main destination for Colombian exports benefiting from trade agreements (≈ USD 1.8 billion).
- Ecuador is a key market for non-traditional exports.

Beyond the Dashboard
The analytical base enables forecasting, regression analysis, clustering, and machine learning use cases. The dashboard represents only the first analytical layer.

Future Work
- Export forecasting models
- Firm and product clustering
- Predictive analysis of trade agreement utilization
- Expansion to additional markets

Disclaimer
This project is for analytical and educational purposes only. All data is sourced from publicly available official records.

Feedback
Comments and suggestions are welcome.
