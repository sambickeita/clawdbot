# Historical Data Types for IBKR API

## WhatToShow Parameter Options

The `whatToShow` parameter specifies the type of data to retrieve when calling `reqHistoricalData()`.

### Price Data

| Value | Description | Bars Available |
|-------|-------------|-----------------|
| `TRADES` | Trades (executed transactions) | All bars |
| `MIDPOINT` | Midpoint between bid and ask | All bars |
| `BID` | Bid price | All bars |
| `ASK` | Ask price | All bars |
| `BID_ASK` | Bid and ask prices | All bars |
| `ADJUSTED_LAST` | Adjusted last price (with dividends/splits) | All bars |

### Volume Data

| Value | Description | Notes |
|-------|-------------|--------|
| `AGGTRADES` | Aggregated trades | Trade volume with count |
| `TRADES` | Individual trades | Default for price bars |

### Implied Volatility

| Value | Description | Notes |
|-------|-------------|--------|
| `OPTION_IMPLIED_VOLATILITY` | Implied volatility | Options only |
| `HISTORICAL_VOLATILITY` | Historical volatility | Calculated from price history |

### Yield Data

| Value | Description | Notes |
|-------|-------------|--------|
| `YIELD_ASK` | Ask yield | Bonds |
| `YIELD_BID` | Bid yield | Bonds |
| `YIELD_BID_ASK` | Bid and ask yields | Bonds |
| `YIELD_LAST` | Last yield | Bonds |

### Fixed Income

| Value | Description | Notes |
|-------|-------------|--------|
| `FEE_RATE` | Fee rate | Bonds |

### Schedule

| Value | Description | Notes |
|-------|-------------|--------|
| `SCHEDULE` | Trading schedule | Market hours |

## Duration Parameter

Format: `X <UNIT>` where `X` is a number and `<UNIT>` is:

| Unit | Description | Example |
|------|-------------|---------|
| `S` | Seconds | `300 S` (5 minutes) |
| `D` | Days | `1 D` (1 day) |
| `W` | Weeks | `2 W` (2 weeks) |
| `M` | Months | `1 M` (1 month) |
| `Y` | Years | `1 Y` (1 year) |

## Bar Size Parameter

Supported sizes:

| Value | Description |
|-------|-------------|
| `1 secs` | 1 second |
| `5 secs` | 5 seconds |
| `10 secs` | 10 seconds |
| `15 secs` | 15 seconds |
| `30 secs` | 30 seconds |
| `1 min` | 1 minute |
| `2 mins` | 2 minutes |
| `3 mins` | 3 minutes |
| `5 mins` | 5 minutes |
| `10 mins` | 10 minutes |
| `15 mins` | 15 minutes |
| `20 mins` | 20 minutes |
| `30 mins` | 30 minutes |
| `1 hour` | 1 hour |
| `2 hours` | 2 hours |
| `3 hours` | 3 hours |
| `4 hours` | 4 hours |
| `8 hours` | 8 hours |
| `1 day` | 1 day |
| `1 week` | 1 week |
| `1 month` | 1 month |

## Example Requests

### Daily OHLCV Data

```python
# Last 30 days of daily bars
client.reqHistoricalData(
    1,
    contract,
    "",
    "30 D",
    "1 day",
    "TRADES",
    1,  # useRTH
    1,  # formatDate
    False,
    []
)
```

### Intraday 5-Minute Bars

```python
# Last 5 days of 5-minute bars
client.reqHistoricalData(
    1,
    contract,
    "",
    "5 D",
    "5 mins",
    "MIDPOINT",
    1,
    1,
    False,
    []
)
```

### Historical Volatility

```python
# 1 year of historical volatility
client.reqHistoricalData(
    1,
    contract,
    "",
    "1 Y",
    "1 day",
    "HISTORICAL_VOLATILITY",
    1,
    1,
    False,
    []
)
```

## Limitations

- Max 1000 bars per request
- For more data, use multiple requests with different end times
- Historical data depends on your market data subscriptions
- Some data types may not be available for all contracts

## Regular Trading Hours (RTH)

| Value | Description |
|-------|-------------|
| `1` | Only regular trading hours data |
| `0` | Include extended hours data |

## Date Format

| Value | Description |
|-------|-------------|
| `1` | Dates formatted as YYYYMMDD HH:mm:ss |
| `2` | Dates as Unix timestamp (seconds since epoch) |

## Best Practices

1. **Start small** - Test with small duration first
2. **Check availability** - Verify data is available for your contract
3. **Handle pacing** - Don't request too frequently
4. **Use whatToShow wisely** - Different types for different use cases
5. **RTH for equities** - Use RTH=1 for regular hours data
