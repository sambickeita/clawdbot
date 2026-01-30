#!/usr/bin/env python3
"""
Script pour monitorer le portefeuille IBKR en temps réel.
Récupère les positions, le P&L et les données de compte.

Usage:
    python monitor_portfolio.py
    python monitor_portfolio.py --watch AAPL SPY MSFT

Environment Variables:
    IBKR_HOST       - TWS host (default: 127.0.0.1)
    IBKR_PORT       - TWS port (7497 for Paper, 7496 for Live)
    IBKR_CLIENT_ID  - Client ID (default: 1)
"""

import sys
import time
import os
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.common import *
from ibapi.utils import iswrapper
from datetime import datetime

class PortfolioMonitor(EWrapper, EClient):
    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, self)
        self.positions = {}
        self.portfolio = {}
        self.account_summary = {}
        self.pnl = {}
        self.connected = False
        self.data_received = False
        self.watch_symbols = []

    @iswrapper
    def nextValidId(self, orderId):
        self.connected = True
        print(f"[OK] Connected. Next Order ID: {orderId}")

    @iswrapper
    def position(self, account, contract, position, avgCost):
        self.positions[contract.symbol] = {
            'account': account,
            'symbol': contract.symbol,
            'position': position,
            'avgCost': avgCost,
            'secType': contract.secType,
            'exchange': contract.exchange,
            'currency': contract.currency
        }

    @iswrapper
    def positionEnd(self):
        print(f"[DATA] Received {len(self.positions)} positions")
        self.data_received = True

    @iswrapper
    def updatePortfolio(self, contract, position, marketPrice, marketValue, averageCost, unrealizedPNL, realizedPNL, accountName):
        self.portfolio[contract.symbol] = {
            'symbol': contract.symbol,
            'position': position,
            'marketPrice': marketPrice,
            'marketValue': marketValue,
            'averageCost': averageCost,
            'unrealizedPNL': unrealizedPNL,
            'realizedPNL': realizedPNL,
            'accountName': accountName
        }

    @iswrapper
    def accountDownloadEnd(self, accountName):
        print(f"[DATA] Portfolio download complete for {accountName}")
        self.data_received = True

    @iswrapper
    def accountSummary(self, reqId, account, tag, value, currency):
        if account not in self.account_summary:
            self.account_summary[account] = {}
        self.account_summary[account][tag] = {
            'value': value,
            'currency': currency
        }

    @iswrapper
    def accountSummaryEnd(self, reqId):
        print(f"[DATA] Account summary complete")
        self.data_received = True

    @iswrapper
    def pnl(self, reqId, dailyPnL, unrealizedPnL, realizedPnL):
        self.pnl = {
            'daily': dailyPnL,
            'unrealized': unrealizedPnL,
            'realized': realizedPnL
        }

    @iswrapper
    def error(self, reqId, errorCode, errorString):
        if errorCode in [2104, 2106, 2158]:
            return
        print(f"[ERROR] Code {errorCode}: {errorString}")

    def is_connected(self):
        return self.connected

def print_positions(positions):
    """Display current positions"""
    print("\n" + "=" * 80)
    print("POSITIONS")
    print("=" * 80)
    print(f"{'Symbol':<10} {'Position':>12} {'Avg Cost':>12} {'Sec Type':<8} {'Exchange':<8}")
    print("-" * 80)

    for symbol, pos in positions.items():
        print(f"{pos['symbol']:<10} {pos['position']:>12} ${pos['avgCost']:>11.2f} {pos['secType']:<8} {pos['exchange']:<8}")

    print("-" * 80)
    print(f"Total positions: {len(positions)}")
    print("=" * 80)

def print_portfolio(portfolio):
    """Display portfolio with market values and P&L"""
    print("\n" + "=" * 100)
    print("PORTFOLIO")
    print("=" * 100)
    print(f"{'Symbol':<10} {'Position':>12} {'Market Price':>14} {'Market Value':>16} {'Unrealized P&L':>18}")
    print("-" * 100)

    total_market_value = 0
    total_unrealized_pnl = 0

    for symbol, pos in portfolio.items():
        print(f"{pos['symbol']:<10} {pos['position']:>12} ${pos['marketPrice']:>13.2f} ${pos['marketValue']:>15.2f} ${pos['unrealizedPNL']:>17.2f}")
        total_market_value += pos['marketValue']
        total_unrealized_pnl += pos['unrealizedPNL']

    print("-" * 100)
    print(f"{'TOTAL':<10} {'':>12} {'':>14} ${total_market_value:>15.2f} ${total_unrealized_pnl:>17.2f}")
    print("=" * 100)

