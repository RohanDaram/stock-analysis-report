# 📈 Stock Analysis Report

> **Investment Portfolio Tracker & Daily Email Report**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![yfinance](https://img.shields.io/badge/yfinance-Market_Data-purple?style=for-the-badge)](https://github.com/ranaroussi/yfinance)
[![LangChain](https://img.shields.io/badge/🦜_LangChain-Framework-green?style=for-the-badge)](https://www.langchain.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-412991?style=for-the-badge&logo=openai&logoColor=white)](https://platform.openai.com/)
[![uv](https://img.shields.io/badge/uv-Package_Manager-DE5FE9?style=for-the-badge)](https://github.com/astral-sh/uv)

An intelligent stock portfolio analysis tool that fetches closing market data, generates comprehensive performance reports, and delivers AI-powered insights directly to your inbox.

---

## Features

- **Multi-Account Portfolio Tracking** - Manage multiple investment accounts (Roth IRA, 401(k), HSA, Brokerage, etc.)
- **Automated Email Reports** - HTML email reports sent daily with portfolio performance
- **AI-Powered Analysis** - Get insights about your portfolio using OpenAI's GPT models via LangChain
- **Real-Time Market Data** - Fetch closing stock prices and historical data using Yahoo Finance
- **Interactive Account Management** - Python script to add, remove, and update stocks across accounts
- **Performance Metrics** - Track daily gains/losses, percentage changes, and overall portfolio performance

---

## Tech Stack

This project utilizes the following tools/apis/packages for report generation and data analysis:

| Tools | Usage | Documentation |
|------------|---------|---------------|
| **[yfinance](https://github.com/ranaroussi/yfinance)** | Fetch closing stock market data from Yahoo Finance | [📖 Docs](https://pypi.org/project/yfinance/) |
| **[LangChain](https://www.langchain.com/)** | Framework for building LLM-powered applications | [📖 Docs](https://python.langchain.com/docs/get_started/introduction) |
| **[ChatOpenAI](https://platform.openai.com/docs/guides/chat)** | OpenAI's GPT models for intelligent portfolio analysis | [📖 Docs](https://python.langchain.com/docs/integrations/chat/openai) |
| **[uv](https://github.com/astral-sh/uv)** | Python package installer and resolver | [📖 Docs](https://docs.astral.sh/uv/) |
| **[python-dotenv](https://github.com/theskumar/python-dotenv)** | Environment variable management | [📖 Docs](https://pypi.org/project/python-dotenv/) |

---

## Prerequisites

- **Python 3.11+**
- **[uv](https://docs.astral.sh/uv/)** - Modern Python package manager
- **OpenAI API Key** - For AI-powered analysis
- **SMTP Email Account** - For sending reports

---

## Installation and Setup

### Install uv (if not already installed)
Using pip:
```bash
pip install uv
```
Using Homebrew (for Mac only):
```bash
brew install uv
```

### Clone the Repository

```bash
git clone https://github.com/RohanDaram/stock-analysis-report.git
cd stock-analysis-report
```

### Install Dependencies

Using **uv** for dependency resolution:

```bash
uv sync
```

This will create a virtual environment and install all dependencies from `pyproject.toml`.

### Configure Environment Variables

Update `.env` with your credentials:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Email Configuration
EMAIL_FROM=your_email@example.com
EMAIL_TO=recipient@example.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=465
SMTP_USER=your_email@example.com
SMTP_PASS=your_app_password_here
```

---

## Usage

### Manage Investment Accounts

Use the ```manage_investment_accounts.py``` script to manage your portfolio:

```bash
uv run python manage_investment_accounts.py
```

**Available Operations:**
1. View all accounts
2. Add new account
3. Remove account
4. Add stock to account
5. Remove stock from account
6. Update stock quantity

Your portfolio data is stored in `investment_accounts.json`.

### Generate Stock Analysis Report

Run generate-stock-analysis-report.py to:
- Fetch latest stock prices from **Yahoo Finance**
- Calculate portfolio performance
- Generate AI analysis using **ChatOpenAI** via **LangChain**
- Send email report

```bash
uv run generate-stock-analysis-report.py
```

### Automate Daily Reports

Set up a cron job (Linux/macOS) to run daily:

```bash
# Edit the crontab
crontab -e

# Add this line at the bottom, Example cron job (runs daily at 5 PM)
0 17 * * * cd /path/to/stock-analysis-report && uv run generate-stock-analysis-report.py

# Save and exit the crontab using the commands for your specific text editor
```

---

## Project Structure

```
stock-analysis-report/
├── generate-stock-analysis-report.py  # Main report generation script
├── manage_investment_accounts.py      # Account management script
├── investment_accounts.json           # Portfolio data storage
├── pyproject.toml                     # Project dependencies (uv)
├── uv.lock                            # Dependency lock file
├── .env                               # Environment variables (Edit with your own values)
├── .gitignore                       
└── README.md                          
```

---

## How It Works

### 1. Data Collection
- Loads portfolio from `investment_accounts.json`
- Fetches 2-day price history for each stock using **[yfinance](https://github.com/ranaroussi/yfinance)**
- Calculates daily price changes and percentage gains/losses

### 2. AI Analysis
- Sends portfolio performance data to **[ChatOpenAI](https://python.langchain.com/docs/integrations/chat/openai)** via **[LangChain](https://www.langchain.com/)**
- LLM analyzes trends, identifies top performers, and provides insights
- Generates commentary on portfolio movements

### 3. Report Generation
- Creates an HTML formatted email with:
  - Individual account performance tables
  - Overall portfolio change
  - AI-generated analysis
- Sends via SMTP to configured email address

---

## Disclaimer
*Stock prices and changes are based on closing prices and may contain discrepancies.
After-hours trading may result in different current prices. Please verify all information before making any decisions.*

## Sample Output

### Console Output
```
Investment Report for xyz
Report Generated for November 29, 2025


Account: Roth IRA
Symbol     Closing Price      # of Stocks    Today's % Gain/Loss            Day's Change             
AAPL       $278.85            50             0.47                           $65.00                    
MSFT       $492.01            50             1.34                           $325.50                   
Account Total Change: 390.50

Account: 401(k)
Symbol     Closing Price      # of Stocks    Today's % Gain/Loss            Day's Change             
VFIAX      $633.24            100            0.54                           $339.00                   
VTI        $336.31            100            0.56                           $187.00                   
Account Total Change: 526.00

Account: Individual Brokerage
Symbol     Closing Price      # of Stocks    Today's % Gain/Loss            Day's Change             
TSLA       $430.17            50             0.84                           $179.50                   
AMZN       $233.22            50             1.77                           $203.00                   
Account Total Change: 382.50

Account: HSA
Symbol     Closing Price      # of Stocks    Today's % Gain/Loss            Day's Change             
VOO        $628.41            100            0.55                           $346.00                   
VWENX      $84.84             100            0.27                           $23.00                    
Account Total Change: 369.00

Overall Change Across all Accounts: 1668.00

Disclaimer: Stock prices and changes are based on closing prices and may contain discrepancies.
After-hours trading may result in different current prices. Please verify all information before making any decisions.
--- AI Generated Portfolio Analysis ---
**Comprehensive Investment Performance Analysis – November 29, 2025**

---

### **Overall Summary**
- **Total Daily Change Across All Accounts:** +$1,668.00  
- **Major Contributors to Gains:** 
  - 401(k) Account: +$526.00
  - HSA Account: +$369.00
  - Brokerage Account: +$382.50
  - Roth IRA: +$390.50

Total gains are well-distributed, indicating balanced contributions from each account.

---

### **Account-Level Insights**

#### 1. **Roth IRA (+$390.50)**
- **Key Stocks:**
  - **MSFT:**  
    - Largest individual contributor in IRA (~$325.50).  
    - Percentage Gain: +1.34%  
    - Contribution: ~$325.50
  - **AAPL:**  
    - Smaller gain relative to MSFT (+0.47%).  
    - Contribution: ~$65.00

**Insight:** Microsoft (MSFT) significantly outperformed Apple (AAPL), contributing most to IRA’s gain. The high number of stocks (50 each) maintains stability with moderate gains.

---

#### 2. **401(k) (+$526.00)**
- **Key Stocks/ETFs:**
  - **VFIAX:**  
    - Gain: +$339.00, +0.54%  
  - **VTI:**  
    - Gain: +$187.00, +0.56%  

**Insight:** Both index funds performed solidly with similar percentage gains. The 401(k) shows strong contribution from broad market ETFs, indicating positive market sentiment.

---

#### 3. **Individual Brokerage (+$382.50)**
- **Key Stocks:**
  - **AMZN:**  
    - Notably high percentage gain (+1.77%), contributing ~$203.00  
  - **TSLA:**  
    - Gain of +$179.50, +0.84%
  
**Insight:** Amazon’s significant surge (1.77%) was a major driver, with Tesla also performing well. The notable rally in tech and e-commerce stocks boosted this account.

---

#### 4. **HSA (+$369.00)**
- **Key Holdings:**
  - **VOO (S&P 500 ETF):**  
    - Gain: +$346.00, +0.55%  
  - **VWENX (Balanced Fund):**  
    - Gain: +$23.00, +0.27%
  
**Insight:** The HSA benefits from broad-market exposure, with VOO providing most gains, aligned with positive overall market trends.

---

### **Notable Movements & Trends**
- **Broad Market Uplift:** Gains across ETFs (VFIAX, VOO) and index funds (VTI, VWENX) suggest a generally bullish market environment.
- **Tech and E-commerce Strength:** Amazon (AMZN) exhibited the highest individual stock percentage gain (1.77%), indicating robust sector performance.
- **Microsoft (MSFT):** Outperformed Apple in the IRA, showing strength in large-cap tech.
- **Consistent Gains:** All accounts posted positive gains, reflecting sustained upward momentum.

---

### **Key Takeaways for Action**
- **Maintain exposure in broad ETFs and market index funds** (VFIAX, VOO, VTI) given their stable gains.
- **Monitor high-growth stocks like Amazon (AMZN)** for potential continued rally opportunities.
- **Consider rebalancing toward tech stocks,** as they contributed substantially today.
- **Evaluate potential for profit-taking** in stocks with significant recent gains (e.g., AMZN and MSFT) if upward momentum shows signs of slowdown.

---

### **Summary in a Nutshell**
The overall positive performance indicates a healthy market environment with tech and broad-market ETFs leading gains. Amazon and Microsoft emerged as top individual contributors, while diversified ETF holdings across accounts provided stability and steady growth. Staying diversified and vigilant for sector rotations can help optimize future gains.

---

**Disclaimer:** All stock prices are closing prices as of November 29, 2025, and actual after-hours prices may differ. Always verify before making investment decisions.
```
## Screenshots of Running the Project Locally
Cloning the repository and running uv init to initialize the project.
<img src="images/Git Clone.png" alt="Screenshot of Git Clone">

Project structure after cloning and initializing the project.
<img src="images/Project Structure.png" alt="Screenshot of Project Structure">

Running ```uv add``` command to add dependencies to the project.
<img src="images/uv add.png" alt="Screenshot of uv command">
