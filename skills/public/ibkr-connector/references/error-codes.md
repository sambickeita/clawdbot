# IBKR API Error Codes Reference

## Connection Errors (1000-1999)

| Code | Description | Action |
|------|-------------|--------|
| 100 | Max rate of messages exceeded | Slow down requests |
| 101 | Duplicate order ID | Generate new order ID |
| 102 | Duplicate order | Check if order exists |
| 103 | Can't find order with ID | Verify order ID is valid |
| 104 | Server not yet connected | Wait for connection |
| 105 | Order already closed | Order filled or cancelled |
| 106 | Unknown order | Order not found |
| 107 | Order modification failed | Check order status |
| 108 | Cancel order failed | Order already filled |
| 109 | API connection lost | Reconnect to TWS |
| 110 | No security definition found | Check contract details |
| 111 | Order placed by another user | Cannot modify/cancel |
| 112 | Market depth not available | Market data subscription required |
| 113 | No market data | Subscribe to market data |
| 114 | No such ticker | Check symbol and exchange |
| 115 | Not connected | Connect to TWS first |
| 116 | Connection reset by broker | Reconnect |
| 117 | Connection timed out | Check network connection |
| 118 | Unknown host | Verify TWS host |
| 119 | Connection refused | Verify TWS port |
| 120 | Already connected | Disconnect first |
| 121 | Server version not supported | Update TWS |
| 122 | Too many connections | Reduce number of clients |
| 123 | Order too large | Reduce order size |
| 124 | Duplicate account ID | Use unique client ID |
| 125 | Account ID changed | Reconnect with correct ID |
| 126 | No account ID | Specify account ID |
| 127 | Not authorized | Check credentials |
| 128 | Password changed | Update password |
| 129 | Invalid API key | Verify API key |
| 130 | API key expired | Renew API key |
| 131 | No order ID | Specify order ID |
| 132 | Invalid order type | Check order type |
| 133 | Invalid order quantity | Must be positive integer |
| 134 | Invalid order price | Check price value |
| 135 | Invalid limit price | Must be valid number |
| 136 | Invalid stop price | Must be valid number |
| 137 | Invalid trailing amount | Must be valid number |
| 138 | Invalid time in force | Check TIF value |
| 139 | Invalid OCA type | Check OCA setting |
| 140 | Invalid order reference | Check reference ID |
| 141 | Invalid combo order type | Check order parameters |
| 142 | Invalid combo legs | Check combo order legs |
| 143 | Invalid delta | Must be 0-1 |
| 144 | Not enough order legs | Add more legs |
| 145 | Too many order legs | Reduce number of legs |
| 146 | Invalid delta neutral order | Check order parameters |
| 147 | No account info | Account not found |
| 148 | Account not active | Activate account |
| 149 | Account closed | Use active account |
| 150 | Account locked | Contact IBKR support |
| 151 | Account suspended | Contact IBKR support |
| 152 | Account under review | Contact IBKR support |
| 153 | Account has insufficient funds | Add funds to account |
| 154 | Account has insufficient margin | Reduce position size |
| 155 | Account not authorized for trading | Enable trading permissions |
| 156 | Account not authorized for order type | Check account permissions |
| 157 | Account not authorized for market | Check market permissions |
| 158 | Account not authorized for order size | Reduce order size |
| 159 | Account has daily trade limit reached | Wait until next day |
| 160 | Account has weekly trade limit reached | Wait until next week |
| 161 | Account has monthly trade limit reached | Wait until next month |
| 162 | Account has trade value limit reached | Reduce order value |
| 163 | Account has position limit reached | Reduce position size |
| 164 | Account has margin limit reached | Reduce position size |
| 165 | Account has buying power limit reached | Reduce order size |
| 166 | Account has shorting limit reached | Reduce short position |
| 167 | Account not authorized for shorting | Enable shorting permissions |
| 168 | Account has order limit reached | Cancel old orders |
| 169 | Account has open order limit reached | Cancel old orders |
| 170 | Account has order value limit reached | Reduce order value |
| 171 | Account has order size limit reached | Reduce order size |
| 172 | Account has daily order limit reached | Wait until next day |
| 173 | Account has weekly order limit reached | Wait until next week |
| 174 | Account has monthly order limit reached | Wait until next month |
| 175 | Account has order rate limit reached | Slow down orders |
| 176 | Account has order frequency limit reached | Slow down orders |
| 177 | Account has order timing limit reached | Wait before next order |
| 178 | Account has market data limit reached | Subscribe to more data |
| 179 | Account has market data rate limit reached | Slow down requests |
| 180 | Account has market data frequency limit reached | Slow down requests |
| 181 | Account has market data timing limit reached | Wait before next request |
| 182 | Account has historical data limit reached | Wait before next request |
| 183 | Account has historical data rate limit reached | Slow down requests |
| 184 | Account has historical data frequency limit reached | Slow down requests |
| 185 | Account has historical data timing limit reached | Wait before next request |
| 186 | Account has scanner limit reached | Wait before next scan |
| 187 | Account has scanner rate limit reached | Slow down scans |
| 188 | Account has scanner frequency limit reached | Slow down scans |
| 189 | Account has scanner timing limit reached | Wait before next scan |
| 190 | Account has news limit reached | Wait before next request |
| 191 | Account has news rate limit reached | Slow down requests |
| 192 | Account has news frequency limit reached | Slow down requests |
| 193 | Account has news timing limit reached | Wait before next request |
| 194 | Account has fundamental limit reached | Wait before next request |
| 195 | Account has fundamental rate limit reached | Slow down requests |
| 196 | Account has fundamental frequency limit reached | Slow down requests |
| 197 | Account has fundamental timing limit reached | Wait before next request |
| 198 | Account has limit reached | Check specific limit |
| 199 | Account not authorized for request | Check permissions |
| 200 | No security definition found | Check contract details |

