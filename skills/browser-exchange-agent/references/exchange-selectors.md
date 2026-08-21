# Exchange CSS Selectors Reference

This document contains CSS selectors for major cryptocurrency exchanges. Selectors are organized by exchange and function.

## Table of Contents

- [Coinbase](#coinbase)
- [Kraken](#kraken)
- [Binance](#binance)
- [KuCoin](#kucoin)
- [Gemini](#gemini)

---

## Coinbase

### Login Page

| Element | Selector | Notes |
|---------|----------|-------|
| Email Input | `input[name="email"]` `input[type="email"]` `#email` | Primary identifier |
| Password Input | `input[name="password"]` `input[type="password"]` `#password` | |
| Submit Button | `button[type="submit"]` `[data-testid="submit-button"]` | |
| 2FA Input | `input[name="code"]` `input[name="totp"]` `input[type="tel"]` | |
| 2FA Submit | `button[type="submit"]` `[data-testid="verify-button"]` | |
| Error Message | `[data-testid="error-message"]` `.error-message` `[role="alert"]` | |
| Remember Me | `input[name="remember_me"]` | |

### Balances Page

| Element | Selector | Notes |
|---------|----------|-------|
| Asset Row | `[data-testid="asset-row"]` `.asset-row` `[class*="AssetRow"]` | Container for each asset |
| Asset Name | `[data-testid="asset-name"]` `.asset-name` | Full name (e.g., "Bitcoin") |
| Asset Symbol | `[data-testid="asset-symbol"]` `.asset-symbol` | Ticker (e.g., "BTC") |
| Balance Amount | `[data-testid="balance-amount"]` `.balance-amount` | Crypto amount |
| Balance Value | `[data-testid="balance-value"]` `.balance-value` | USD value |
| Loading State | `[data-testid="loading"]` `.loading` | |

### Navigation

| Element | Selector | Notes |
|---------|----------|-------|
| Accounts Link | `a[href="/accounts"]` `[data-testid="nav-accounts"]` | |
| Portfolio Link | `a[href="/portfolio"]` `[data-testid="nav-portfolio"]` | |
| Trade Link | `a[href="/trade"]` `[data-testid="nav-trade"]` | |
| User Menu | `[data-testid="user-menu"]` `.user-menu` | |
| Logout | `button:has-text("Sign out")` `a[href*="logout"]` | |

---

## Kraken

### Login Page

| Element | Selector | Notes |
|---------|----------|-------|
| Username/Email | `input[name="username"]` `input[name="email"]` `#username` | |
| Password | `input[name="password"]` `input[type="password"]` `#password` | |
| Submit Button | `button[type="submit"]` `.sign-in-button` | |
| 2FA Input | `input[name="otp"]` `input[name="totp"]` `#otp` | |
| Error Message | `.error` `.alert` `.notification-error` | |
| Remember Me | `input[name="remember"]` | |

### Balances Page

| Element | Selector | Notes |
|---------|----------|-------|
| Balance Row | `tr[data-row]` `.balance-row` `table tbody tr` | |
| Asset Name | `.asset-name` `td:first-child` `[data-field="asset"]` | |
| Asset Symbol | `.asset-symbol` `.currency-code` | |
| Balance Amount | `.balance-amount` `td:nth-child(2)` `[data-field="balance"]` | |
| Balance Value | `.balance-value` `td:nth-child(4)` `[data-field="value"]` | |
| Loading | `.loading` `.spinner` | |

### Funding Navigation

| Element | Selector | Notes |
|---------|----------|-------|
| Spot Balances | `a[href*="funding/spot-balances"]` | |
| Funding Link | `a[href*="/u/funding"]` | |
| Staking | `a[href*="staking"]` | |

---

## Binance

### Login Page

| Element | Selector | Notes |
|---------|----------|-------|
| Email Input | `input[name="email"]` `input[id="email"]` `input[data-testid="email-input"]` | |
| Password Input | `input[name="password"]` `input[id="password"]` | |
| Submit Button | `button[type="submit"]` `.login-btn` `#click_login_submit` | |
| 2FA Input | `input[name="code"]` `input[id="code"]` `input[placeholder*="2FA"]` | |
| CAPTCHA | `iframe[id*="captcha"]` `.geetest_canvas_slice` `#clickCaptcha` | Multiple types |
| Error Message | `.error-msg` `.toast-error` `[data-testid="error"]` | |
| Remember Me | `input[name="remember"]` `.remember-checkbox` | |

### Wallet/Balances Page

| Element | Selector | Notes |
|---------|----------|-------|
| Balance Row | `.css-1c82c04` `[data-testid="spot-balances-row"]` `.bn-table-row` | |
| Asset Name | `.coin-name` `[data-testid="asset-name"]` `.asset` | |
| Asset Symbol | `.coin-symbol` `[data-testid="asset-symbol"]` | |
| Available | `.available-balance` `[data-testid="available-balance"]` | |
| In Order | `.in-order` `td:nth-child(4)` | |
| BTC Value | `.btc-value` `[data-testid="btc-value"]` `td:nth-child(5)` | |
| Action Menu | `.action-menu` `td:last-child` | |

### Dust Conversion

| Element | Selector | Notes |
|---------|----------|-------|
| Dust Page | `https://www.binance.com/en/my/wallet/account/dust` | URL |
| Convert Button | `button:has-text("Convert")` `.convert-dust-btn` | |
| Select All | `input[type="checkbox"]` `.select-all` | |
| Confirm | `button:has-text("Confirm")` `.confirm-btn` | |

### Navigation

| Element | Selector | Notes |
|---------|----------|-------|
| Wallet Menu | `.wallet-menu` `[data-testid="wallet-menu"]` | |
| Spot Wallet | `a[href*="wallet/account/spot"]` | |
| Funding Wallet | `a[href*="wallet/account/funding"]` | |
| Earn | `a[href*="earn"]` | |

---

## KuCoin

### Login Page

| Element | Selector | Notes |
|---------|----------|-------|
| Email/Phone | `input[name="email"]` `input[name="loginName"]` `input[type="email"]` | |
| Password | `input[name="password"]` `input[type="password"]` | |
| Submit Button | `button[type="submit"]` `.login-btn` `button.login` | |
| 2FA Input | `input[name="code"]` `input[name="otp"]` `input[placeholder*="2FA"]` | |
| CAPTCHA | `iframe[src*="captcha"]` `.geetest-wrap` | Geetest |
| Error | `.error-tip` `.error-message` `.ant-message-error` | |
| Remember | `input[name="remember"]` | |

### Assets/Balances Page

| Element | Selector | Notes |
|---------|----------|-------|
| Coin List Item | `.coin-list-item` `.balance-item` `tr[data-coin]` | |
| Coin Name | `.coin-name` `.currency-name` `td:nth-child(1) .name` | |
| Coin Symbol | `.coin-symbol` `.currency` `td:nth-child(1) .symbol` | |
| Balance | `.balance` `.available` `td:nth-child(3)` | |
| Frozen | `.frozen` `td:nth-child(4)` | |
| BTC Value | `.btc-value` `.estimated-value` `td:nth-child(5)` | |
| Actions | `.actions` `td:last-child` | |

### Dust Collection

| Element | Selector | Notes |
|---------|----------|-------|
| Dust Page | `https://www.kucoin.com/assets/dust` | URL |
| Collect Button | `button:has-text("Collect")` `.collect-btn` | |
| Select Assets | `.asset-checkbox` `input[type="checkbox"]` | |

---

## Gemini

### Login Page

| Element | Selector | Notes |
|---------|----------|-------|
| Email | `input[name="email"]` `input[type="email"]` `#email` | |
| Password | `input[name="password"]` `input[type="password"]` `#password` | |
| Submit | `button[type="submit"]` `input[type="submit"]` | |
| 2FA Input | `input[name="code"]` `input[name="twoFactorCode"]` `input[placeholder*="code"]` | |
| Error | `.error` `.alert-danger` `[role="alert"]` | |
| Remember Device | `input[name="rememberDevice"]` | |

### Balances Page

| Element | Selector | Notes |
|---------|----------|-------|
| Balance Row | `.balance-row` `[data-testid="balance-row"]` `tr` | |
| Currency Name | `.currency-name` `td:first-child` | |
| Currency Code | `.currency-code` `.symbol` | |
| Available | `.available-balance` `td:nth-child(2)` | |
| USD Value | `.usd-value` `td:nth-child(4)` | |

---

## Common Selectors

### Form Elements

| Purpose | Common Selectors |
|---------|------------------|
| Text Input | `input[type="text"]` `input:not([type])` |
| Email Input | `input[type="email"]` `input[name*="email"]` `input[name*="user"]` |
| Password Input | `input[type="password"]` `input[name*="pass"]` |
| Submit Button | `button[type="submit"]` `input[type="submit"]` |
| Checkbox | `input[type="checkbox"]` |
| Dropdown | `select` `[role="listbox"]` |

### Status Indicators

| Purpose | Common Selectors |
|---------|------------------|
| Loading | `.loading` `.spinner` `[class*="Loading"]` `.skeleton` |
| Error | `.error` `[class*="Error"]` `[role="alert"]` `.alert-danger` |
| Success | `.success` `[class*="Success"]` `.alert-success` |
| Disabled | `[disabled]` `.disabled` `[aria-disabled="true"]` |

### Navigation

| Purpose | Common Selectors |
|---------|------------------|
| Logout | `a[href*="logout"]` `button:has-text("Log out")` `button:has-text("Sign out")` |
| User Menu | `.user-menu` `[data-testid="user-menu"]` `.account-menu` |
| Settings | `a[href*="settings"]` `a[href*="preferences"]` |

---

## Tips for Selector Selection

1. **Prefer data-testid attributes** - These are most stable
2. **Use partial class matching** - `[class*="AssetRow"]` handles dynamic class names
3. **Have fallbacks** - Try multiple selectors in order
4. **Avoid generated classes** - Classes with hashes like `.css-1a2b3c` change frequently
5. **Test selectors** - Use browser DevTools to verify selectors work

## Anti-Detection Notes

Some exchanges randomize selectors or use obfuscation:
- Binance: Uses CSS-in-JS with generated class names
- KuCoin: Uses Ant Design components with dynamic classes
- Coinbase: Has stable data-testid attributes

When selectors fail, consider:
1. XPath expressions for text-based selection
2. Visual selectors (Playwright's getByRole, getByText)
3. Relative positioning (parent/child relationships)
