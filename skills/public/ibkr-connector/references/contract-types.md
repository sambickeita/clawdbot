# IBKR Contract Types Reference

## Stock (STK)

**Description:** Common stock shares

```python
contract = Contract()
contract.symbol = "AAPL"
contract.secType = "STK"
contract.exchange = "SMART"
contract.currency = "USD"
contract.primaryExchange = "ISLAND"  # Optional: for direct routing
```

**Exchanges:**
- `SMART` - Smart routing (default)
- `ISLAND` - NASDAQ
- `ARCA` - NYSE Arca
- `NYSE` - New York Stock Exchange
- `BATS` - BATS Exchange

**Example:**
```python
# Apple stock
contract = Contract()
contract.symbol = "AAPL"
contract.secType = "STK"
contract.exchange = "SMART"
contract.currency = "USD"
```

## Option (OPT)

**Description:** Call and put options

```python
contract = Contract()
contract.symbol = "AAPL"
contract.secType = "OPT"
contract.exchange = "SMART"
contract.currency = "USD"
contract.lastTradeDateOrContractMonth = "20250119"  # YYYYMMDD
contract.strike = 150.0
contract.right = "C"  # "C" for Call, "P" for Put
contract.multiplier = "100"
```

**Parameters:**
| Parameter | Description | Example |
|-----------|-------------|---------|
| `symbol` | Underlying symbol | "AAPL" |
| `secType` | Security type | "OPT" |
| `exchange` | Exchange | "SMART" |
| `currency` | Currency | "USD" |
| `lastTradeDateOrContractMonth` | Expiration date | "20250119" |
| `strike` | Strike price | 150.0 |
| `right` | Option right | "C" (Call) or "P" (Put) |
| `multiplier` | Contract multiplier | "100" |

**Example:**
```python
# Apple $150 Call expiring Jan 19, 2025
contract = Contract()
contract.symbol = "AAPL"
contract.secType = "OPT"
contract.exchange = "SMART"
contract.currency = "USD"
contract.lastTradeDateOrContractMonth = "20250119"
contract.strike = 150.0
contract.right = "C"
contract.multiplier = "100"
```

## Future (FUT)

**Description:** Futures contracts

```python
contract = Contract()
contract.symbol = "ES"
contract.secType = "FUT"
contract.exchange = "CME"
contract.currency = "USD"
contract.lastTradeDateOrContractMonth = "202503"
contract.multiplier = "50"
```

**Exchanges:**
- `CME` - Chicago Mercantile Exchange
- `CBOT` - Chicago Board of Trade
- `NYMEX` - New York Mercantile Exchange
- `COMEX` - Commodity Exchange
- `EUREX` - Eurex Exchange
- `NYBOT` - New York Board of Trade

**Example:**
```python
# E-mini S&P 500 futures (March 2025)
contract = Contract()
contract.symbol = "ES"
contract.secType = "FUT"
contract.exchange = "CME"
contract.currency = "USD"
contract.lastTradeDateOrContractMonth = "202503"
contract.multiplier = "50"
```

## Forex (CASH)

**Description:** Currency pairs

```python
contract = Contract()
contract.symbol = "EUR"
contract.secType = "CASH"
contract.exchange = "IDEALPRO"
contract.currency = "USD"
```

**Currency Pairs:**
| Symbol | Currency | Base | Quote |
|--------|----------|-------|-------|
| EUR | USD | Euro | US Dollar |
| GBP | USD | British Pound | US Dollar |
| JPY | USD | Japanese Yen | US Dollar |
| CHF | USD | Swiss Franc | US Dollar |
| CAD | USD | Canadian Dollar | US Dollar |
| AUD | USD | Australian Dollar | US Dollar |

**Example:**
```python
# EUR/USD
contract = Contract()
contract.symbol = "EUR"
contract.secType = "CASH"
contract.exchange = "IDEALPRO"
contract.currency = "USD"
```

## Index (IND)

**Description:** Stock indices

```python
contract = Contract()
contract.symbol = "SPX"
contract.secType = "IND"
contract.exchange = "CBOE"
contract.currency = "USD"
```

**Indices:**
| Symbol | Name | Exchange |
|--------|------|----------|
| SPX | S&P 500 | CBOE |
| NDX | NASDAQ 100 | NASDAQ |
| DJX | Dow Jones | CBOE |
| RUT | Russell 2000 | CBOE |
| VIX | CBOE Volatility Index | CBOE |

