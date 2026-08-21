# Browser Automation Patterns & Anti-Detection

This document contains common automation patterns and techniques to avoid bot detection on cryptocurrency exchanges.

## Table of Contents

- [Anti-Detection Techniques](#anti-detection-techniques)
- [Wait Strategies](#wait-strategies)
- [Session Management](#session-management)
- [Error Handling](#error-handling)
- [Retry Logic](#retry-logic)
- [Rate Limiting](#rate-limiting)

---

## Anti-Detection Techniques

### 1. Browser Fingerprint Randomization

```javascript
// Override navigator.webdriver
await context.addInitScript(() => {
  Object.defineProperty(navigator, 'webdriver', {
    get: () => undefined
  });
});

// Random user agents
const userAgents = [
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
  'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
];

const context = await browser.newContext({
  userAgent: userAgents[Math.floor(Math.random() * userAgents.length)]
});
```

### 2. Viewport and Locale Consistency

```javascript
const context = await browser.newContext({
  viewport: { width: 1920, height: 1080 },
  locale: 'en-US',
  timezoneId: 'America/New_York',
  geolocation: { latitude: 40.7128, longitude: -74.0060 },
  permissions: ['notifications']
});
```

### 3. Human-Like Mouse Movements

```javascript
// Use Playwright's built-in slowMo or implement custom delays
await page.click(selector, { delay: 100 }); // 100ms delay between mouse down/up

// Random delays between actions
const randomDelay = (min, max) => Math.floor(Math.random() * (max - min + 1) + min);
await page.waitForTimeout(randomDelay(500, 2000));
```

### 4. Page Load Behavior

```javascript
// Don't wait for all resources - be less predictable
await page.goto(url, { waitUntil: 'domcontentloaded' });

// Then wait for specific element
await page.waitForSelector('[data-testid="content-loaded"]');
```

### 5. Disable Automation Flags

```javascript
const browser = await chromium.launch({
  args: [
    '--disable-blink-features=AutomationControlled',
    '--disable-web-security',
    '--disable-features=IsolateOrigins,site-per-process'
  ]
});
```

---

## Wait Strategies

### Explicit Waits (Preferred)

```javascript
// Wait for element to be visible
await page.waitForSelector('.balance-row', { state: 'visible' });

// Wait for element to be hidden (loading complete)
await page.waitForSelector('.loading', { state: 'hidden' });

// Wait for network idle
await page.waitForLoadState('networkidle');

// Wait for specific function to return true
await page.waitForFunction(() => {
  return document.querySelectorAll('.balance-row').length > 0;
}, { timeout: 30000 });
```

### Custom Wait Helpers

```javascript
class WaitHelper {
  constructor(page) {
    this.page = page;
  }

  // Wait for loading to complete
  async waitForLoadingComplete(selector = '.loading', timeout = 30000) {
    const startTime = Date.now();
    
    while (Date.now() - startTime < timeout) {
      const isLoading = await this.page.evaluate((sel) => {
        const el = document.querySelector(sel);
        return el && el.offsetParent !== null;
      }, selector);

      if (!isLoading) return;
      await this.page.waitForTimeout(500);
    }
    
    throw new Error('Loading timeout exceeded');
  }

  // Wait for element with retry
  async waitForElement(selector, options = {}) {
    const { timeout = 10000, visible = true } = options;
    
    try {
      const element = await this.page.waitForSelector(selector, {
        timeout,
        state: visible ? 'visible' : 'attached'
      });
      return element;
    } catch (error) {
      // Try alternative selectors
      if (options.fallbacks) {
        for (const fallback of options.fallbacks) {
          try {
            return await this.page.waitForSelector(fallback, { timeout: 5000 });
          } catch {
            continue;
          }
        }
      }
      throw error;
    }
  }

  // Wait for text to appear
  async waitForText(text, timeout = 10000) {
    await this.page.waitForFunction(
      (t) => document.body.innerText.includes(t),
      text,
      { timeout }
    );
  }
}
```

---

## Session Management

### Persistent Sessions

```javascript
const SESSION_PATH = './sessions';

class SessionManager {
  constructor(exchange, sessionId = 'default') {
    this.sessionPath = `${SESSION_PATH}/${exchange}_${sessionId}.json`;
  }

  async save(context) {
    await fs.mkdir(SESSION_PATH, { recursive: true });
    const storageState = await context.storageState();
    await fs.writeFile(this.sessionPath, JSON.stringify(storageState));
  }

  async load() {
    try {
      const data = await fs.readFile(this.sessionPath, 'utf8');
      return { storageState: JSON.parse(data) };
    } catch {
      return {};
    }
  }

  async delete() {
    try {
      await fs.unlink(this.sessionPath);
    } catch {
      // File may not exist
    }
  }
}
```

### Session Validation

```javascript
async function isSessionValid(page, dashboardUrl) {
  await page.goto(dashboardUrl, { waitUntil: 'domcontentloaded' });
  
  // Check if redirected to login
  return !page.url().includes('login') && !page.url().includes('signin');
}
```

---

## Error Handling

### Structured Error Types

```javascript
class ExchangeError extends Error {
  constructor(message, type, recoverable = false) {
    super(message);
    this.name = 'ExchangeError';
    this.type = type;
    this.recoverable = recoverable;
  }
}

class LoginError extends ExchangeError {
  constructor(message, reason) {
    super(message, 'LOGIN_ERROR', false);
    this.reason = reason; // 'invalid_credentials', '2fa_required', 'captcha', 'locked'
  }
}

class NavigationError extends ExchangeError {
  constructor(message) {
    super(message, 'NAVIGATION_ERROR', true);
  }
}

class ExtractionError extends ExchangeError {
  constructor(message, selector) {
    super(message, 'EXTRACTION_ERROR', true);
    this.selector = selector;
  }
}
```

### Global Error Handler

```javascript
async function withErrorHandling(fn, options = {}) {
  const { screenshotOnError = true, retries = 0 } = options;
  
  try {
    return await fn();
  } catch (error) {
    if (screenshotOnError && page) {
      await page.screenshot({ 
        path: `error_${Date.now()}.png`,
        fullPage: true 
      });
    }
    
    // Log error details
    console.error('Automation error:', {
      message: error.message,
      url: page?.url(),
      timestamp: new Date().toISOString()
    });
    
    throw error;
  }
}
```

---

## Retry Logic

### Exponential Backoff

```javascript
async function withRetry(fn, options = {}) {
  const { 
    maxRetries = 3, 
    baseDelay = 1000,
    maxDelay = 10000,
    shouldRetry = () => true 
  } = options;

  let lastError;
  
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error;
      
      if (attempt === maxRetries || !shouldRetry(error)) {
        throw error;
      }
      
      // Exponential backoff with jitter
      const delay = Math.min(
        baseDelay * Math.pow(2, attempt) + Math.random() * 1000,
        maxDelay
      );
      
      console.log(`Retry ${attempt + 1}/${maxRetries} after ${delay}ms`);
      await new Promise(r => setTimeout(r, delay));
    }
  }
  
  throw lastError;
}
```

### Action-Specific Retries

```javascript
// Retry navigation with page reload
async function navigateWithRetry(page, url, options = {}) {
  return withRetry(
    () => page.goto(url, { waitUntil: 'networkidle', timeout: 60000 }),
    {
      maxRetries: 3,
      shouldRetry: (error) => 
        error.message.includes('net::') || 
        error.message.includes('timeout')
    }
  );
}

// Retry element interaction
async function clickWithRetry(page, selector, options = {}) {
  return withRetry(
    async () => {
      const element = await page.waitForSelector(selector, { timeout: 10000 });
      await element.click();
    },
    {
      maxRetries: 3,
      baseDelay: 500,
      shouldRetry: (error) => 
        error.message.includes('detached') ||
        error.message.includes('visible')
    }
  );
}
```

---

## Rate Limiting

### Request Throttling

```javascript
class RateLimiter {
  constructor(requestsPerSecond = 2) {
    this.minInterval = 1000 / requestsPerSecond;
    this.lastRequest = 0;
  }

  async throttle() {
    const now = Date.now();
    const elapsed = now - this.lastRequest;
    
    if (elapsed < this.minInterval) {
      await new Promise(r => setTimeout(r, this.minInterval - elapsed));
    }
    
    this.lastRequest = Date.now();
  }
}

// Usage
const limiter = new RateLimiter(1); // 1 request per second

async function makeRequest() {
  await limiter.throttle();
  // Perform action
}
```

### Exchange-Specific Rate Limits

```javascript
const RATE_LIMITS = {
  coinbase: { requests: 10, window: 1000 },    // 10 req/s
  kraken: { requests: 60, window: 60000 },     // 60 req/min
  binance: { requests: 20, window: 1000 },     // 20 req/s
  kucoin: { requests: 30, window: 1000 },      // 30 req/s
  gemini: { requests: 10, window: 1000 }       // 10 req/s
};

class ExchangeRateLimiter {
  constructor(exchange) {
    const limit = RATE_LIMITS[exchange];
    this.minInterval = limit.window / limit.requests;
    this.lastRequest = 0;
  }

  async wait() {
    const now = Date.now();
    const elapsed = now - this.lastRequest;
    
    if (elapsed < this.minInterval) {
      await new Promise(r => setTimeout(r, this.minInterval - elapsed));
    }
    
    this.lastRequest = Date.now();
  }
}
```

---

## CAPTCHA Handling

### Detection

```javascript
async function detectCaptcha(page) {
  const captchaSelectors = [
    'iframe[src*="recaptcha"]',
    'iframe[src*="hcaptcha"]',
    '.g-recaptcha',
    '.h-captcha',
    '[data-testid="captcha"]'
  ];

  for (const selector of captchaSelectors) {
    const element = await page.$(selector);
    if (element) return { detected: true, type: selector };
  }

  return { detected: false };
}
```

### Manual Intervention

```javascript
async function handleCaptchaManual(page, timeout = 120000) {
  console.log('CAPTCHA detected - waiting for manual solution...');
  
  // Wait for CAPTCHA to be solved (iframe disappears)
  await page.waitForFunction(
    () => !document.querySelector('iframe[src*="recaptcha"]'),
    { timeout }
  );
  
  console.log('CAPTCHA appears to be solved');
}
```

---

## Best Practices

1. **Always use explicit waits** - Never use fixed delays
2. **Handle session expiration** - Check auth status before actions
3. **Capture evidence** - Screenshots on errors
4. **Log everything** - Timestamps, URLs, actions
5. **Respect rate limits** - Don't get IP banned
6. **Use headless for production** - Headed only for debugging
7. **Clean up resources** - Always close browser contexts
8. **Validate data** - Check extracted data makes sense
9. **Have fallbacks** - Multiple selector strategies
10. **Monitor for changes** - Exchanges update frequently
