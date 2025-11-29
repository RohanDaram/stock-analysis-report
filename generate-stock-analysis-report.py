import os
import datetime
import smtplib
import ssl
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Dict, List, Tuple, Any

import yfinance as yf
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

# JSON file path
JSON_FILE = "investment_accounts.json"


def load_investment_data() -> Tuple[Dict[str, str], Dict[str, List[Dict[str, Any]]]]:
    """Load investment account data from JSON file."""
    if not os.path.exists(JSON_FILE):
        print(f"Error: {JSON_FILE} not found!")
        return {}, {}
    
    with open(JSON_FILE, 'r') as f:
        data = json.load(f)
    
    accounts = data.get("accounts", {})
    
    # Extract account descriptions and investment accounts
    account_description = {}
    investment_accounts = {}
    
    for account_id, account_info in accounts.items():
        account_description[account_id] = account_info["name"]
        investment_accounts[account_id] = account_info["stocks"]
    
    return account_description, investment_accounts


# Load data from JSON file
ACCOUNT_DESCRIPTION, INVESTMENT_ACCOUNTS = load_investment_data()

EMAIL_CONFIG = {
    "from_email": os.getenv("EMAIL_FROM"),
    "to_email": os.getenv("EMAIL_TO"),
    "smtp_server": os.getenv("SMTP_SERVER"),
    "smtp_port": int(os.getenv("SMTP_PORT", 465)),
    "smtp_user": os.getenv("SMTP_USER"),
    "smtp_pass": os.getenv("SMTP_PASS")
}

def get_stock_data(ticker: str) -> Any:
    """Fetches 2 days of history for a given ticker."""
    data = yf.Ticker(ticker)
    #Two days history period to calculate change
    return data.history(period="2d")

def calculate_portfolio_performance(
    accounts: Dict[str, List[Dict[str, Any]]]
) -> Tuple[Dict[str, Any], float]:
    """
    Calculates performance for all accounts.
    Returns a dictionary with detailed data per account and the overall total change.
    """
    account_details = {}
    overall_total_change = 0.0

    for account_id, stock_list in accounts.items():
        
        account_name = ACCOUNT_DESCRIPTION.get(account_id, account_id)
        print(f"\nAccount: {account_name}")
        header_todays_change_percent = "Today's % Gain/Loss"
        header_todays_change = "Day's Change"
        print(f"{'Symbol':<10} {'Closing Price':<18} {'# of Stocks':<14} {header_todays_change_percent:<30} {header_todays_change:<25}")
        
        account_total_change = 0.0
        stocks_data = []

        for stock_info in stock_list:
            ticker = stock_info["ticker"]
            qty = stock_info["no_of_stocks"]
            
            history = get_stock_data(ticker)
            
            stock_data = {
                "ticker": ticker,
                "qty": qty,
                "price_curr": 0.0,
                "price_prev": 0.0,
                "price_diff": 0.0,
                "percent_change": 0.0,
                "total_change": 0.0,
                "has_data": False
            }

            if not history.empty and len(history) >= 2:
                price_prev = history["Close"].iloc[-2]
                price_curr = history["Close"].iloc[-1]
                price_diff = price_curr - price_prev
                percent_change = (price_diff / price_prev) * 100
                total_change = price_diff * qty

                stock_data.update({
                    "price_curr": price_curr,
                    "price_prev": price_prev,
                    "price_diff": price_diff,
                    "percent_change": percent_change,
                    "total_change": total_change,
                    "has_data": True
                })

                account_total_change += total_change
                
                print(
                    f"{ticker:<10} ${price_curr:<17.2f} {qty:<14} {percent_change:<30.2f} ${total_change:<25.2f}"
                )
            else:
                print(f"{ticker:<10} {'No Data':<12} {qty:<14} {'N/A':<20} {'N/A':<18}")

            stocks_data.append(stock_data)

        account_details[account_id] = {
            "name": account_name,
            "stocks": stocks_data,
            "total_change": account_total_change
        }
        overall_total_change += account_total_change
        print(f"Account Total Change: {account_total_change:.2f}")

    print(f"\nOverall Change Across all Accounts: {overall_total_change:.2f}")
    print("\nDisclaimer: Stock prices and changes are based on closing prices and may contain discrepancies.")
    print("After-hours trading may result in different current prices. Please verify all information before making any decisions.")
    return account_details, overall_total_change