## Market Data Errors (2000-2999)

| Code | Description | Action |
|------|-------------|--------|
| 2100 | Market data farm connection is OK | Info message, ignore |
| 2101 | Market data farm connection is inactive | Info message, ignore |
| 2102 | Market data farm connection is active | Info message, ignore |
| 2103 | Market data farm connection is dead | Reconnect to TWS |
| 2104 | Market data farm connection is OK | Info message, ignore |
| 2105 | Market data farm connection is inactive | Info message, ignore |
| 2106 | Market data farm connection is OK | Info message, ignore |
| 2107 | Market data farm connection is inactive | Info message, ignore |
| 2108 | Market data farm connection is OK | Info message, ignore |
| 2109 | No market data | Subscribe to market data |
| 2110 | Market data not subscribed | Subscribe to market data |
| 2111 | Market data request not found | Request market data |
| 2112 | Market data already subscribed | Already subscribed |
| 2113 | Market data subscription failed | Check market data subscription |
| 2114 | Market data not allowed | Not authorized for this data |
| 2115 | Market data disabled | Enable market data |
| 2116 | Market data not available | Data not available for this contract |
| 2117 | Market data limit reached | Reduce number of subscriptions |
| 2118 | Market data rate limit reached | Slow down requests |
| 2119 | Market data frequency limit reached | Slow down requests |
| 2120 | Market data timing limit reached | Wait before next request |
| 2121 | Market data request limit reached | Slow down requests |
| 2122 | Market data request rate limit reached | Slow down requests |
| 2123 | Market data request frequency limit reached | Slow down requests |
| 2124 | Market data request timing limit reached | Wait before next request |
| 2125 | Market data subscription limit reached | Cancel unused subscriptions |
| 2126 | Market data subscription rate limit reached | Slow down subscriptions |
| 2127 | Market data subscription frequency limit reached | Slow down subscriptions |
| 2128 | Market data subscription timing limit reached | Wait before next subscription |
| 2129 | No market data | Subscribe to market data |
| 2130 | Market data not subscribed | Subscribe to market data |
| 2131 | Market data request not found | Request market data |
| 2132 | Market data already subscribed | Already subscribed |
| 2133 | Market data subscription failed | Check market data subscription |
| 2134 | Market data not allowed | Not authorized for this data |
| 2135 | Market data disabled | Enable market data |
| 2136 | Market data not available | Data not available for this contract |
| 2137 | Market data limit reached | Reduce number of subscriptions |
| 2138 | Market data rate limit reached | Slow down requests |
| 2139 | Market data frequency limit reached | Slow down requests |
| 2140 | Market data timing limit reached | Wait before next request |
| 2141 | Market data request limit reached | Slow down requests |
| 2142 | Market data request rate limit reached | Slow down requests |
| 2143 | Market data request frequency limit reached | Slow down requests |
| 2144 | Market data request timing limit reached | Wait before next request |
| 2145 | Market data subscription limit reached | Cancel unused subscriptions |
| 2146 | Market data subscription rate limit reached | Slow down subscriptions |
| 2147 | Market data subscription frequency limit reached | Slow down subscriptions |
| 2148 | Market data subscription timing limit reached | Wait before next subscription |
| 2158 | Secdef data farm connection is OK | Info message, ignore |