def print_account_summary(account_summary):
    """Display account information"""
    print("\n" + "=" * 60)
    print("ACCOUNT SUMMARY")
    print("=" * 60)

    for account, data in account_summary.items():
        print(f"\nAccount: {account}")
        print("-" * 60)

        important_tags = [
            'NetLiquidation',
            'AvailableFunds',
            'TotalCashValue',
            'GrossPositionValue',
            'MaintMarginReq',
            'EquityWithLoanValue'
        ]

        for tag in important_tags:
            if tag in data:
                value = data[tag]['value']
                currency = data[tag]['currency']
                print(f"  {tag:<25} {value:>15} {currency}")

    print("=" * 60)

def print_pnl(pnl):
    """Display P&L information"""
    print("\n" + "=" * 60)
    print("PROFIT & LOSS")
    print("=" * 60)
    print(f"Daily P&L:     ${pnl.get('daily', 0):>15.2f}")
    print(f"Unrealized P&L: ${pnl.get('unrealized', 0):>15.2f}")
    print(f"Realized P&L:   ${pnl.get('realized', 0):>15.2f}")
    print("=" * 60)

def parse_args(args):
    result = {
        'host': os.getenv('IBKR_HOST', '127.0.0.1'),
        'port': int(os.getenv('IBKR_PORT', '7497')),
        'client_id': int(os.getenv('IBKR_CLIENT_ID', '2')),
        'watch': []
    }

    for i, arg in enumerate(args):
        if arg == '--watch' and i + 1 < len(args):
            symbols = args[i + 1].upper().split(',')
            result['watch'] = [s.strip() for s in symbols]
        elif arg in ['--help', '-h']:
            print("Usage: python monitor_portfolio.py [OPTIONS]")
            print("\nOptions:")
            print("  --watch SYMBOLS    - Comma-separated symbols to watch (e.g., AAPL,SPY,MSFT)")
            print("  --host HOST         - TWS host (default: 127.0.0.1)")
            print("  --port PORT         - TWS port (default: 7497)")
            print("  --client-id ID      - Client ID (default: 2)")
            print("\nExample:")
            print("  python monitor_portfolio.py --watch AAPL,SPY,MSFT")
            sys.exit(0)

    return result

def main():
    params = parse_args(sys.argv[1:])

    print(f"[INIT] Connecting to IBKR at {params['host']}:{params['port']}")

    monitor = PortfolioMonitor()

    try:
        monitor.connect(params['host'], params['port'], params['client_id'])
        print("[INIT] Connection initiated...")
    except Exception as e:
        print(f"[FAIL] Could not initiate connection: {e}")
        return 1

    # Start message thread
    monitor.nextOrderId()

    # Wait for connection
    timeout = 10
    elapsed = 0
    while not monitor.is_connected() and elapsed < timeout:
        time.sleep(0.1)
        elapsed += 0.1
        monitor.nextOrderId()

    if not monitor.is_connected():
        print("[FAIL] Connection timeout")
        monitor.disconnect()
        return 1

    # Request all data
    print("\n[DATA] Requesting portfolio data...")
    monitor.reqPositions()
    monitor.reqAccountUpdates(True, "")
    monitor.reqAccountSummary(0, "All", "$LEDGER")

    # Wait for data
    print("[WAIT] Waiting for data...")
    time.sleep(3)

    # Check for P&L (requires account name)
    if monitor.positions:
        first_account = next(iter(monitor.positions.values()))['account']
        monitor.reqPnL(first_account, "")
        time.sleep(1)

    # Display results
    print(f"\n{'=' * 80}")
    print(f"PORTFOLIO MONITORING - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'=' * 80}")

    if monitor.positions:
        print_positions(monitor.positions)

    if monitor.portfolio:
        print_portfolio(monitor.portfolio)

    if monitor.account_summary:
        print_account_summary(monitor.account_summary)

    if monitor.pnl:
        print_pnl(monitor.pnl)

    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    if monitor.positions:
        num_positions = len(monitor.positions)
        print(f"Positions: {num_positions}")

    if monitor.pnl:
        daily_pnl = monitor.pnl.get('daily', 0)
        unrealized_pnl = monitor.pnl.get('unrealized', 0)
        realized_pnl = monitor.pnl.get('realized', 0)

        pnl_color = "🟢" if daily_pnl >= 0 else "🔴"
        print(f"Daily P&L: {pnl_color} ${daily_pnl:,.2f}")
        print(f"Total Unrealized: ${unrealized_pnl:,.2f}")
        print(f"Total Realized:   ${realized_pnl:,.2f}")

    print("=" * 80)

    # Stop updates
    monitor.reqAccountUpdates(False, "")
    monitor.disconnect()

    print("[DONE] Portfolio monitoring completed")

    return 0

if __name__ == "__main__":
    sys.exit(main())
