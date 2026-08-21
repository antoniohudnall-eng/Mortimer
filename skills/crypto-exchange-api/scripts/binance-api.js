/**
 * Binance API Client
 * 
 * Node.js script for Binance API calls with rate limiting and error handling.
 * 
 * Usage:
 *   node binance-api.js [command] [options]
 * 
 * Commands:
 *   balances              Get account balances
 *   dust [thresholds]     Identify dust positions
 *   exchange-info         Get exchange information
 *   ticker <symbol>       Get ticker for a symbol
 */

const axios = require('axios');
const crypto = require('crypto');

const BASE_URL = process.env.BINANCE_BASE_URL || 'https://api.binance.com';
const API_KEY = process.env.BINANCE_API_KEY;
const API_SECRET = process.env.BINANCE_API_SECRET;

// Default dust thresholds (in asset units)
const DEFAULT_THRESHOLDS = {
  'BTC': 0.0001,
  'ETH': 0.001,
  'BNB': 0.01,
  'USDT': 1.0,
  'USDC': 1.0,
  'BUSD': 1.0,
  'XRP': 1.0,
  'ADA': 1.0,
  'DOGE': 10.0,
  'MATIC': 1.0,
  'SOL': 0.01,
  'DOT': 0.1,
  'AVAX': 0.01,
  'LINK': 0.1,
  'UNI': 0.1,
  'LTC': 0.01,
  'BCH': 0.001,
  'ETC': 0.01,
  'XLM': 1.0,
  'VET': 10.0,
  'FIL': 0.01,
  'TRX': 10.0,
  'EOS': 0.1,
  'XMR': 0.001,
  'ALGO': 1.0,
  'ATOM': 0.1,
  'XTZ': 0.1,
  'NEAR': 0.1,
  'FTM': 1.0,
  'MANA': 1.0,
  'SAND': 1.0,
  'AXS': 0.01,
  'THETA': 0.1,
  'EGLD': 0.001,
  'HBAR': 1.0,
  'ICP': 0.01,
  'FLOW': 0.1,
  'APE': 0.1,
  'GALA': 10.0,
  'CHZ': 1.0,
  'ENJ': 1.0,
  'BAT': 1.0,
  'COMP': 0.001,
  'SNX': 0.1,
  'YFI': 0.0001,
  'MKR': 0.0001,
  'ZEC': 0.001,
  'DASH': 0.001,
  'NEO': 0.01,
  'QTUM': 0.1,
  'IOST': 10.0,
  'ZIL': 10.0,
  'ONT': 0.1,
  'ZRX': 1.0,
  'KNC': 0.1,
  'BAND': 0.1,
  'RLC': 0.1,
  'STORJ': 0.1,
  'KAVA': 0.1,
  'WAVES': 0.01,
  'DCR': 0.001,
  'LSK': 0.1,
  'STEEM': 1.0,
  'HIVE': 0.1,
  'SC': 10.0,
  'DGB': 10.0,
  'NANO': 0.01,
  'RVN': 1.0,
  'SUSHI': 0.1,
  'CVC': 1.0,
  'OXT': 1.0,
  'REP': 0.01,
  'LRC': 1.0,
  'NMR': 0.001,
  'BAL': 0.01,
  'CRV': 0.1,
  'UMA': 0.01,
  'OCEAN': 1.0,
  'PAXG': 0.0001,
  'REN': 1.0,
  'BNT': 0.1,
  'LPT': 0.01,
  'ANT': 0.1,
  'KEEP': 1.0,
  'NU': 1.0,
  'TBTC': 0.0001,
  'MLN': 0.001
};

/**
 * Generate HMAC SHA256 signature
 */
function generateSignature(queryString) {
  if (!API_SECRET) {
    throw new Error('BINANCE_API_SECRET environment variable is required');
  }
  return crypto
    .createHmac('sha256', API_SECRET)
    .update(queryString)
    .digest('hex');
}

/**
 * Make authenticated request to Binance API
 */
