# IBKR Order Types Reference

## Market Orders (MKT)

**Description:** Execute immediately at current market price

```python
order = Order()
order.action = "BUY"  # or "SELL"
order.totalQuantity = 100
order.orderType = "MKT"
order.eTradeOnly = False
order.firmQuoteOnly = False
```

**Use cases:**
- Fast execution needed
- Small quantity orders
- Liquid markets
- Price not critical

**Risks:**
- Slippage in fast markets
- Unfavorable fill prices
- Higher impact

## Limit Orders (LMT)

**Description:** Execute only at specified price or better

```python
order = Order()
order.action = "BUY"
order.totalQuantity = 100
order.orderType = "LMT"
order.lmtPrice = 150.00  # Limit price
order.eTradeOnly = False
order.firmQuoteOnly = False
```

**Use cases:**
- Price protection needed
- Entry/exit at specific levels
- Controlling execution price

**Risks:**
- May not fill
- Partial fills possible
- Miss opportunities

## Stop Orders (STP)

**Description:** Convert to market order when stop price triggered

```python
order = Order()
order.action = "SELL"
order.totalQuantity = 100
order.orderType = "STP"
order.auxPrice = 145.00  # Stop price
order.eTradeOnly = False
order.firmQuoteOnly = False
```

**Use cases:**
- Stop loss protection
- Exiting losing positions
- Risk management

**Risks:**
- Slippage on trigger
- Gap risk (price jumps over stop)
- Stop hunts in volatile markets

## Stop-Limit Orders (STP LMT)

**Description:** Convert to limit order when stop price triggered

```python
order = Order()
order.action = "SELL"
order.totalQuantity = 100
order.orderType = "STP LMT"
order.auxPrice = 145.00   # Stop price
order.lmtPrice = 144.90   # Limit price
order.eTradeOnly = False
order.firmQuoteOnly = False
```

**Use cases:**
- Stop loss with price protection
- Minimize slippage
- Precise exit points

**Risks:**
- May not fill after trigger
- Price may move past limit
- Complex to manage

## Market-on-Close (MOC)

**Description:** Execute at market close

```python
order = Order()
order.action = "BUY"
order.totalQuantity = 100
order.orderType = "MOC"
order.eTradeOnly = False
order.firmQuoteOnly = False
```

**Use cases:**
- End-of-day execution
- Index rebalancing
- Closing positions

**Risks:**
- Volatility at close
- Uncertain fill price
- Timing dependent

## Limit-on-Close (LOC)

**Description:** Limit order at market close

```python
order = Order()
order.action = "BUY"
order.totalQuantity = 100
order.orderType = "LOC"
order.lmtPrice = 150.00
order.eTradeOnly = False
order.firmQuoteOnly = False
```

**Use cases:**
- End-of-day price protection
- Index rebalancing with limit
- Close at specific price

**Risks:**
- May not fill
- Price protection vs execution tradeoff
- Timing dependent

## Market-on-Open (MOO)

**Description:** Execute at market open

```python
order = Order()
order.action = "BUY"
order.totalQuantity = 100
order.orderType = "MOO"
order.eTradeOnly = False
order.firmQuoteOnly = False
```

**Use cases:**
- Opening bell execution
- Gap trading
- News-driven entries

**Risks:**
- High volatility
- Uncertain fill price
- Opening gap risk

## Trailing Stop (TRAIL)

**Description:** Stop price trails market price

```python
order = Order()
order.action = "SELL"
order.totalQuantity = 100
order.orderType = "TRAIL"
order.auxPrice = 1.00  # Trail amount in points
order.trailingPercent = False  # If True, use percentage
order.eTradeOnly = False
order.firmQuoteOnly = False
```

**Use cases:**
- Lock in profits
- Dynamic stop loss
- Trend following

**Risks:**
- May trigger prematurely
- Complex to optimize
- Whipsaw risk

## Trailing Stop Limit (TRAIL LIMIT)

**Description:** Trailing stop with limit price protection

```python
order = Order()
order.action = "SELL"
order.totalQuantity = 100
order.orderType = "TRAIL LIMIT"
order.auxPrice = 1.00        # Trail amount
order.lmtPriceOffset = 0.10   # Limit offset from stop
order.eTradeOnly = False
order.firmQuoteOnly = False
```

**Use cases:**
- Profit protection with price control
- Reduced slippage
- Precise trailing exits

**Risks:**
- Complex to manage
- May not fill
- Difficult to optimize

## Volume-Weighted Average Price (VWAP)

**Description:** Execute at volume-weighted average price

```python
order = Order()
order.action = "BUY"
order.totalQuantity = 1000
order.orderType = "VWAP"
order.eTradeOnly = False
order.firmQuoteOnly = False
```

**Use cases:**
- Large orders
- Minimize market impact
- Institutional trading

**Risks:**
- Delayed execution
- Price uncertainty
- Not available for all markets

## Time-Weighted Average Price (TWAP)

**Description:** Execute evenly over time

```python
order = Order()
order.action = "BUY"
order.totalQuantity = 1000
order.orderType = "TWAP"
order.eTradeOnly = False
order.firmQuoteOnly = False
```

**Use cases:**
- Large orders
- Smooth execution
- Minimize timing risk

**Risks:**
- Delayed execution
- Price uncertainty
- Not available for all markets