def generate_html_report(
    account_details: Dict[str, Any], 
    overall_total: float,
    report_date: str
) -> str:
    """Generates the HTML email body from the calculated data."""
    msg_body = f"""
    <h2>Investment Report for xyz</h2>
    <p><strong>Report Generated on {report_date}</strong></p>
    <br>
    """
    
    for account_id, details in account_details.items():
        msg_body += f"<h3>Account: {details['name']}</h3>"
        msg_body += """
        <table border="1" cellpadding="5" cellspacing="0">
          <tr>
            <th>Symbol</th>
            <th>Stock Price</th>
            <th># of Stocks</th>
            <th>Today's % Gain/Loss</th>
            <th>Day's Change</th>
          </tr>
        """
        
        for stock in details["stocks"]:
            if stock["has_data"]:
                msg_body += (
                    f"<tr>"
                    f"<td>{stock['ticker']}</td>"
                    f"<td>{stock['price_curr']:.2f}</td>"
                    f"<td>{stock['qty']}</td>"
                    f"<td>{stock['percent_change']:.2f}%</td>"
                    f"<td>{stock['total_change']:.2f}</td>"
                    f"</tr>\n"
                )
            else:
                msg_body += (
                    f"<tr>"
                    f"<td>{stock['ticker']}</td>"
                    f"<td>No data</td>"
                    f"<td>{stock['qty']}</td>"
                    f"<td>No data</td>"
                    f"<td>No data</td>"
                    f"</tr>\n"
                )
        
        msg_body += "</table>\n"
        msg_body += f"<p><b> Today's Change: {details['total_change']:.2f}</b></p>"
        msg_body += "<br>"

    msg_body += f"<h3>Overall Change Across all Accounts: {overall_total:.2f}</h3>"
    msg_body += """
    <br>
    <p><em><strong>Disclaimer:</strong> Stock prices and changes are based on closing prices and may contain discrepancies.<br>
    After-hours trading may result in different current prices. Please verify all information before making any decisions.</em></p>
    """
    return msg_body

def send_email(subject: str, body: str):
    """Sends the email report."""
    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = EMAIL_CONFIG["from_email"]
    msg["To"] = EMAIL_CONFIG["to_email"]
    msg.attach(MIMEText(body, "html"))

    try:
        with smtplib.SMTP_SSL(EMAIL_CONFIG["smtp_server"], EMAIL_CONFIG["smtp_port"]) as server:
            server.login(EMAIL_CONFIG["smtp_user"], EMAIL_CONFIG["smtp_pass"])
            server.sendmail(EMAIL_CONFIG["from_email"], [EMAIL_CONFIG["to_email"]], msg.as_string())
            print("Email sent successfully.")
    except Exception as e:
        print("Error sending email:", e)


def analyze_portfolio_performance_with_llm(report_content: str) -> str:
    """Sends the report content to Azure OpenAI for analysis."""
    try:
        llm = ChatOpenAI(
            model = "gpt-4.1-nano",
            temperature=1.0,
            max_tokens=2000,
            top_p=0.95,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            streaming=False,
        )

        messages = [
            {
                "role": "system",
                "content": '''You are an expert stock analyst. When given a list of stocks with their daily price changes across multiple accounts, analyze all available data and provide a comprehensive summary of insights.
                            Identify which accounts and which individual stocks contributed most to gains or losses for the day.
                            Highlight notable trends, unusual movements, significant contributors, and any patterns that may help explain overall performance.
                            Present your analysis clearly, concisely, and in a way that is easy to act on.''',
            },
            {"role": "user", "content": report_content},
        ]

        print("\n--- AI Generated Portfolio Analysis ---")
        response = llm.invoke(messages)
        content = response.content
        print(content)
        print("\n-------------------")
        return content
    except Exception as e:
        error_msg = f"Skipping AI analysis due to error (likely missing credentials): {e}"
        print(f"\n{error_msg}")
        return error_msg


def main():
    """Orchestrates the data fetching, calculation, reporting, and analysis."""
    today = datetime.date.today().strftime("%B %d, %Y")
    print(f"Investment Report for xyz")
    print(f"Report Generated for {today}\n")
    
    # 1. Calculate Performance
    account_details, overall_total = calculate_portfolio_performance(INVESTMENT_ACCOUNTS)
    
    # 2. Generate Report
    portfolio_performance_report = generate_html_report(account_details, overall_total, today)
    
    # 3. AI Analysis
    ai_analysis = analyze_portfolio_performance_with_llm(portfolio_performance_report)
    
    # Add AI Analysis to the report
    portfolio_performance_report += f"""
    <br>
    <h3>AI Generated Portfolio Analysis</h3>
    <p style="white-space: pre-wrap;">{ai_analysis}</p>
    """
    
    # 4. Send Email
    today = datetime.date.today().isoformat()
    subject = f"Daily Stock Closing Prices for {today}"
    send_email(subject, portfolio_performance_report)
    
    print("\nDone.")


if __name__ == "__main__":
    main()
