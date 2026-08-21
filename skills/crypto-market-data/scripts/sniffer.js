#!/usr/bin/env node
/**
 * SNIFFER — Market Pulse Analyst
 *
 * Follows the money. Pulls top movers + trending coins, detects the signal, and emits
 * a pulse report for the marketing team (VELUM/SCRIBBLE) and leads for the investors
 * (ALPHA-9/Cryptonio).
 *
 * The Sniffer detects; it does not recommend. Every signal cites a number.
 *
 * Usage:
 *   node sniffer.js                 # full pulse report
 *   node sniffer.js --top 20        # how many top coins to scan
 *   node sniffer.js --json          # machine-readable output
 *   node sniffer.js --min-move 5    # only flag coins moving >= 5% (24h)
 */
const apiClient = require('./api_client');

const TOP_N = 50;          // scan this many top coins
const MIN_MOVE_PCT = 5;    // flag coins moving >= this % in 24h
const MIN_VOLUME = 1e6;    // ignore dust: only flag coins with >= $1M volume

function parseArgs(argv) {
  const args = { top: TOP_N, json: false, minMove: MIN_MOVE_PCT };
  for (const a of argv) {
    if (a.startsWith('--top=')) args.top = parseInt(a.split('=')[1], 10);
    else if (a.startsWith('--min-move=')) args.minMove = parseFloat(a.split('=')[1]);
    else if (a === '--json') args.json = true;
  }
  return args;
}

async function getTopCoins(perPage) {
  const params = {
    vs_currency: 'usd',
    per_page: String(perPage),
    page: '1',
    order: 'market_cap_desc',
  };
  return apiClient.get('/crypto/coins/markets', params);
}

async function getTrending() {
  return apiClient.get('/crypto/search/trending');
}

function detectMovers(coins, minMove) {
  // Sort by absolute 24h change, descending. Flag the biggest movers (up AND down).
  const movers = coins
    .filter((c) => c && typeof c.price_change_percentage_24h === 'number')
    .filter((c) => (c.total_volume || 0) >= MIN_VOLUME)
    .map((c) => ({
      symbol: (c.symbol || '').toUpperCase(),
      name: c.name || c.symbol,
      price: c.current_price,
      change24h: c.price_change_percentage_24h,
      volume: c.total_volume,
      marketCap: c.market_cap,
    }))
    .sort((a, b) => Math.abs(b.change24h) - Math.abs(a.change24h));

  const gainers = movers.filter((m) => m.change24h >= minMove);
  const losers = movers.filter((m) => m.change24h <= -minMove);
  return { gainers, losers, all: movers };
}

function detectTrending(trending) {
  // Trending coins are the "narrative" signal — what people are searching for.
  if (!trending || trending.error || !trending.coins) return [];
  return (trending.coins || []).slice(0, 10).map((c) => {
    const item = c.item || c;
    return {
      symbol: (item.symbol || '').toUpperCase(),
      name: item.name || item.symbol,
      marketCapRank: item.market_cap_rank,
    };
  });
}

function buildPulse(movers, trending, args) {
  const now = new Date().toISOString();
  const lines = [];
  lines.push(`🐕📡 SNIFFER — MARKET PULSE`);
  lines.push(`Generated: ${now}`);
  lines.push(`Scan: top ${args.top} coins | min move ±${args.minMove}% | min vol $1M`);
  lines.push('');

  lines.push(`## 🔥 GAINERS (24h ≥ +${args.minMove}%)`);
  if (movers.gainers.length === 0) lines.push('  (none above threshold)');
  else movers.gainers.slice(0, 10).forEach((m) => {
    lines.push(`  +${m.change24h.toFixed(1)}%  ${m.symbol}  ($${m.price?.toFixed(4) ?? '?'})  vol $${(m.volume / 1e6).toFixed(1)}M`);
  });

  lines.push('');
  lines.push(`## 🩸 LOSERS (24h ≤ -${args.minMove}%)`);
  if (movers.losers.length === 0) lines.push('  (none above threshold)');
  else movers.losers.slice(0, 10).forEach((m) => {
    lines.push(`  ${m.change24h.toFixed(1)}%  ${m.symbol}  ($${m.price?.toFixed(4) ?? '?'})  vol $${(m.volume / 1e6).toFixed(1)}M`);
  });

  lines.push('');
  lines.push('## 🧭 TRENDING (narrative signal)');
  if (trending.length === 0) lines.push('  (no trending data)');
  else trending.forEach((t) => {
    lines.push(`  ${t.symbol}  ${t.name}${t.marketCapRank ? `  (rank #${t.marketCapRank})` : ''}`);
  });

  lines.push('');
  lines.push('## 📌 LEADS (for ALPHA-9 / Cryptonio)');
  const leads = movers.gainers.slice(0, 5).map((m) => m.symbol).join(', ');
  lines.push(leads ? `  Watch: ${leads}` : '  (no leads this cycle)');
  lines.push('');
  lines.push('— The money leaves a trail. I follow it. —');

  return lines.join('\n');
}

async function main() {
  const args = parseArgs(process.argv.slice(2));

  const [coins, trending] = await Promise.all([
    getTopCoins(args.top),
    getTrending(),
  ]);

  if (coins.error) {
    console.error(`SNIFFER ERROR: ${coins.error}`);
    process.exit(1);
  }

  const movers = detectMovers(coins, args.minMove);
  const trendingList = detectTrending(trending);

  if (args.json) {
    console.log(JSON.stringify({
      generated: new Date().toISOString(),
      gainers: movers.gainers.slice(0, 10),
      losers: movers.losers.slice(0, 10),
      trending: trendingList,
      leads: movers.gainers.slice(0, 5).map((m) => m.symbol),
    }, null, 2));
  } else {
    console.log(buildPulse(movers, trendingList, args));
  }
}

main();