## Relative (REL)

**Description:** Execute relative to market data

```python
order = Order()
order.action = "BUY"
order.totalQuantity = 100
order.orderType = "REL"
order.lmtPriceOffset = 0.10  # Offset from reference price
order.eTradeOnly = False
order.firmQuoteOnly = False
```

**Use cases:**
- Relative to VWAP
- Relative to opening price
- Relative to moving average

**Risks:**
- Complex reference logic
- Delayed execution
- Uncertain fill price

## Pegged (PEG)

**Description:** Peg to best bid/ask

```python
order = Order()
order.action = "BUY"
order.totalQuantity = 100
order.orderType = "PEG"
order.lmtPriceOffset = 0.10
order.eTradeOnly = False
order.firmQuoteOnly = False
```

**Use cases:**
- Stay at top of book
- Tight spread execution
- Price improvement

**Risks:**
- Frequent updates
- Execution uncertainty
- Not available on all exchanges

## Scale Orders

**Description:** Multiple child orders at different prices

```python
order = Order()
order.action = "BUY"
order.totalQuantity = 100
order.orderType = "SCALE"
order.scaleInitLevelSize = 25  # First order size
order.scaleSubsLevelSize = 25  # Subsequent order sizes
order.scalePriceAdjustValue = 0.50  # Price adjustment
order.scalePriceIncrement = 0.10  # Price increment
order.scaleTable = "True"  # Scale to scale
order.scaleRandomPercent = False
order.eTradeOnly = False
order.firmQuoteOnly = False
```

**Use cases:**
- Averaging into positions
- Scaling out of positions
- Entry/exit optimization

**Risks:**
- Complex management
- Partial execution risk
- Over-trading

## Algo Orders

### Arrival Price

```python
order.orderType = "ALGO"
order.algoStrategy = "ArrivalPx"
order.algoParams = []
order.eTradeOnly = False
order.firmQuoteOnly = False
```

### VWAP

```python
order.orderType = "ALGO"
order.algoStrategy = "Vwap"
order.algoParams = []
order.eTradeOnly = False
order.firmQuoteOnly = False
```

### TWAP

```python
order.orderType = "ALGO"
order.algoStrategy = "Twap"
order.algoParams = []
order.eTradeOnly = False
order.firmQuoteOnly = False
```

### POV (Percentage of Volume)

```python
order.orderType = "ALGO"
order.algoStrategy = "Pov"
order.algoParams = []
order.eTradeOnly = False
order.firmQuoteOnly = False
```

### Adaptive

```python
order.orderType = "ALGO"
order.algoStrategy = "Adaptive"
order.algoParams = []
order.eTradeOnly = False
order.firmQuoteOnly = False
```

## Conditional Orders

### One-Cancels-Other (OCO)

```python
order.orderType = "LMT"
order.lmtPrice = 150.00
order.ocaGroup = "OCO_001"  # Group identifier
order.ocaType = 1  # Cancel all with remaining
order.eTradeOnly = False
order.firmQuoteOnly = False
```

### One-Cancels-All (OCA)

```python
order.orderType = "LMT"
order.lmtPrice = 150.00
order.ocaGroup = "OCA_001"  # Group identifier
order.ocaType = 2  # Cancel all
order.eTradeOnly = False
order.firmQuoteOnly = False
```

## Order Parameters

### Time in Force (TIF)

| Value | Description |
|-------|-------------|
| `DAY` | Good for day |
| `GTC` | Good till cancelled |
| `IOC` | Immediate or cancel |
| `OPG` | At the opening |
| `CLS` | At the closing |

```python
order.tif = "DAY"  # or "GTC", "IOC", "OPG", "CLS"
```

### Order Flags

```python
order.outsideRth = False  # Allow outside regular hours
order.hidden = False  # Hide order from market
order.discretionaryAmt = 0.10  # Discretionary amount
order.allOrNone = False  # All or none
order.minQty = 1  # Minimum quantity
order.percentOffset = 0.0  # Percentage offset
order.eTradeOnly = False  # Electronic only
order.firmQuoteOnly = False  # Firm quote only
order.optOutSmartRouting = False  # Opt out of smart routing
```

## Best Practices

### Order Selection Guide

| Situation | Recommended Order Type |
|-----------|------------------------|
| Quick entry/exit | Market (MKT) |
| Price-sensitive | Limit (LMT) |
| Stop loss | Stop (STP) |
| Profit taking | Trailing Stop (TRAIL) |
| Large orders | VWAP / TWAP |
| Algorithmic | ALGO orders |
| Conditional | OCO / OCA |

### Risk Management

1. **Always use stops** - Protect against losses
2. **Set reasonable limits** - Define max position size
3. **Monitor execution** - Watch order status
4. **Test in paper** - Before live trading
5. **Review fills** - Analyze execution quality

### Execution Tips

1. **Use limit orders** for better prices
2. **Size appropriately** for liquidity
3. **Consider slippage** in fast markets
4. **Check market hours** before ordering
5. **Verify permissions** for order types

## Common Mistakes

1. **Wrong order type** - Use appropriate type for strategy
2. **Incorrect prices** - Double-check limit/stop prices
3. **Wrong quantity** - Verify position size
4. **Missing stops** - Always use risk management
5. **Poor timing** - Consider market conditions
