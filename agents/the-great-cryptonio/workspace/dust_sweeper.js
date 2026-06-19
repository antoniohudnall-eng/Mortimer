#!/usr/bin/env node
/**
 * Cryptonio Phase 1: Dust Consolidation Engine
 * Auto-converts dust balances (<$5) to USDC
 * Runs every 6 hours via cron
 */

const axios = require('axios');
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

// Account credentials
const ACCOUNTS = [
  {
    name: 'Primary',
    key: process.env.BINANCE_US_API_KEY || 'wRTD8W5MmvFWOhggOUYwuvy0VQeahhEKjPdIMFyvzQRaCbGMhQxGN2oV37NbTBtv',
    secret: process.env.BINANCE_US_SECRET_KEY || 'c6oAdgdnPVA4huHpidKKNw5K6kQk1Wzu0q38uchgXWzgZK1nojk8KXVWpNUxQpuq'
  },
  {
    name: 'Secondary', 
    key: process.env.BINANCE_US_SECOND_API_KEY || 'ZVQQNuBDmvnT3GZ98UJ2bl0TD0nGzO7qhGSGe1X9ffAz0wGUlPka3vUFuuYHfWcO',
    secret: process.env.BINANCE_US_SECOND_SECRET || 'MurYo7M04m7Y7mYwPF8EnKsOxCTNEdnXMS28NvZcSQ6c6cP1oaPPHzOqFAvnrzf8'
  }
];

// Configuration
const CONFIG = {
  DUST_THRESHOLD_USD: 5.00,  // Assets < $5 are dust
  MIN_TRADE_USD: 2.00,       // Don't trade smaller than this
  MAX_GAS_PERCENT: 2.00,     // Maximum 2% gas cost
  TARGET_ASSET: 'USDC',      // Consolidate to USDC
  BLACKLIST: ['BTC', 'LTC', 'BCH'], // Never sell these
  DAILY_TRADE_LIMIT: 5
};

// Logging
const LOG_DIR = path.join(__dirname, '..', 'memory', 'trading');
if (!fs.existsSync(LOG_DIR)) {
  fs.mkdirSync(LOG_DIR, { recursive: true });
}

function log(message) {
  const timestamp = new Date().toISOString();
  const logLine = `[${timestamp}] ${message}\n`;
  const logFile = path.join(LOG_DIR, `${new Date().toISOString().split('T')[0]}.log`);
  fs.appendFileSync(logFile, logLine);
  console.log(logLine.trim());
}

async function getPrices() {
  try {
    const response = await axios.get('https://api.binance.us/api/v3/ticker/price');
    const prices = {};
    response.data.forEach(p => {
      prices[p.symbol] = parseFloat(p.price);
    });
    return prices;
  } catch (error) {
    log(`ERROR fetching prices: ${error.message}`);
    return null;
  }
}

async function getAccountBalances(account) {
  try {
    const timestamp = Date.now();
    const queryString = `timestamp=${timestamp}`;
    const signature = crypto.createHmac('sha256', account.secret).update(queryString).digest('hex');
    
    const response = await axios.get(
      `https://api.binance.us/api/v3/account?${queryString}&signature=${signature}`,
      { headers: { 'X-MBX-APIKEY': account.key } }
    );
    
    return response.data.balances.filter(b => {
      const total = parseFloat(b.free) + parseFloat(b.locked);
      return total > 0;
    });
  } catch (error) {
    log(`ERROR fetching balances for ${account.name}: ${error.message}`);
    return null;
  }
}

function identifyDust(balances, prices) {
  const dustAssets = [];
  
  balances.forEach(b => {
    const total = parseFloat(b.free) + parseFloat(b.locked);
    const symbol = b.asset;
    
    // Skip blacklisted assets
    if (CONFIG.BLACKLIST.includes(symbol)) return;
    
    // Skip stablecoins
    if (symbol === 'USDT' || symbol === 'USDC') return;
    
    // Calculate USD value
    const price = prices[symbol + 'USD'] || prices['USDT' + symbol];
    if (!price) return;
    
    const usdValue = total * price;
    
    if (usdValue > 0 && usdValue < CONFIG.DUST_THRESHOLD_USD && usdValue > CONFIG.MIN_TRADE_USD) {
      dustAssets.push({
        symbol,
        amount: total,
        usdValue,
        price
      });
    }
  });
  
  return dustAssets.sort((a, b) => b.usdValue - a.usdValue);
}

async function executeTrade(account, asset, amount) {
  // Check if trading pair exists
  const symbol = asset.symbol + 'USDC';
  
  log(`PROPOSED TRADE [${account.name}]: Sell ${asset.amount} ${asset.symbol} (~$${asset.usdValue.toFixed(2)}) for USDC`);
  
  // Phase 1: Simulation only - log but don't execute
  // After 7-day burn-in, uncomment below for live trading
  
  /*
  try {
    const timestamp = Date.now();
    const queryString = `symbol=${symbol}&side=SELL&type=MARKET&quantity=${amount}&timestamp=${timestamp}`;
    const signature = crypto.createHmac('sha256', account.secret).update(queryString).digest('hex');
    
    const response = await axios.post(
      `https://api.binance.us/api/v3/order?${queryString}&signature=${signature}`,
      {},
      { headers: { 'X-MBX-APIKEY': account.key } }
    );
    
    log(`EXECUTED: ${response.data.symbol} ${response.data.side} ${response.data.executedQty}`);
    return true;
  } catch (error) {
    log(`EXECUTION ERROR: ${error.message}`);
    return false;
  }
  */
 
  // Simulation mode
  log(`SIMULATION: Trade would execute here (Phase 1 - observation mode)`);
  return 'simulated';
}

async function main() {
  log('=== CRYPTONIO DUST SWEEP INITIATED ===');
  log(`Config: Dust threshold $${CONFIG.DUST_THRESHOLD_USD}, Min trade $${CONFIG.MIN_TRADE_USD}`);
  
  const prices = await getPrices();
  if (!prices) {
    log('ABORT: Could not fetch prices');
    process.exit(1);
  }
  
  let totalDustFound = 0;
  let tradesProposed = 0;
  
  for (const account of ACCOUNTS) {
    log(`\n--- Scanning ${account.name} Account ---`);
    
    const balances = await getAccountBalances(account);
    if (!balances) continue;
    
    const dustAssets = identifyDust(balances, prices);
    
    if (dustAssets.length === 0) {
      log('No dust found in this account');
      continue;
    }
    
    log(`Found ${dustAssets.length} dust assets:`);
    dustAssets.forEach(d => {
      log(`  - ${d.symbol}: ${d.amount} = $${d.usdValue.toFixed(2)}`);
      totalDustFound += d.usdValue;
    });
    
    // Execute trades (simulation mode for now)
    for (const asset of dustAssets) {
      if (tradesProposed >= CONFIG.DAILY_TRADE_LIMIT) {
        log(`Daily trade limit reached (${CONFIG.DAILY_TRADE_LIMIT})`);
        break;
      }
      
      const result = await executeTrade(account, asset, asset.amount);
      if (result) tradesProposed++;
    }
  }
  
  log(`\n=== SUMMARY ===`);
  log(`Total dust found: $${totalDustFound.toFixed(2)}`);
  log(`Trades proposed: ${tradesProposed}`);
  log(`Mode: ${process.env.LIVE_TRADING === 'true' ? 'LIVE' : 'SIMULATION'}`);
  log('=== COMPLETE ===\n');
}

// Run
main().catch(error => {
  log(`FATAL ERROR: ${error.message}`);
  process.exit(1);
});
