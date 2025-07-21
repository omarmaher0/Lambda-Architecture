
# 💹 Lambda Architecture - Crypto Price Pipeline

A complete data engineering mini-project applying **Lambda Architecture** using:
- 📦 Batch data (historical crypto prices from Kaggle)
- 🔁 Streaming data (live prices from CoinGecko API)
- 🛢 PostgreSQL for storage
- 🐍 Python for ETL
- 📊 Simple Streamlit Dashboard

---

## 📁 Project Structure

```
lambda-architecture-crypto-pipeline/
├── data/
│   └── crypto_batch.csv         # Historical BTC & ETH data (Kaggle)
├── scripts/
│   ├── insert_batch.py          # Insert historical data into PostgreSQL
│   └── stream_live_prices.py    # Stream live prices from CoinGecko API
├── db/
│   └── schema.sql               # PostgreSQL tables and views
├── analytics/
│   └── price_trends.sql        # SQL queries for basic analysis
├── streamlit_app/
│   └── app.py                   # [Coming Soon] Real-time dashboard
└── README.md
```

---

## 🧠 What is Lambda Architecture?

Lambda Architecture combines:
- **Batch Layer**: Precomputed historical data
- **Speed Layer**: Real-time streaming data
- **Serving Layer**: Combined view for queries

---

## 🗂️ Tables and Views

| Table/View        | Description                                 |
|-------------------|---------------------------------------------|
| `btc_batch`       | Historical BTC & ETH prices from Kaggle     |
| `live_prices`     | Live crypto prices from CoinGecko API       |
| `combined_prices` | Unified view of batch + stream data         |

---

## 🚀 How to Run

### 1. Setup PostgreSQL using Docker

```bash
docker run --name pg-lambda -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres
```

### 2. Run schema.sql to create tables and views

```bash
psql -h localhost -U postgres -f db/schema.sql
```

### 3. Insert Batch Data (from Kaggle)

```bash
python batch_bitcoin.py
```

### 4. Start Streaming Data

```bash
python stream_prices.py
```

### 5. Create view in PostgreSQL

```sql
CREATE OR REPLACE VIEW combined_prices AS
SELECT
    'BTC' AS symbol,
    TO_TIMESTAMP("Date", 'MM/DD/YYYY') AS timestamp,
    REPLACE("Price", ',', '')::FLOAT AS price,
    'batch' AS source
FROM btc_batch

UNION ALL

SELECT
    symbol,
    timestamp,
    price,
    'stream' AS source
FROM live_prices;
```

### 6. Run Streamlit

```bash
python streamlit run streamlit.py
```

---

## 📈 Sample Queries

```sql
-- Latest 10 prices
SELECT * FROM combined_prices ORDER BY timestamp DESC LIMIT 10;

-- Average price per symbol
SELECT symbol, ROUND(AVG(price)::numeric, 2) AS avg_price
FROM combined_prices
GROUP BY symbol;
```

---

## 🔍 Next Steps

- ✅ Add Streamlit Dashboard (Real-time chart)
- ✅ Add Airflow DAG to automate the pipeline
- ✅ Add anomaly alerts if prices jump/drop suddenly

---

## 🔗 Dataset Sources

- [📥 Kaggle: Bitcoin and Ethereum Prices](https://www.kaggle.com/datasets/kapturovalexander/bitcoin-and-ethereum-prices-from-start-to-2023)
- [⚡ CoinGecko API - Real-Time Prices](https://www.coingecko.com/en/api/documentation)

---

## 🙌 Author

**Omar Oun**  
💼 Data Engineer in the making | Passionate about pipelines  
📩 Feel free to connect on [LinkedIn](https://www.linkedin.com/in/omaroun/)
