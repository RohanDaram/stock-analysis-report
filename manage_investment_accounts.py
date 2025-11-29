import json
import os
from typing import Dict, List, Any

JSON_FILE = "investment_accounts.json"


def load_accounts() -> Dict[str, Any]:
    """Load investment accounts from JSON file."""
    if not os.path.exists(JSON_FILE):
        return {"accounts": {}}
    
    with open(JSON_FILE, 'r') as f:
        return json.load(f)


def save_accounts(data: Dict[str, Any]) -> None:
    """Save investment accounts to JSON file."""
    with open(JSON_FILE, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"\n✓ Changes saved to {JSON_FILE}")


def view_all_accounts(data: Dict[str, Any]) -> None:
    """Display all accounts and their stocks."""
    accounts = data.get("accounts", {})
    
    if not accounts:
        print("\nNo accounts found.")
        return
    
    print("\n" + "="*60)
    print("ALL INVESTMENT ACCOUNTS")
    print("="*60)
    
    for account_id, account_info in accounts.items():
        print(f"\nAccount ID: {account_id}")
        print(f"Name: {account_info['name']}")
        print(f"Stocks:")
        
        if not account_info.get('stocks'):
            print("  (No stocks)")
        else:
            for stock in account_info['stocks']:
                print(f"  - {stock['ticker']}: {stock['no_of_stocks']} shares")
    
    print("="*60)


def add_account(data: Dict[str, Any]) -> None:
    """Add a new investment account."""
    print("\n--- Add New Account ---")
    
    account_id = input("Enter account ID (e.g., ac5): ").strip()
    
    if account_id in data["accounts"]:
        print(f"✗ Account '{account_id}' already exists!")
        return
    
    account_name = input("Enter account name (e.g., Traditional IRA): ").strip()
    
    if not account_name:
        print("✗ Account name cannot be empty!")
        return
    
    data["accounts"][account_id] = {
        "name": account_name,
        "stocks": []
    }
    
    save_accounts(data)
    print(f"✓ Account '{account_name}' ({account_id}) added successfully!")


def remove_account(data: Dict[str, Any]) -> None:
    """Remove an investment account."""
    print("\n--- Remove Account ---")
    view_all_accounts(data)
    
    account_id = input("\nEnter account ID to remove: ").strip()
    
    if account_id not in data["accounts"]:
        print(f"✗ Account '{account_id}' not found!")
        return
    
    account_name = data["accounts"][account_id]["name"]
    confirm = input(f"Are you sure you want to remove '{account_name}' ({account_id})? (yes/no): ").strip().lower()
    
    if confirm == "yes":
        del data["accounts"][account_id]
        save_accounts(data)
        print(f"✓ Account '{account_name}' removed successfully!")
    else:
        print("✗ Removal cancelled.")


def add_stock_to_account(data: Dict[str, Any]) -> None:
    """Add a stock to an existing account."""
    print("\n--- Add Stock to Account ---")
    view_all_accounts(data)
    
    account_id = input("\nEnter account ID: ").strip()
    
    if account_id not in data["accounts"]:
        print(f"✗ Account '{account_id}' not found!")
        return
    
    ticker = input("Enter stock ticker symbol (e.g., AAPL): ").strip().upper()
    
    # Check if stock already exists in this account
    for stock in data["accounts"][account_id]["stocks"]:
        if stock["ticker"] == ticker:
            print(f"✗ Stock '{ticker}' already exists in this account!")
            print(f"  Current quantity: {stock['no_of_stocks']} shares")
            print("  Use 'Update stock quantity' option to modify it.")
            return
    
    try:
        quantity = int(input("Enter number of shares: ").strip())
        if quantity <= 0:
            print("✗ Quantity must be greater than 0!")
            return
    except ValueError:
        print("✗ Invalid quantity! Please enter a number.")
        return
    
    data["accounts"][account_id]["stocks"].append({
        "ticker": ticker,
        "no_of_stocks": quantity
    })
    
    save_accounts(data)
    print(f"✓ Added {quantity} shares of {ticker} to {data['accounts'][account_id]['name']}!")


def remove_stock_from_account(data: Dict[str, Any]) -> None:
    """Remove a stock from an account."""
    print("\n--- Remove Stock from Account ---")
    view_all_accounts(data)
    
    account_id = input("\nEnter account ID: ").strip()
    
    if account_id not in data["accounts"]:
        print(f"✗ Account '{account_id}' not found!")
        return
    
    ticker = input("Enter stock ticker symbol to remove: ").strip().upper()
    
    stocks = data["accounts"][account_id]["stocks"]
    
    for i, stock in enumerate(stocks):
        if stock["ticker"] == ticker:
            confirm = input(f"Remove {stock['no_of_stocks']} shares of {ticker}? (yes/no): ").strip().lower()
            
            if confirm == "yes":
                stocks.pop(i)
                save_accounts(data)
                print(f"✓ Stock '{ticker}' removed from {data['accounts'][account_id]['name']}!")
            else:
                print("✗ Removal cancelled.")
            return
    
    print(f"✗ Stock '{ticker}' not found in this account!")


def update_stock_quantity(data: Dict[str, Any]) -> None:
    """Update the quantity of shares for a stock in an account."""
    print("\n--- Update Stock Quantity ---")
    view_all_accounts(data)
    
    account_id = input("\nEnter account ID: ").strip()
    
    if account_id not in data["accounts"]:
        print(f"✗ Account '{account_id}' not found!")
        return
    
    ticker = input("Enter stock ticker symbol: ").strip().upper()
    
    for stock in data["accounts"][account_id]["stocks"]:
        if stock["ticker"] == ticker:
            print(f"Current quantity: {stock['no_of_stocks']} shares")
            
            try:
                new_quantity = int(input("Enter new quantity: ").strip())
                if new_quantity <= 0:
                    print("✗ Quantity must be greater than 0!")
                    return
            except ValueError:
                print("✗ Invalid quantity! Please enter a number.")
                return
            
            stock["no_of_stocks"] = new_quantity
            save_accounts(data)
            print(f"✓ Updated {ticker} quantity to {new_quantity} shares in {data['accounts'][account_id]['name']}!")
            return
    
    print(f"✗ Stock '{ticker}' not found in this account!")


def display_menu() -> None:
    """Display the main menu."""
    print("\n" + "="*60)
    print("INVESTMENT ACCOUNT MANAGEMENT")
    print("="*60)
    print("1. View all accounts")
    print("2. Add new account")
    print("3. Remove account")
    print("4. Add stock to account")
    print("5. Remove stock from account")
    print("6. Update stock quantity")
    print("7. Exit")
    print("="*60)


def main():
    """Main menu loop."""
    print("Welcome to Investment Account Manager!")
    
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-7): ").strip()
        
        data = load_accounts()
        
        if choice == "1":
            view_all_accounts(data)
        elif choice == "2":
            add_account(data)
        elif choice == "3":
            remove_account(data)
        elif choice == "4":
            add_stock_to_account(data)
        elif choice == "5":
            remove_stock_from_account(data)
        elif choice == "6":
            update_stock_quantity(data)
        elif choice == "7":
            print("\nGoodbye!")
            break
        else:
            print("\n✗ Invalid choice! Please enter a number between 1 and 7.")


if __name__ == "__main__":
    main()