**Example:**
```python
# S&P 500 Index
contract = Contract()
contract.symbol = "SPX"
contract.secType = "IND"
contract.exchange = "CBOE"
contract.currency = "USD"
```

## Bond (BOND)

**Description:** Bonds and fixed income securities

```python
contract = Contract()
contract.symbol = "US912828Z40"  # CUSIP
contract.secType = "BOND"
contract.exchange = "SMART"
contract.currency = "USD"
```

**Bond Types:**
- Government bonds
- Corporate bonds
- Municipal bonds
- Treasury bonds

## Contract Details Request

```python
# Get contract details from symbol
def get_contract_details(client, symbol, secType="STK"):
    contract = Contract()
    contract.symbol = symbol
    contract.secType = secType
    contract.exchange = "SMART"
    contract.currency = "USD"

    client.reqContractDetails(1, contract)

# Handle response
def contractDetails(self, reqId, contractDetails):
    contract = contractDetails.contract
    print(f"Symbol: {contract.symbol}")
    print(f"Exchange: {contract.exchange}")
    print(f"Currency: {contract.currency}")
    print(f"ConId: {contract.conId}")  # Use conId for precise referencing
    print(f"Min Tick: {contractDetails.minTick}")
    print(f"Price Magnifier: {contractDetails.priceMagnifier}")
    print(f"Order Types: {contractDetails.orderTypes}")
    print(f"Valid Exchanges: {contractDetails.validExchanges}")
```

## Using ConId

For precise contract referencing, use `conId` instead of symbol:

```python
# Create contract by conId (most precise)
contract = Contract()
contract.conId = 265598  # AAPL conId
contract.exchange = "SMART"

# Get conId for symbol
contract = Contract()
contract.symbol = "AAPL"
contract.secType = "STK"
contract.exchange = "SMART"
client.reqContractDetails(1, contract)
# Check conId in contractDetails callback
```

## SMART Routing

SMART (Smart Routing) automatically routes orders to the best available exchange:

**Advantages:**
- Best price execution
- Automatic execution venue selection
- Improved liquidity
- Lower costs

**For Direct Routing:**
```python
contract.primaryExchange = "ISLAND"  # Route directly to NASDAQ
contract.primaryExchange = "NYSE"  # Route directly to NYSE
```

## Contract Validation

Before using a contract, always validate:

```python
def validate_contract(client, contract):
    """Validate contract before trading"""
    client.reqContractDetails(1, contract)
    time.sleep(1)  # Wait for response

    # Check if contract is valid
    if contract.validExchanges and len(contract.validExchanges) > 0:
        return True
    return False
```

## Common Contract Errors

| Error | Description | Fix |
|-------|-------------|-----|
| 200 | No security definition found | Check contract parameters |
| 354 | Can't find exchange | Verify exchange is valid |
| 200 | Invalid secType | Check security type |
| 200 | Invalid currency | Check currency code |

## Best Practices

1. **Use conId for precision** - Most reliable contract identification
2. **Validate contracts** - Before placing orders
3. **Use SMART routing** - For best execution
4. **Check market availability** - Verify market data subscription
5. **Test with reqContractDetails** - Before trading
6. **Handle contract updates** - Watch for contract changes
7. **Use appropriate secType** - Match contract type to instrument
8. **Check expiration dates** - For options and futures
9. **Verify multipliers** - For correct position sizing
10. **Review exchange rules** - Before trading specific exchanges

## Contract Discovery

### Search Contracts

```python
# Search for contract matching criteria
def search_contracts(client, symbol):
    contract = Contract()
    contract.symbol = symbol
    contract.secType = "STK"
    contract.exchange = "SMART"
    contract.currency = "USD"

    client.reqMatchingSymbols(1, contract)
```

### Option Chains

```python
# Get option chain for underlying
def get_option_chain(client, symbol, expiry):
    contract = Contract()
    contract.symbol = symbol
    contract.secType = "OPT"
    contract.exchange = "SMART"
    contract.currency = "USD"
    contract.lastTradeDateOrContractMonth = expiry

    client.reqSecDefOptParams(1, symbol, "", "STK", contract.conId)
```

### Stock Scanner

```python
# Scan for stocks matching criteria
def scan_stocks(client):
    contract = Contract()
    contract.secType = "STK"
    contract.exchange = "SMART"
    contract.currency = "USD"

    # Scan for most active stocks
    client.reqScannerSubscription(1, {
        'instrument': 'STK',
        'locationCode': 'STK.US.MAJOR',
        'scanCode': 'TOP_TRADE_RATE'
    }, [], [])
```

