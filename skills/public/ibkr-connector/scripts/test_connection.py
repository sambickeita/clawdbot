#!/usr/bin/env python3
"""
Test script for IBKR API connection.
Verifies connectivity to TWS or IB Gateway.

Usage:
    python test_connection.py [--host HOST] [--port PORT] [--client-id ID]
"""

import sys
import time
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.common import *
from ibapi.utils import iswrapper

class IBKRClient(EWrapper, EClient):
    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, self)
        self.connected = False
        self.next_order_id = None
        self.error_count = 0
        self.server_time = None

    @iswrapper
    def error(self, reqId, errorCode, errorString):
        self.error_count += 1

        # Ignore market data info messages
        if errorCode in [2104, 2106, 2158]:
            return

        print(f"[ERROR] Code {errorCode}: {errorString}")

        # Critical errors
        if errorCode in [502, 504]:  # Connection errors
            self.connected = False

    @iswrapper
    def nextValidId(self, orderId):
        self.next_order_id = orderId
        print(f"[OK] Next valid order ID: {orderId}")
        self.connected = True

    @iswrapper
    def currentTime(self, time):
        self.server_time = time
        print(f"[OK] Server time: {time}")

    @iswrapper
    def connectAck(self):
        print("[OK] Connection acknowledged")

    def is_connected(self):
        return self.connected and self.next_order_id is not None

    def run(self):
        self.run()

def parse_args():
    args = {
        'host': '127.0.0.1',
        'port': 7497,
        'client_id': 0
    }

    for i, arg in enumerate(sys.argv[1:], 1):
        if arg == '--host' and i + 1 < len(sys.argv):
            args['host'] = sys.argv[i + 1]
        elif arg == '--port' and i + 1 < len(sys.argv):
            args['port'] = int(sys.argv[i + 1])
        elif arg == '--client-id' and i + 1 < len(sys.argv):
            args['client_id'] = int(sys.argv[i + 1])
        elif arg in ['--help', '-h']:
            print("Usage: python test_connection.py [--host HOST] [--port PORT] [--client-id ID]")
            print("\nDefaults:")
            print("  --host 127.0.0.1")
            print("  --port 7497 (Paper Trading) or 7496 (Live)")
            print("  --client-id 0")
            sys.exit(0)

    return args

def main():
    print("=" * 60)
    print("IBKR Connection Test")
    print("=" * 60)

    args = parse_args()

    print(f"\nConnecting to:")
    print(f"  Host: {args['host']}")
    print(f"  Port: {args['port']} ({'Paper Trading' if args['port'] == 7497 else 'Live Trading'})")
    print(f"  Client ID: {args['client_id']}")

    client = IBKRClient()

    try:
        client.connect(args['host'], args['port'], args['client_id'])
        print("[INIT] Connection initiated...")
    except Exception as e:
        print(f"[FAIL] Could not initiate connection: {e}")
        print("\nPossible causes:")
        print("  1. TWS/IB Gateway is not running")
        print("  2. API is not enabled in TWS settings")
        print("  3. Incorrect port number")
        print("  4. Firewall blocking connection")
        sys.exit(1)

    # Start message thread
    client.nextOrderId()

    # Wait for connection with timeout
    timeout = 10
    elapsed = 0
    interval = 0.1

    print(f"\nWaiting for connection (timeout: {timeout}s)...")

    while not client.is_connected() and elapsed < timeout:
        time.sleep(interval)
        elapsed += interval
        client.nextOrderId()  # Keep connection alive

    if client.is_connected():
        print("\n" + "=" * 60)
        print("[SUCCESS] Connection established!")
        print("=" * 60)
        print(f"Next Order ID: {client.next_order_id}")
        if client.server_time:
            print(f"Server Time: {client.server_time}")
        print(f"Errors encountered: {client.error_count}")

        # Test server time
        print("\n[TEST] Requesting server time...")
        client.reqCurrentTime()
        time.sleep(1)

        # Disconnect gracefully
        print("\n[CLEANUP] Disconnecting...")
        client.disconnect()
        print("[DONE] Connection test completed successfully")

        return 0
    else:
        print("\n" + "=" * 60)
        print("[FAIL] Connection timeout")
        print("=" * 60)
        print("\nTroubleshooting:")
        print("  1. Ensure TWS or IB Gateway is running and logged in")
        print("  2. Check API Settings in TWS:")
        print("     - Enable 'ActiveX and Socket Clients'")
        print("     - Verify Socket Port matches the one used here")
        print("  3. Check for firewall blocking port", args['port'])
        print("  4. Try restarting TWS/IB Gateway")
        client.disconnect()
        return 1

if __name__ == "__main__":
    sys.exit(main())
