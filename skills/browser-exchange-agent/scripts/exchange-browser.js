#!/usr/bin/env node
/**
 * exchange-browser.js - Main browser automation script for crypto exchanges
 * 
 * Usage:
 *   node exchange-browser.js --exchange=coinbase --action=balances --headless
 *   node exchange-browser.js --exchange=kraken --action=login --headed
 *   node exchange-browser.js --exchange=binance --action=dust --screenshot
 */

const { chromium, firefox, webkit } = require('playwright');
const path = require('path');
const fs = require('fs').promises;

// Import helpers
const LoginHelper = require('./login-helper');
const BalanceScraper = require('./balance-scraper');
const ScreenshotUtil = require('./screenshot');

// Exchange configurations
const EXCHANGE_CONFIGS = {
  coinbase: {
    name: 'Coinbase',
    baseUrl: 'https://www.coinbase.com',
    loginUrl: 'https://www.coinbase.com/signin',
    balancesUrl: 'https://www.coinbase.com/accounts',
    requires2FA: true,
    hasDustSweeping: true,
  },
  kraken: {
    name: 'Kraken',
    baseUrl: 'https://www.kraken.com',
    loginUrl: 'https://www.kraken.com/sign-in',
    balancesUrl: 'https://www.kraken.com/u/funding/spot-balances',
    requires2FA: true,
    hasDustSweeping: false,
  },
  binance: {
    name: 'Binance',
    baseUrl: 'https://www.binance.com',
    loginUrl: 'https://www.binance.com/en/login',
    balancesUrl: 'https://www.binance.com/en/my/wallet/account/spot',
    requires2FA: true,
    hasDustSweeping: true,
  },
  kucoin: {
    name: 'KuCoin',
    baseUrl: 'https://www.kucoin.com',
    loginUrl: 'https://www.kucoin.com/login',
    balancesUrl: 'https://www.kucoin.com/assets/coin-list',
    requires2FA: true,
    hasDustSweeping: true,
  },
  gemini: {
    name: 'Gemini',
    baseUrl: 'https://www.gemini.com',
    loginUrl: 'https://exchange.gemini.com/login',
    balancesUrl: 'https://exchange.gemini.com/balances',
    requires2FA: true,
    hasDustSweeping: false,
  }
};

class ExchangeBrowser {
  constructor(options = {}) {
    this.options = {
      exchange: options.exchange || 'coinbase',
      action: options.action || 'balances',
      headless: options.headless !== false,
      browser: options.browser || 'chromium',
      screenshot: options.screenshot || false,
      sessionId: options.sessionId || null,
      outputPath: options.outputPath || null,
      timeout: options.timeout || 60000,
      slowMo: options.slowMo || 0,
      ...options
    };
    
    this.browser = null;
    this.context = null;
    this.page = null;
    this.sessionPath = null;
    this.loginHelper = null;
    this.balanceScraper = null;
    this.screenshotUtil = null;
  }

