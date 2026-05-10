# AI-Driven Sentiment & Environmental Analytics 🚀

A multi-stream data pipeline that integrates real-time weather logging with local AI-powered sentiment analysis of global news.

## 🌟 Project Overview
This repository contains two main data pipelines designed to demonstrate end-to-end data engineering:
1.  **Political Sentiment Engine**: Scrapes news archives from The Guardian and real-time headlines via NewsAPI, processing them through a **local Llama 3 instance** via Ollama to categorize global sentiment.
2.  **Multi-City Weather Logger**: A persistent background service tracking atmospheric conditions in **Hamburg and London** to analyze regional climate trends.

## 🛠️ The Tech Stack
* **Language:** Python 3.14.4
* **AI Engine:** Llama 3 (Running locally via Ollama)
* **Data Handling:** Pandas, CSV Serialization
* **Visualization:** Excel Pivot Tables & Power Query
* **Environment:** Secure `.env` management for API credentials

## 📁 Project Structure
* `scripts/`: Contains the core logic for data fetching and AI processing.
* `images/`: Data visualizations and architecture snapshots.
* `.env.example`: Template for required API keys (OpenWeather, NewsAPI, The Guardian).

## 📊 Sample Insights
### Political Sentiment Analysis
By leveraging a local LLM, this project avoids cloud costs and maintains data privacy while classifying thousands of headlines.
![Guardian Sentiment Chart](images/guardian_chart.png)

### Weather Tracking (Hamburg vs. London)
Currently logging 24-hour cycles to compare temperature and humidity fluctuations between Northern Germany and the UK.

## 🚀 How to Run
1.  **Clone the repo:** `git clone https://github.com/vulevu228/AI-Weather-Sentiment.git`
2.  **Install dependencies:** `pip install pandas requests python-dotenv`
3.  **Setup Keys:** Rename `.env.example` to `.env` and add your API keys.
4.  **Run the Logger:** `python scripts/weather_logger.py`
