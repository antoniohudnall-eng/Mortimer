#!/usr/bin/env node
/**
 * Dust Analyzer
 * 
 * Analyze account balances for dust positions with detailed reporting.
 * 
 * Usage:
 *   node dust-analyzer.js [options]
 * 
 * Options:
 *   --thresholds <file>   Load thresholds from JSON file
 *   --min-value <usd>     Minimum USD value to consider (default: 1.0)
 *   --output <format>     Output format: json, table (default: table)
 *   --include-zero        Include zero balances in output
 *   --help                Show help message
 */

const fs = require('fs');
const path = require('path');

// Import the Binance API client
const binanceApi = require('./binance-api');

// Parse command line arguments
function parseArgs() {
  const args = process.argv.slice(2);
  const options = {
    thresholdsFile: null,
    minValue: 1.0,
    output: 'table',
    includeZero: false
  };

  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case '--thresholds':
        options.thresholdsFile = args[++i];
        break;
      case '--min-value':
        options.minValue = parseFloat(args[++i]);
        break;
      case '--output':
        options.output = args[++i];
        break;
      case '--include-zero':
        options.includeZero = true;
        break;
      case '--help':
        showHelp();
        process.exit(0);
        break;
      default:
        console.error(`Unknown option: ${args[i]}`);
        showHelp();
        process.exit(1);
    }
  }

  return options;
}

function showHelp() {
  console.log(`
Dust Analyzer - Analyze crypto balances for dust positions

Usage: node dust-analyzer.js [options]

Options:
  --thresholds <file>   Load thresholds from JSON file
  --min-value <usd>     Minimum USD value to consider (default: 1.0)
  --output <format>     Output format: json, table (default: table)
  --include-zero        Include zero balances in output
  --help                Show this help message

Environment Variables:
  BINANCE_API_KEY       Your Binance API key
  BINANCE_API_SECRET    Your Binance API secret
  BINANCE_BASE_URL      Binance API base URL (optional)

Examples:
  node dust-analyzer.js
  node dust-analyzer.js --output json
  node dust-analyzer.js --thresholds ./custom-thresholds.json
  node dust-analyzer.js --min-value 5.0 --output table
`);
}

/**
 * Load thresholds from file
 */
function loadThresholds(filePath) {
  try {
    const fullPath = path.resolve(filePath);
    const content = fs.readFileSync(fullPath, 'utf8');
    return JSON.parse(content);
  } catch (error) {
    console.error(`Error loading thresholds file: ${error.message}`);
    process.exit(1);
  }
}

/**
 * Format number with appropriate decimals
 */
function formatNumber(num, decimals = 8) {
  return parseFloat(num).toFixed(decimals).replace(/\.?0+$/, '');
}

/**
 * Format currency
 */
function formatCurrency(num) {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(num);
}

/**
 * Print table output
 */
function printTable(data, options) {
  // Filter data
  let filtered = data;
  
  if (!options.includeZero) {
    filtered = filtered.filter(item => item.total > 0);
  }

  if (filtered.length === 0) {
    console.log('\nNo balances found.\n');
    return;
  }

  // Calculate column widths
  const assetWidth = Math.max(6, ...filtered.map(d => d.asset.length));
  const totalWidth = 18;
  const freeWidth = 18;
  const lockedWidth = 18;
  const thresholdWidth = 18;
  const statusWidth = 8;

  // Print header
  console.log('\n' + '═'.repeat(assetWidth + totalWidth + freeWidth + lockedWidth + thresholdWidth + statusWidth + 20));
  console.log(
    ' '.repeat(4) +
    'Asset'.padEnd(assetWidth) + ' │ ' +
    'Total'.padStart(totalWidth) + ' │ ' +
    'Free'.padStart(freeWidth) + ' │ ' +
    'Locked'.padStart(lockedWidth) + ' │ ' +
    'Threshold'.padStart(thresholdWidth) + ' │ ' +
    'Status'.padEnd(statusWidth)
  );
  console.log('─'.repeat(assetWidth + totalWidth + freeWidth + lockedWidth + thresholdWidth + statusWidth + 20));

  // Print rows
  let dustCount = 0;
  let totalDustValue = 0;

  filtered.forEach(item => {
    const isDust = item.isDust;
    const status = isDust ? 'DUST ⚠' : 'OK ✓';
    const statusColor = isDust ? '\x1b[33m' : '\x1b[32m';
    const resetColor = '\x1b[0m';

    if (isDust) {
      dustCount++;
      totalDustValue += item.total;
    }

    console.log(
      statusColor +
      ' '.repeat(4) +
      item.asset.padEnd(assetWidth) + ' │ ' +
      formatNumber(item.total).padStart(totalWidth) + ' │ ' +
      formatNumber(item.free).padStart(freeWidth) + ' │ ' +
      formatNumber(item.locked).padStart(lockedWidth) + ' │ ' +
      formatNumber(item.threshold).padStart(thresholdWidth) + ' │ ' +
      status.padEnd(statusWidth) +
      resetColor
    );
  });

  console.log('═'.repeat(assetWidth + totalWidth + freeWidth + lockedWidth + thresholdWidth + statusWidth + 20));

  // Print summary
  console.log('\n📊 Summary:');
  console.log(`   Total assets: ${filtered.length}`);
  console.log(`   Dust positions: ${dustCount}`);
  console.log(`   Healthy positions: ${filtered.length - dustCount}`);
  
  if (dustCount > 0) {
    console.log(`\n   ⚠️  You have ${dustCount} dust position(s) that may be difficult to trade.`);
    console.log(`      Consider converting dust to BNB or consolidating positions.`);
  }
  console.log('');
}

/**
 * Print JSON output
 */
function printJson(data, options) {
  let filtered = data;
  
  if (!options.includeZero) {
    filtered = filtered.filter(item => item.total > 0);
  }

  const output = {
    timestamp: new Date().toISOString(),
    summary: {
      totalAssets: filtered.length,
      dustCount: filtered.filter(item => item.isDust).length,
      healthyCount: filtered.filter(item => !item.isDust).length
    },
    positions: filtered
  };

  console.log(JSON.stringify(output, null, 2));
}

/**
 * Main function
 */
async function main() {
  const options = parseArgs();

  // Load custom thresholds if provided
  let customThresholds = {};
  if (options.thresholdsFile) {
    customThresholds = loadThresholds(options.thresholdsFile);
    console.log(`Loaded thresholds from: ${options.thresholdsFile}`);
  }

  try {
    console.log('Fetching account balances...\n');
    
    // Get dust analysis
    const dustData = await binanceApi.identifyDust(customThresholds);

    // Output based on format
    switch (options.output) {
      case 'json':
        printJson(dustData, options);
        break;
      case 'table':
      default:
        printTable(dustData, options);
        break;
    }

  } catch (error) {
    console.error('\n❌ Error:', error.message);
    
    if (error.message.includes('BINANCE_API_KEY')) {
      console.error('\nPlease set your Binance API credentials:');
      console.error('  export BINANCE_API_KEY="your_api_key"');
      console.error('  export BINANCE_API_SECRET="your_api_secret"');
    }
    
    process.exit(1);
  }
}

// Run if called directly
if (require.main === module) {
  main();
}

// Export for use as module
module.exports = {
  parseArgs,
  loadThresholds,
  formatNumber,
  formatCurrency
};