## Order Errors (3000-3999)

| Code | Description | Action |
|------|-------------|--------|
| 300 | Can't find order with ID | Verify order ID |
| 301 | Can't modify order | Order already filled/cancelled |
| 302 | Can't cancel order | Order already filled |
| 303 | Order already modified | Wait for modification confirmation |
| 304 | Can't modify after fill | Order is filled |
| 305 | Can't cancel after fill | Order is filled |
| 306 | Can't modify cancelled order | Order is cancelled |
| 307 | Can't cancel cancelled order | Order is cancelled |
| 308 | Order modification rejected | Check order parameters |
| 309 | Order cancellation rejected | Check order status |
| 310 | Order already exists | Check if duplicate |
| 311 | Order not found | Verify order ID |
| 312 | Order rejected | Check order parameters |
| 313 | Order rejected by broker | Contact broker |
| 314 | Order rejected by exchange | Contact exchange |
| 315 | Order rejected by system | Check system status |
| 316 | Order rejected by risk manager | Check risk parameters |
| 317 | Order rejected by compliance | Check compliance rules |
| 318 | Order rejected by regulator | Check regulatory rules |
| 319 | Order rejected by market | Check market rules |
| 320 | Order rejected by liquidity provider | Check LP rules |
| 321 | Order rejected by matching engine | Check order validity |
| 322 | Order rejected by validation | Check order parameters |
| 323 | Order rejected by timeout | Submit again |
| 324 | Order rejected by rate limit | Slow down orders |
| 325 | Order rejected by size limit | Reduce order size |
| 326 | Order rejected by value limit | Reduce order value |
| 327 | Order rejected by position limit | Reduce position size |
| 328 | Order rejected by margin limit | Reduce position size |
| 329 | Order rejected by buying power limit | Reduce order size |
| 330 | Order rejected by shorting limit | Reduce short position |
| 331 | Order rejected by account limit | Check account status |
| 332 | Order rejected by order limit | Cancel old orders |
| 333 | Order rejected by open order limit | Cancel old orders |
| 334 | Order rejected by order value limit | Reduce order value |
| 335 | Order rejected by order size limit | Reduce order size |
| 336 | Order rejected by daily order limit | Wait until next day |
| 337 | Order rejected by weekly order limit | Wait until next week |
| 338 | Order rejected by monthly order limit | Wait until next month |
| 339 | Order rejected by order rate limit | Slow down orders |
| 340 | Order rejected by order frequency limit | Slow down orders |
| 341 | Order rejected by order timing limit | Wait before next order |
| 342 | Order rejected by market limit | Reduce market exposure |
| 343 | Order rejected by market rate limit | Slow down orders |
| 344 | Order rejected by market frequency limit | Slow down orders |
| 345 | Order rejected by market timing limit | Wait before next order |
| 346 | Order rejected by exchange limit | Reduce exchange exposure |
| 347 | Order rejected by exchange rate limit | Slow down orders |
| 348 | Order rejected by exchange frequency limit | Slow down orders |
| 349 | Order rejected by exchange timing limit | Wait before next order |
| 350 | Order rejected by currency limit | Reduce currency exposure |
| 351 | Order rejected by currency rate limit | Slow down orders |
| 352 | Order rejected by currency frequency limit | Slow down orders |
| 353 | Order rejected by currency timing limit | Wait before next order |
| 354 | Order rejected by security limit | Reduce security exposure |
| 355 | Order rejected by security rate limit | Slow down orders |
| 356 | Order rejected by security frequency limit | Slow down orders |
| 357 | Order rejected by security timing limit | Wait before next order |
| 358 | Order rejected by sector limit | Reduce sector exposure |
| 359 | Order rejected by sector rate limit | Slow down orders |
| 360 | Order rejected by sector frequency limit | Slow down orders |
| 361 | Order rejected by sector timing limit | Wait before next order |
| 362 | Order rejected by industry limit | Reduce industry exposure |
| 363 | Order rejected by industry rate limit | Slow down orders |
| 364 | Order rejected by industry frequency limit | Slow down orders |
| 365 | Order rejected by industry timing limit | Wait before next order |
| 366 | Order rejected by asset limit | Reduce asset exposure |
| 367 | Order rejected by asset rate limit | Slow down orders |
| 368 | Order rejected by asset frequency limit | Slow down orders |
| 369 | Order rejected by asset timing limit | Wait before next order |
| 370 | Order rejected by strategy limit | Reduce strategy exposure |
| 371 | Order rejected by strategy rate limit | Slow down orders |
| 372 | Order rejected by strategy frequency limit | Slow down orders |
| 373 | Order rejected by strategy timing limit | Wait before next order |
| 374 | Order rejected by algorithm limit | Reduce algorithm exposure |
| 375 | Order rejected by algorithm rate limit | Slow down orders |
| 376 | Order rejected by algorithm frequency limit | Slow down orders |
| 377 | Order rejected by algorithm timing limit | Wait before next order |
| 378 | Order rejected by trader limit | Reduce trader exposure |
| 379 | Order rejected by trader rate limit | Slow down orders |
| 380 | Order rejected by trader frequency limit | Slow down orders |
| 381 | Order rejected by trader timing limit | Wait before next order |
| 382 | Order rejected by group limit | Reduce group exposure |
| 383 | Order rejected by group rate limit | Slow down orders |
| 384 | Order rejected by group frequency limit | Slow down orders |
| 385 | Order rejected by group timing limit | Wait before next order |
| 386 | Order rejected by account type limit | Check account type |
| 387 | Order rejected by account type rate limit | Slow down orders |
| 388 | Order rejected by account type frequency limit | Slow down orders |
| 389 | Order rejected by account type timing limit | Wait before next order |
| 390 | Order rejected by account level limit | Check account level |
| 391 | Order rejected by account level rate limit | Slow down orders |
| 392 | Order rejected by account level frequency limit | Slow down orders |
| 393 | Order rejected by account level timing limit | Wait before next order |
| 394 | Order rejected by account tier limit | Check account tier |
| 395 | Order rejected by account tier rate limit | Slow down orders |
| 396 | Order rejected by account tier frequency limit | Slow down orders |
| 397 | Order rejected by account tier timing limit | Wait before next order |
| 398 | Order rejected by account category limit | Check account category |
| 399 | Order rejected by account category rate limit | Slow down orders |