  /**
   * Initialize browser and context
   */
  async initialize() {
    console.log(`[ExchangeBrowser] Initializing ${this.options.browser} browser...`);
    
    const browserType = this.getBrowserType();
    
    // Launch browser with anti-detection settings
    this.browser = await browserType.launch({
      headless: this.options.headless,
      slowMo: this.options.slowMo,
      args: [
        '--disable-blink-features=AutomationControlled',
        '--disable-web-security',
        '--disable-features=IsolateOrigins,site-per-process',
        '--disable-site-isolation-trials'
      ]
    });

    // Setup session storage path
    this.sessionPath = path.join(
      process.cwd(), 
      'sessions', 
      `${this.options.exchange}_${this.options.sessionId || 'default'}`
    );

    // Create context with persistent storage
    const contextOptions = {
      viewport: { width: 1920, height: 1080 },
      userAgent: this.getRandomUserAgent(),
      locale: 'en-US',
      timezoneId: 'America/New_York',
      permissions: ['notifications'],
      ...await this.loadSessionState()
    };

    this.context = await this.browser.newContext(contextOptions);

    // Add anti-detection scripts
    await this.context.addInitScript(() => {
      // Override navigator.webdriver
      Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
      });
      
      // Override permissions
      const originalQuery = window.navigator.permissions.query;
      window.navigator.permissions.query = (parameters) => (
        parameters.name === 'notifications' 
          ? Promise.resolve({ state: Notification.permission })
          : originalQuery(parameters)
      );
    });

    this.page = await this.context.newPage();
    
    // Set default timeout
    this.page.setDefaultTimeout(this.options.timeout);
    this.page.setDefaultNavigationTimeout(this.options.timeout);

    // Initialize helpers
    this.loginHelper = new LoginHelper(this.page, this.getExchangeConfig());
    this.balanceScraper = new BalanceScraper(this.page, this.getExchangeConfig());
    this.screenshotUtil = new ScreenshotUtil(this.page);

    console.log('[ExchangeBrowser] Browser initialized successfully');
  }

  /**
   * Get browser type based on option
   */
  getBrowserType() {
    switch (this.options.browser) {
      case 'firefox': return firefox;
      case 'webkit': return webkit;
      default: return chromium;
    }
  }

  /**
   * Get exchange configuration
   */
  getExchangeConfig() {
    const config = EXCHANGE_CONFIGS[this.options.exchange];
    if (!config) {
      throw new Error(`Unknown exchange: ${this.options.exchange}`);
    }
    return config;
  }

  /**
   * Get random user agent to avoid detection
   */
  getRandomUserAgent() {
    const userAgents = [
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15'
    ];
    return userAgents[Math.floor(Math.random() * userAgents.length)];
  }

  /**
   * Load session state if exists
   */
  async loadSessionState() {
    try {
      const storageState = await fs.readFile(`${this.sessionPath}.json`, 'utf8');
      console.log('[ExchangeBrowser] Loaded existing session');
      return { storageState: JSON.parse(storageState) };
    } catch {
      return {};
    }
  }

  /**
   * Save session state
   */
  async saveSessionState() {
    try {
      await fs.mkdir(path.dirname(this.sessionPath), { recursive: true });
      const storageState = await this.context.storageState();
      await fs.writeFile(`${this.sessionPath}.json`, JSON.stringify(storageState, null, 2));
      console.log('[ExchangeBrowser] Session saved');
    } catch (error) {
      console.error('[ExchangeBrowser] Failed to save session:', error.message);
    }
  }

  /**
   * Execute the requested action
   */
  async execute() {
    try {
      console.log(`[ExchangeBrowser] Executing action: ${this.options.action}`);

      switch (this.options.action) {
        case 'login':
          return await this.performLogin();
        case 'balances':
          return await this.extractBalances();
        case 'dust':
          return await this.extractDustPositions();
        case 'screenshot':
          return await this.takeScreenshot();
        default:
          throw new Error(`Unknown action: ${this.options.action}`);
      }
    } catch (error) {
      console.error('[ExchangeBrowser] Execution error:', error.message);
      
      // Capture error screenshot
      if (this.screenshotUtil) {
        await this.screenshotUtil.capture('error', { fullPage: true });
      }
      
      throw error;
    }
  }

  /**
   * Perform login flow
   */
  async performLogin() {
    console.log('[ExchangeBrowser] Starting login flow...');
    
    const result = await this.loginHelper.login({
      username: process.env.EXCHANGE_USERNAME,
      password: process.env.EXCHANGE_PASSWORD,
      twoFactorSecret: process.env.EXCHANGE_2FA_SECRET
    });

    if (result.success) {
      await this.saveSessionState();
      
      if (this.options.screenshot) {
        await this.screenshotUtil.capture('login-success', { fullPage: true });
      }
    }

    return result;
  }

  /**
   * Extract all balances
   */
  async extractBalances() {
    console.log('[ExchangeBrowser] Extracting balances...');
    
    // Ensure logged in
    await this.ensureAuthenticated();
    
    const balances = await this.balanceScraper.extractAllBalances();
    
    if (this.options.screenshot) {
      await this.screenshotUtil.capture('balances', { fullPage: true });
    }

    if (this.options.outputPath) {
      await fs.writeFile(
        this.options.outputPath, 
        JSON.stringify(balances, null, 2)
      );
    }

    return balances;
  }

  /**
   * Extract dust positions only
   */
  async extractDustPositions() {
    console.log('[ExchangeBrowser] Extracting dust positions...');
    
    // Ensure logged in
    await this.ensureAuthenticated();
    
    const dustPositions = await this.balanceScraper.extractDustPositions();
    
    if (this.options.screenshot) {
      await this.screenshotUtil.capture('dust-positions', { fullPage: true });
    }

    if (this.options.outputPath) {
      await fs.writeFile(
        this.options.outputPath, 
        JSON.stringify(dustPositions, null, 2)
      );
    }

    return dustPositions;
  }

  /**
   * Take verification screenshot
   */
  async takeScreenshot() {
    console.log('[ExchangeBrowser] Taking screenshot...');
    
    await this.ensureAuthenticated();
    
    const screenshot = await this.screenshotUtil.capture('verification', {
      fullPage: true,
      outputPath: this.options.outputPath
    });

    return { screenshotPath: screenshot };
  }

  /**
   * Ensure user is authenticated
   */
  async ensureAuthenticated() {
    const config = this.getExchangeConfig();
    
    // Navigate to balances page
    await this.page.goto(config.balancesUrl, { waitUntil: 'networkidle' });
    
    // Check if redirected to login
    if (this.page.url().includes('login') || this.page.url().includes('signin')) {
      console.log('[ExchangeBrowser] Not authenticated, performing login...');
      await this.performLogin();
    } else {
      console.log('[ExchangeBrowser] Already authenticated');
    }
  }

  /**
   * Cleanup resources
   */
  async cleanup() {
    console.log('[ExchangeBrowser] Cleaning up...');
    
    if (this.context) {
      await this.context.close();
    }
    
    if (this.browser) {
      await this.browser.close();
    }
  }
}

// CLI handling
async function main() {
  const args = process.argv.slice(2);
  const options = parseArgs(args);

  const browser = new ExchangeBrowser(options);

  try {
    await browser.initialize();
    const result = await browser.execute();
    
    console.log('\n[Result]', JSON.stringify(result, null, 2));
    process.exit(0);
  } catch (error) {
    console.error('\n[Error]', error.message);
    process.exit(1);
  } finally {
    await browser.cleanup();
  }
}

function parseArgs(args) {
  const options = {};
  
  for (const arg of args) {
    if (arg.startsWith('--')) {
      const [key, value] = arg.slice(2).split('=');
      
      if (value === undefined) {
        options[key] = true;
      } else if (value === 'true') {
        options[key] = true;
      } else if (value === 'false') {
        options[key] = false;
      } else if (!isNaN(value)) {
        options[key] = Number(value);
      } else {
        options[key] = value;
      }
    }
  }
  
  return options;
}

// Run if called directly
if (require.main === module) {
  main();
}

module.exports = ExchangeBrowser;
