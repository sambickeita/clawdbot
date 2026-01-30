#!/usr/bin/env python3
"""
Script pour placer des ordres via IBKR API.
Supporte Paper Trading (démonstration) et Live Trading.

Usage:
    python place_order.py AAPL BUY 100 --order-type MARKET
    python place_order.py SPY BUY 50 --order-type LIMIT --limit-price 450.00
    python place_order.py TSLA SELL 20 --order-type STOP --stop-price 240.00

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
from ibapi.contract import Contract
from ibapi.order import *
from ibapi.common import *
from ibapi.utils import iswrapper

class OrderClient(EWrapper, EClient):
    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, self)
        self.next_order_id = None
        self.order_status = None
        self.execution = None
        self.open_order = None
        self.error_messages = []

    @iswrapper
    def nextValidId(self, orderId):
        self.next_order_id = orderId

    @iswrapper
    def openOrder(self, orderId, contract, order, orderState):
        self.open_order = {
            'orderId': orderId,
            'symbol': contract.symbol,
            'action': order.action,
            'totalQuantity': order.totalQuantity,
            'orderType': order.orderType,
            'status': orderState.status
        }
        print(f"[ORDER] Order {orderId} opened: {contract.symbol} {order.action} {order.totalQuantity} @ {order.orderType}")

    @iswrapper
    def orderStatus(self, orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice):
        status_map = {
            "PendingSubmit": "Pending Submit",
            "PendingCancel": "Pending Cancel",
            "PreSubmitted": "Pre Submitted",
            "Submitted": "Submitted",
            "ApiPending": "API Pending",
            "ApiCancelled": "API Cancelled",
            "Cancelled": "Cancelled",
            "Filled": "Filled",
            "Inactive": "Inactive"
        }
        self.order_status = {
            'orderId': orderId,
            'status': status_map.get(status, status),
            'filled': filled,
            'remaining': remaining,
            'avgFillPrice': avgFillPrice,
            'lastFillPrice': lastFillPrice
        }
        print(f"[STATUS] Order {orderId}: {status_map.get(status, status)} - Filled: {filled}/{filled+remaining} @ ${avgFillPrice}")

    @iswrapper
    def execDetails(self, reqId, contract, execution):
        self.execution = {
            'symbol': contract.symbol,
            'side': execution.side,
            'shares': execution.shares,
            'price': execution.price,
            'time': execution.time
        }
        print(f"[EXEC] {contract.symbol} {execution.side} {execution.shares} @ ${execution.price}")

    @iswrapper
    def error(self, reqId, errorCode, errorString):
        self.error_messages.append(f"{errorCode}: {errorString}")

        # Ignore market data info messages
        if errorCode in [2104, 2106, 2158]:
            return

        print(f"[ERROR] Code {errorCode}: {errorString}")

def create_contract(symbol, secType="STK", exchange="SMART", currency="USD"):
    contract = Contract()
    contract.symbol = symbol
    contract.secType = secType
    contract.exchange = exchange
    contract.currency = currency
    return contract

def create_order(action, quantity, order_type, **kwargs):
    order = Order()
    order.action = action  # BUY or SELL
    order.totalQuantity = quantity
    order.orderType = order_type
    order.eTradeOnly = False
    order.firmQuoteOnly = False

    # Order type specific parameters
    if order_type == "LMT":
        if 'limit_price' not in kwargs:
            raise ValueError("Limit orders require --limit-price")
        order.lmtPrice = kwargs['limit_price']
    elif order_type == "STP":
        if 'stop_price' not in kwargs:
            raise ValueError("Stop orders require --stop-price")
        order.auxPrice = kwargs['stop_price']
    elif order_type == "STP_LMT":
        if 'stop_price' not in kwargs or 'limit_price' not in kwargs:
            raise ValueError("Stop-Limit orders require --stop-price and --limit-price")
        order.auxPrice = kwargs['stop_price']
        order.lmtPrice = kwargs['limit_price']

    return order

def parse_args(args):
    if len(args) < 4:
        print("Usage: python place_order.py SYMBOL ACTION QUANTITY [OPTIONS]")
        print("\nRequired:")
        print("  SYMBOL      - Stock symbol (e.g., AAPL)")
        print("  ACTION      - BUY or SELL")
        print("  QUANTITY    - Number of shares")
        print("\nOptions:")
        print("  --order-type TYPE    - MARKET (default), LIMIT, STOP, STP_LMT")
        print("  --limit-price PRICE   - Limit price (for LIMIT and STP_LMT)")
        print("  --stop-price PRICE    - Stop price (for STOP and STP_LMT)")
        print("  --host HOST          - TWS host (default: 127.0.0.1)")
        print("  --port PORT          - TWS port (default: 7497)")
        print("  --client-id ID       - Client ID (default: 1)")
        print("\nExamples:")
        print("  python place_order.py AAPL BUY 100")
        print("  python place_order.py SPY BUY 50 --order-type LIMIT --limit-price 450.00")
        print("  python place_order.py TSLA SELL 20 --order-type STOP --stop-price 240.00")
        sys.exit(1)

    result = {
        'symbol': args[0].upper(),
        'action': args[1].upper(),
        'quantity': int(args[2]),
        'order_type': 'MARKET',
        'host': os.getenv('IBKR_HOST', '127.0.0.1'),
        'port': int(os.getenv('IBKR_PORT', '7497')),
        'client_id': int(os.getenv('IBKR_CLIENT_ID', '1'))
    }

    if result['action'] not in ['BUY', 'SELL']:
        print(f"Error: ACTION must be BUY or SELL, got {result['action']}")
        sys.exit(1)

    # Parse optional arguments
    i = 3
    while i < len(args):
        if args[i] == '--order-type':
            if i + 1 < len(args):
                result['order_type'] = args[i + 1]
                i += 2
        elif args[i] == '--limit-price':
            if i + 1 < len(args):
                result['limit_price'] = float(args[i + 1])
                i += 2
        elif args[i] == '--stop-price':
            if i + 1 < len(args):
                result['stop_price'] = float(args[i + 1])
                i += 2
        elif args[i] == '--host':
            if i + 1 < len(args):
                result['host'] = args[i + 1]
                i += 2
        elif args[i] == '--port':
            if i + 1 < len(args):
                result['port'] = int(args[i + 1])
                i += 2
        elif args[i] == '--client-id':
            if i + 1 < len(args):
                result['client_id'] = int(args[i + 1])
                i += 2
        else:
            i += 1

    return result

def confirm_order(params):
    """Ask user to confirm order placement"""
    print("\n" + "=" * 60)
    print("ORDER CONFIRMATION")
    print("=" * 60)
    print(f"Symbol:     {params['symbol']}")
    print(f"Action:     {params['action']}")
    print(f"Quantity:   {params['quantity']}")
    print(f"Order Type: {params['order_type']}")
    if 'limit_price' in params:
        print(f"Limit Price: ${params['limit_price']:.2f}")
    if 'stop_price' in params:
        print(f"Stop Price:  ${params['stop_price']:.2f}")
    print(f"Environment: {'Paper Trading' if params['port'] == 7497 else 'Live Trading'}")
    print("=" * 60)

    response = input("\nConfirm order? (yes/no): ").lower()
    return response in ['yes', 'y']

def main():
    params = parse_args(sys.argv[1:])

    print(f"[INIT] Connecting to IBKR at {params['host']}:{params['port']}")

    # Confirm order before placing
    if not confirm_order(params):
        print("[CANCEL] Order cancelled by user")
        return 1

    client = OrderClient()

    try:
        client.connect(params['host'], params['port'], params['client_id'])
        print("[INIT] Connection initiated...")
    except Exception as e:
        print(f"[FAIL] Could not initiate connection: {e}")
        return 1

    # Start message thread
    client.nextOrderId()

    # Wait for next order ID
    timeout = 10
    elapsed = 0
    while client.next_order_id is None and elapsed < timeout:
        time.sleep(0.1)
        elapsed += 0.1
        client.nextOrderId()

    if client.next_order_id is None:
        print("[FAIL] Timeout waiting for connection")
        client.disconnect()
        return 1

    print(f"[OK] Connected. Next Order ID: {client.next_order_id}")

    # Create contract and order
    contract = create_contract(params['symbol'])
    order = create_order(
        params['action'],
        params['quantity'],
        params['order_type'],
        limit_price=params.get('limit_price'),
        stop_price=params.get('stop_price')
    )

    # Place order
    order_id = client.next_order_id
    print(f"\n[ORDER] Placing order {order_id}...")
    client.placeOrder(order_id, contract, order)
    client.next_order_id += 1

    # Wait for order status
    print("[WAIT] Waiting for order status...")
    time.sleep(1)

    # Monitor order status
    max_wait = 30
    elapsed = 0
    while elapsed < max_wait:
        if client.order_status and client.order_status['status'] in ['Filled', 'Cancelled']:
            break
        time.sleep(0.5)
        elapsed += 0.5

    # Summary
    print("\n" + "=" * 60)
    print("ORDER SUMMARY")
    print("=" * 60)

    if client.open_order:
        print(f"Order ID:   {client.open_order['orderId']}")
        print(f"Symbol:     {client.open_order['symbol']}")
        print(f"Action:     {client.open_order['action']}")
        print(f"Quantity:   {client.open_order['totalQuantity']}")
        print(f"Order Type: {client.open_order['orderType']}")

    if client.order_status:
        print(f"\nStatus:     {client.order_status['status']}")
        print(f"Filled:     {client.order_status['filled']}")
        print(f"Remaining:  {client.order_status['remaining']}")
        if client.order_status['filled'] > 0:
            print(f"Avg Price:  ${client.order_status['avgFillPrice']:.2f}")

    if client.execution:
        print(f"\nExecution:")
        print(f"  Symbol:  {client.execution['symbol']}")
        print(f"  Side:    {client.execution['side']}")
        print(f"  Shares:   {client.execution['shares']}")
        print(f"  Price:    ${client.execution['price']:.2f}")

    if client.error_messages:
        print(f"\nErrors ({len(client.error_messages)}):")
        for err in client.error_messages:
            print(f"  - {err}")

    print("=" * 60)

    client.disconnect()
    print("[DONE] Order placement completed")

    return 0

if __name__ == "__main__":
    sys.exit(main())