## System Errors (4000-4999)

| Code | Description | Action |
|------|-------------|--------|
| 502 | Couldn't connect to TWS | Verify TWS is running |
| 504 | Not connected | Connect to TWS first |
| 505 | Duplicate client ID | Use unique client ID |
| 506 | Client ID mismatch | Verify client ID |
| 507 | Client not allowed | Check client permissions |
| 508 | Client not authorized | Check client authorization |
| 509 | Client not found | Verify client exists |
| 510 | Client limit reached | Reduce number of clients |
| 511 | Client rate limit reached | Slow down requests |
| 512 | Client frequency limit reached | Slow down requests |
| 513 | Client timing limit reached | Wait before next request |
| 514 | Server not found | Verify TWS host |
| 515 | Server not available | Check TWS status |
| 516 | Server not responding | Check TWS status |
| 517 | Server busy | Wait and retry |
| 518 | Server overloaded | Wait and retry |
| 519 | Server under maintenance | Wait for maintenance to complete |
| 520 | Server error | Contact IBKR support |
| 521 | Server timeout | Wait and retry |
| 522 | Server connection lost | Reconnect to TWS |
| 523 | Server connection reset | Reconnect to TWS |
| 524 | Server connection refused | Verify TWS port |
| 525 | Server connection timeout | Check network connection |
| 526 | Server handshake failed | Reconnect to TWS |
| 527 | Server authentication failed | Verify credentials |
| 528 | Server authorization failed | Check permissions |
| 529 | Server limit reached | Wait and retry |
| 530 | Server rate limit reached | Slow down requests |
| 531 | Server frequency limit reached | Slow down requests |
| 532 | Server timing limit reached | Wait before next request |
| 533 | Invalid request | Check request parameters |
| 534 | Invalid response | Check response format |
| 535 | Invalid message | Check message format |
| 536 | Invalid data | Check data format |
| 537 | Invalid value | Check value format |
| 538 | Invalid type | Check data type |
| 539 | Invalid format | Check data format |
| 540 | Invalid encoding | Check data encoding |
| 541 | Invalid length | Check data length |
| 542 | Invalid range | Check data range |
| 543 | Invalid size | Check data size |
| 544 | Invalid checksum | Check data integrity |
| 545 | Invalid signature | Check data signature |
| 546 | Invalid version | Check version compatibility |
| 547 | Invalid protocol | Check protocol version |
| 548 | Invalid API | Check API version |
| 549 | Invalid client | Check client version |
| 550 | Invalid server | Check server version |
| 551 | Missing request | Provide request |
| 552 | Missing response | Check response |
| 553 | Missing message | Check message |
| 554 | Missing data | Provide data |
| 555 | Missing value | Provide value |
| 556 | Missing type | Provide type |
| 557 | Missing format | Provide format |
| 558 | Missing encoding | Provide encoding |
| 559 | Missing length | Provide length |
| 560 | Missing range | Provide range |
| 561 | Missing size | Provide size |
| 562 | Missing checksum | Calculate checksum |
| 563 | Missing signature | Calculate signature |
| 564 | Missing version | Provide version |
| 565 | Missing protocol | Specify protocol |
| 566 | Missing API | Specify API |
| 567 | Missing client | Provide client info |
| 568 | Missing server | Provide server info |
| 569 | Duplicate request | Check for duplicates |
| 570 | Duplicate response | Check for duplicates |
| 571 | Duplicate message | Check for duplicates |
| 572 | Duplicate data | Check for duplicates |
| 573 | Duplicate value | Check for duplicates |
| 574 | Duplicate type | Check for duplicates |
| 575 | Duplicate format | Check for duplicates |
| 576 | Duplicate encoding | Check for duplicates |
| 577 | Duplicate length | Check for duplicates |
| 578 | Duplicate range | Check for duplicates |
| 579 | Duplicate size | Check for duplicates |
| 580 | Duplicate checksum | Check for duplicates |
| 581 | Duplicate signature | Check for duplicates |
| 582 | Duplicate version | Check for duplicates |
| 583 | Duplicate protocol | Check for duplicates |
| 584 | Duplicate API | Check for duplicates |
| 585 | Duplicate client | Check for duplicates |
| 586 | Duplicate server | Check for duplicates |
| 587 | Outdated request | Update request |
| 588 | Outdated response | Update response |
| 589 | Outdated message | Update message |
| 590 | Outdated data | Update data |
| 591 | Outdated value | Update value |
| 592 | Outdated type | Update type |
| 593 | Outdated format | Update format |
| 594 | Outdated encoding | Update encoding |
| 595 | Outdated length | Update length |
| 596 | Outdated range | Update range |
| 597 | Outdated size | Update size |
| 598 | Outdated checksum | Update checksum |
| 599 | Outdated signature | Update signature |

## Critical Actions

### Connection Errors (502, 504)
- **Action**: Reconnect to TWS
- **Wait**: 5-10 seconds before retry
- **Max Retries**: 3

### Order Rejection (312-399)
- **Action**: Review order parameters
- **Check**: Quantity, price, account permissions
- **Contact**: IBKR support if persistent

### Market Data Errors (2100-2158)
- **Info**: Codes 2104, 2106, 2158 can be ignored
- **Action**: Subscribe to market data if needed
- **Check**: Market data subscription status

### Rate Limits (100, 110, 324-399)
- **Action**: Slow down requests
- **Strategy**: Implement request throttling
- **Monitor**: Track request rates

## Best Practices

1. **Log all errors** - For debugging
2. **Ignore info messages** - 2104, 2106, 2158
3. **Handle connection errors** - Implement reconnection logic
4. **Validate orders** - Before submission
5. **Monitor rate limits** - Throttle requests
6. **Use unique order IDs** - Prevent duplicates
7. **Check permissions** - Before trading
8. **Test in paper** - Before live trading