async function makeRequest(endpoint, params = {}, method = 'GET', requiresAuth = false) {
  const url = `${BASE_URL}${endpoint}`;
  
  let config = {
    method,
    url,
    headers: {}
  };

  if (requiresAuth) {
    if (!API_KEY) {
      throw new Error('BINANCE_API_KEY environment variable is required for authenticated requests');
    }

    const timestamp = Date.now();
    const queryParams = new URLSearchParams({
      ...params,
      timestamp: timestamp.toString()
    });
    const queryString = queryParams.toString();
    const signature = generateSignature(queryString);
    
    config.headers['X-MBX-APIKEY'] = API_KEY;
    config.params = { ...params, timestamp, signature };
  } else {
    config.params = params;
  }

  // Retry configuration
  const maxRetries = 3;
  let lastError;

  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      const response = await axios(config);
      return response.data;
    } catch (error) {
      lastError = error;
      
      if (error.response) {
        const status = error.response.status;
        const data = error.response.data;

        // Handle specific error codes
        if (status === 429) {
          // Rate limit exceeded - retry with backoff
          const delay = Math.pow(2, attempt) * 1000;
          console.error(`Rate limit exceeded. Retrying in ${delay}ms...`);
          await sleep(delay);
          continue;
        }

        if (status === 418) {
          // IP ban
          throw new Error(`IP banned from Binance API. Retry after: ${data.retryAfter || 'unknown'}`);
        }

        if (status === 401) {
          throw new Error(`Authentication failed: ${data.msg || 'Invalid API key or secret'}`);
        }

        if (status === 400) {
          throw new Error(`Bad request: ${data.msg || 'Invalid parameters'}`);
        }

        if (status >= 500) {
          // Server error - retry
          const delay = Math.pow(2, attempt) * 1000;
          console.error(`Server error (${status}). Retrying in ${delay}ms...`);
          await sleep(delay);
          continue;
        }

        // Other client errors - don't retry
        throw new Error(`Binance API error (${status}): ${data.msg || 'Unknown error'}`);
      } else if (error.request) {
        // Network error - retry
        const delay = Math.pow(2, attempt) * 1000;
        console.error(`Network error. Retrying in ${delay}ms...`);
        await sleep(delay);
        continue;
      } else {
        throw error;
      }
    }
  }

  throw new Error(`Request failed after ${maxRetries} attempts: ${lastError.message}`);
}

/**
 * Sleep utility
 */
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * Get account balances
 */
async function getBalances() {
  const data = await makeRequest('/api/v3/account', {}, 'GET', true);
  
  // Filter out zero balances
  return data.balances.filter(b => 
    parseFloat(b.free) > 0 || parseFloat(b.locked) > 0
  );
}

/**
 * Identify dust positions
 */
async function identifyDust(customThresholds = {}) {
  const balances = await getBalances();
  const thresholds = { ...DEFAULT_THRESHOLDS, ...customThresholds };
  
  return balances.map(balance => {
    const free = parseFloat(balance.free);
    const locked = parseFloat(balance.locked);
    const total = free + locked;
    const threshold = thresholds[balance.asset] || 0.0001; // Default threshold
    const isDust = total < threshold;
    
    return {
      asset: balance.asset,
      free: balance.free,
      locked: balance.locked,
      total,
      threshold,
      isDust
    };
  });
}

/**
 * Get exchange information
 */
async function getExchangeInfo() {
  return makeRequest('/api/v3/exchangeInfo', {}, 'GET', false);
}

/**
 * Get ticker for a symbol
 */
async function getTicker(symbol) {
  return makeRequest('/api/v3/ticker/24hr', { symbol }, 'GET', false);
}

/**
 * CLI handler
 */
async function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  try {
    switch (command) {
      case 'balances':
        const balances = await getBalances();
        console.log(JSON.stringify(balances, null, 2));
        break;

      case 'dust':
        let thresholds = {};
        if (args[1]) {
          try {
            thresholds = JSON.parse(args[1]);
          } catch (e) {
            console.error('Invalid thresholds JSON:', e.message);
            process.exit(1);
          }
        }
        const dust = await identifyDust(thresholds);
        console.log(JSON.stringify(dust, null, 2));
        break;

      case 'exchange-info':
        const info = await getExchangeInfo();
        console.log(JSON.stringify(info, null, 2));
        break;

      case 'ticker':
        if (!args[1]) {
          console.error('Usage: node binance-api.js ticker <symbol>');
          process.exit(1);
        }
        const ticker = await getTicker(args[1].toUpperCase());
        console.log(JSON.stringify(ticker, null, 2));
        break;

      default:
        console.log(`
Usage: node binance-api.js [command] [options]

Commands:
  balances              Get account balances
  dust [thresholds]     Identify dust positions (optional JSON thresholds)
  exchange-info         Get exchange information
  ticker <symbol>       Get ticker for a symbol

Environment Variables:
  BINANCE_API_KEY       Your Binance API key
  BINANCE_API_SECRET    Your Binance API secret
  BINANCE_BASE_URL      Binance API base URL (default: https://api.binance.com)
        `);
        process.exit(1);
    }
  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  }
}

// Export for use as module
module.exports = {
  getBalances,
  identifyDust,
  getExchangeInfo,
  getTicker,
  DEFAULT_THRESHOLDS
};

// Run CLI if called directly
if (require.main === module) {
  main();
}