## Contract Parameters Reference

### All Security Types

| SecType | Description | Common Exchanges |
|---------|-------------|------------------|
| `STK` | Stock | SMART, ISLAND, NYSE |
| `OPT` | Option | SMART, CBOE, AMEX |
| `FUT` | Future | CME, CBOT, NYMEX |
| `CASH` | Forex | IDEALPRO |
| `IND` | Index | CBOE, NASDAQ |
| `BOND` | Bond | SMART |
| `FOP` | Futures Option | CME, CBOT |
| `WAR` | Warrant | SMART |
| `CFD` | Contract for Difference | SMART |

### Common Exchanges

| Code | Name | Products |
|------|------|----------|
| `SMART` | Smart Routing | All |
| `ISLAND` | NASDAQ | Stocks |
| `NYSE` | NYSE | Stocks |
| `ARCA` | NYSE Arca | Stocks, Options |
| `CBOE` | CBOE | Options |
| `CME` | CME | Futures |
| `CBOT` | CBOT | Futures |
| `IDEALPRO` | Ideal Pro | Forex |
| `TSE` | Toronto Stock Exchange | Stocks |
| `LSE` | London Stock Exchange | Stocks |

### Common Currencies

| Code | Currency |
|------|----------|
| `USD` | US Dollar |
| `EUR` | Euro |
| `GBP` | British Pound |
| `JPY` | Japanese Yen |
| `CHF` | Swiss Franc |
| `CAD` | Canadian Dollar |
| `AUD` | Australian Dollar |
| `CNY` | Chinese Yuan |
| `HKD` | Hong Kong Dollar |

## Examples by Asset Class

### Stocks

```python
# US Stocks
contract = Contract()
contract.symbol = "AAPL"
contract.secType = "STK"
contract.exchange = "SMART"
contract.currency = "USD"

# Canadian Stocks
contract = Contract()
contract.symbol = "SHOP"
contract.secType = "STK"
contract.exchange = "SMART"
contract.currency = "CAD"
```

### Options

```python
# Equity Option
contract = Contract()
contract.symbol = "AAPL"
contract.secType = "OPT"
contract.exchange = "SMART"
contract.currency = "USD"
contract.lastTradeDateOrContractMonth = "20250119"
contract.strike = 150.0
contract.right = "C"
contract.multiplier = "100"

# Index Option
contract = Contract()
contract.symbol = "SPX"
contract.secType = "OPT"
contract.exchange = "CBOE"
contract.currency = "USD"
contract.lastTradeDateOrContractMonth = "20250119"
contract.strike = 5000.0
contract.right = "P"
contract.multiplier = "100"
```

### Futures

```python
# Equity Index Futures
contract = Contract()
contract.symbol = "ES"
contract.secType = "FUT"
contract.exchange = "CME"
contract.currency = "USD"
contract.lastTradeDateOrContractMonth = "202503"
contract.multiplier = "50"

# Commodity Futures
contract = Contract()
contract.symbol = "CL"
contract.secType = "FUT"
contract.exchange = "NYMEX"
contract.currency = "USD"
contract.lastTradeDateOrContractMonth = "202503"
contract.multiplier = "1000"
```

### Forex

```python
# Major Pairs
contract = Contract()
contract.symbol = "EUR"
contract.secType = "CASH"
contract.exchange = "IDEALPRO"
contract.currency = "USD"

# Cross Pairs
contract = Contract()
contract.symbol = "EUR"
contract.secType = "CASH"
contract.exchange = "IDEALPRO"
contract.currency = "GBP"
```

## Troubleshooting

### Contract Not Found

```
Error 200: No security definition found
```

**Causes:**
- Incorrect symbol
- Wrong security type
- Invalid exchange
- Expired contract

**Solutions:**
- Verify symbol is correct
- Check security type matches instrument
- Validate exchange code
- Use conId instead of symbol
- Check contract expiration date

### Market Data Not Available

```
Error 2109: No market data for contract
```

**Causes:**
- No market data subscription
- Market closed
- Invalid contract

**Solutions:**
- Subscribe to market data
- Check market hours
- Validate contract details
- Use reqContractDetails to verify

### Exchange Not Supported

```
Error 354: Can't find exchange
```

**Causes:**
- Exchange code misspelled
- Exchange not available for instrument
- Wrong exchange for security type

**Solutions:**
- Verify exchange code spelling
- Check exchange supports security type
- Use SMART routing for default
- Review exchange documentation
