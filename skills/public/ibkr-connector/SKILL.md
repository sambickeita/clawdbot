---
name: ibkr-connector
description: Full Interactive Brokers TWS API integration for trading automation. Use when connecting to Interactive Brokers for: (1) Retrieving market data (live quotes, historical data), (2) Managing orders (place, modify, cancel), (3) Monitoring positions and portfolio, (4) Account information and P&L tracking, (5) Market scanning and news feeds. Supports both Paper Trading (demo) and Live Trading environments.
---

# IBKR Connector

Interactive Brokers TWS API integration for automated trading operations.

## Prerequisites

### TWS/IB Gateway Setup

1. **Install TWS or IB Gateway**: Download from [Interactive Brokers](https://www.interactivebrokers.com/en/trading/tws.php)
   - TWS: Full GUI with trading tools
   - IB Gateway: Headless, 40% fewer resources (recommended for automation)

2. **Configure API Settings** (in TWS Global Configuration → API → Settings):
   - ✅ Enable "ActiveX and Socket Clients"
   - ❌ Disable "Read-Only API"
   - Set "Socket Port" (default: 7497 for TWS, 4001 for Paper Trading)
   - Enable "Create API Message Log File" for debugging

3. **Recommended Settings**:
   - Lock and Exit: "Never lock Trader Workstation" + "Auto restart"
   - Memory Allocation: 4000 MB (API users)
   - API → Precautions: Enable "Bypass Order Precautions for API orders"

### Python Dependencies

```bash
pip install ibapi  # Official IBKR Python API (requires Python 3.11+)
# OR
pip install ib_async  # Modern async wrapper (recommended)
```

### TWS API Version Sync

Use same version for TWS and API to avoid version conflicts. Check version in `C:\TWS API\API_VersionNum.txt`

## Connection

### Basic Connection Pattern

```python
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.common import *
import time

class IBKRClient(EWrapper, EClient):
    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, self)
        self.connected = False

    def error(self, reqId, errorCode, errorString):
        if errorCode == 2104 or errorCode == 2106:  # Market data OK
            return
        print(f"Error {errorCode}: {errorString}")

    def nextValidId(self, orderId):
        self.next_order_id = orderId
        print(f"Next valid order ID: {orderId}")
        self.connected = True

# Connect to Paper Trading
client = IBKRClient()
client.connect("127.0.0.1", 7497, clientId=0)  # Paper Trading port
client.nextOrderId()

# Wait for connection
while not client.connected:
    time.sleep(0.1)

print("Connected to IBKR!")
```

### Connection Parameters

| Environment | Host | Port | Notes |
|-------------|------|------|-------|
| Paper Trading | 127.0.0.1 | 7497 | Free demo account |
| Live Trading | 127.0.0.1 | 7496 | Real account |
| IB Gateway | 127.0.0.1 | 4001 | Headless mode |

### Disconnect

```python
client.disconnect()
```

## Market Data

### Live Market Data

```python
from ibapi.contract import Contract

def create_stock_contract(symbol, exchange="SMART", currency="USD"):
    contract = Contract()
    contract.symbol = symbol
    contract.secType = "STK"
    contract.exchange = exchange
    contract.currency = currency
    return contract

# Request live quotes
contract = create_stock_contract("AAPL")
client.reqMarketDataType(1)  # 1=Live, 2=Frozen, 3=Delayed, 4=DelayedFrozen
client.reqMktData(1, contract, "", False, False, [])

# Handle in EWrapper.tickPrice
def tickPrice(self, reqId, tickType, price, attrib):
    tickTypeStr = tickTypeToStr(tickType)
    print(f"{tickTypeStr}: {price}")
```

### Historical Data

```python
from ibapi.common import BarData

def req_historical_data(client, contract, duration="1 D", bar_size="1 hour"):
    client.reqHistoricalData(
        1,  # requestId
        contract,
        "",  # endDateTime (empty = now)
        duration,  # "1 D", "1 W", "1 M", "1 Y"
        bar_size,  # "1 min", "1 hour", "1 day"
        "MIDPOINT",  # whatToShow: TRADES, MIDPOINT, BID, ASK, etc.
        1,  # useRTH
        1,  # formatDate
        False,  # keepUpToDate
        []  # chartOptions
    )

def historicalData(self, reqId, bar):
    print(f"{bar.date} O:{bar.open} H:{bar.high} L:{bar.low} C:{bar.close} V:{bar.volume}")
```

See [references/historical-data-types.md](references/historical-data-types.md) for complete `whatToShow` options.

## Order Management

### Place Market Order

```python
from ibapi.order import *
from ibapi.contract import Contract

def place_market_order(client, contract, quantity, action="BUY"):
    order = Order()
    order.action = action  # BUY or SELL
    order.totalQuantity = quantity
    order.orderType = "MKT"
    order.eTradeOnly = False
    order.firmQuoteOnly = False

    client.placeOrder(client.next_order_id, contract, order)
    client.next_order_id += 1
    return client.next_order_id - 1
```

### Place Limit Order

```python
def place_limit_order(client, contract, quantity, limit_price, action="BUY"):
    order = Order()
    order.action = action
    order.totalQuantity = quantity
    order.orderType = "LMT"
    order.lmtPrice = limit_price
    order.eTradeOnly = False
    order.firmQuoteOnly = False

    client.placeOrder(client.next_order_id, contract, order)
    client.next_order_id += 1
    return client.next_order_id - 1
```

### Order Status Callbacks

```python
def openOrder(self, orderId, contract, order, orderState):
    print(f"Order {orderId} opened: {contract.symbol} {order.action} {order.totalQuantity}")

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
    print(f"Order {orderId}: {status_map.get(status, status)} - Filled: {filled}/{filled+remaining}")

def execDetails(self, reqId, contract, execution):
    print(f"Execution: {contract.symbol} {execution.side} {execution.shares} @ {execution.price}")
```

### Cancel Order

```python
client.cancelOrder(order_id)
```

## Positions & Portfolio

### Request Positions

```python
client.reqPositions()

def position(self, account, contract, position, avgCost):
    print(f"{account}: {contract.symbol} {position} shares @ ${avgCost}")

def positionEnd(self):
    print("Position data complete")
```

### Request Portfolio

```python
client.reqAccountUpdates(True, "")

def updatePortfolio(self, contract, position, marketPrice, marketValue, averageCost, unrealizedPNL, realizedPNL, accountName):
    print(f"{contract.symbol}: {position} @ ${marketPrice}, P&L: ${unrealizedPNL}")

def accountDownloadEnd(self, accountName):
    print("Portfolio download complete")
```

## Account Information

### Account Summary

```python
client.reqAccountSummary(0, "All", "$LEDGER")

def accountSummary(self, reqId, account, tag, value, currency):
    if tag == "NetLiquidation":
        print(f"Net Liquidation: {value} {currency}")
    elif tag == "AvailableFunds":
        print(f"Available Funds: {value} {currency}")

def accountSummaryEnd(self, reqId):
    print("Account summary complete")
```

### P&L Information

```python
client.reqPnL(account_name, "")

def pnl(self, reqId, dailyPnL, unrealizedPnL, realizedPnL):
    print(f"Daily P&L: ${dailyPnL}, Unrealized: ${unrealizedPnL}, Realized: ${realizedPnL}")
```

## Contract Discovery

### Search for Contract Details

```python
def search_contract(client, symbol):
    contract = Contract()
    contract.symbol = symbol
    contract.secType = "STK"
    contract.exchange = "SMART"
    contract.currency = "USD"

    client.reqContractDetails(1, contract)

def contractDetails(self, reqId, contractDetails):
    print(f"Contract: {contractDetails.contract.symbol}")
    print(f"Exchange: {contractDetails.contract.exchange}")
    print(f"Currency: {contractDetails.contract.currency}")
    print(f"ConId: {contractDetails.contract.conId}")  # Use conId for precise referencing
```

## Error Handling

### Common Error Codes

| Code | Description | Action |
|------|-------------|--------|
| 200 | No security definition found | Check contract details |
| 399 | Order rejected | Verify order parameters |
| 2104 | Market data farm connection is OK | Ignore (info) |
| 2106 | Market data farm connection is inactive | Ignore (info) |
| 502 | Couldn't connect to TWS | Check TWS is running |

### Pacing Limitations

- Max requests = Market Data Lines / 2 per second
- Default (100 lines) = 50 requests/sec
- If exceeding, requests are queued
- Consider FIX API for high-frequency needs

## Testing Strategy

### Paper Trading Workflow

1. Setup Paper Trading account in [Account Management](https://www.interactivebrokers.com/sso)
2. Connect to port 7497
3. Test all operations with small quantities
4. Validate order execution and fills
5. Verify P&L calculations
6. Once stable, switch to live port 7496

### Testing Checklist

- [ ] Connection establishment
- [ ] Market data subscription
- [ ] Historical data retrieval
- [ ] Order placement (MKT, LMT)
- [ ] Order modification
- [ ] Order cancellation
- [ ] Position tracking
- [ ] Account summary retrieval
- [ ] P&L calculation validation

## Scripts

### Quick Connection Test

```bash
python scripts/test_connection.py
```

### Place Order Script

```bash
python scripts/place_order.py AAPL BUY 100
```

See `scripts/` directory for executable scripts.

## References

- [TWS API Documentation](https://www.interactivebrokers.com/en/trading/tws-api.php)
- [references/contract-types.md](references/contract-types.md) - Contract definitions (STK, OPT, FUT, etc.)
- [references/order-types.md](references/order-types.md) - Order type specifications
- [references/tick-types.md](references/tick-types.md) - Market data tick types
- [references/error-codes.md](references/error-codes.md) - Error code reference

## Best Practices

1. **Always test in Paper Trading first**
2. **Handle pacing limitations** - batch requests when possible
3. **Use conId instead of symbols** for precision
4. **Implement proper error handling** - check all callback errors
5. **Monitor account P&L** in real-time
6. **Set "Never Lock Trader Workstation"** for automated sessions
7. **Use IB Gateway** for headless production environments
8. **Log all API communications** for debugging
9. **Validate order parameters** before submission
10. **Implement reconnection logic** for network resilience

## Migration from QuantConnect

Key differences from QuantConnect:

| Aspect | QuantConnect | IBKR API |
|--------|--------------|-----------|
| Execution | Cloud-based | Local TWS/Gateway |
| Latency | Higher | Lower (local) |
| Cost | Subscription | Per-trade commission |
| Market Data | Included | Separate subscriptions |
| Backtesting | Built-in | Manual (use historical data) |
| Language | C#, Python | Python, Java, C++, C# |

Advantages of IBKR direct:
- Lower latency (local execution)
- Direct market access
- Real-time order management
- Full control over trading logic
- No subscription overhead

Migration steps:
1. Port strategy logic to Python
2. Implement IBKR contract definitions
3. Replace LEAN order management with TWS API
4. Validate order routing and fills
5. Test extensively in Paper Trading
