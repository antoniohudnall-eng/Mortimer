#!/usr/bin/env node
/**
 * balance-scraper.js - Extracts balance data from exchange web UIs
 */

class BalanceScraper {
  constructor(page, exchangeConfig) {
    this.page = page;
    this.config = exchangeConfig;
    this.selectors = this.getSelectors();
  }

  /**
   * Get CSS selectors for balance extraction
   */
  getSelectors() {
    const selectors = {
      coinbase: {
        balanceRows: '[data-testid="asset-row"], .asset-row, [class*="AssetRow"]',
        assetName: '[data-testid="asset-name"], .asset-name, [class*="AssetName"]',
        assetSymbol: '[data-testid="asset-symbol"], .asset-symbol, [class*="AssetSymbol"]',
        balanceAmount: '[data-testid="balance-amount"], .balance-amount, [class*="BalanceAmount"]',
        balanceValue: '[data-testid="balance-value"], .balance-value, [class*="BalanceValue"]',
        loadingIndicator: '[data-testid="loading"], .loading, [class*="Loading"]',
        dustThreshold: 0.01 // USD value below which is considered dust
      },
      kraken: {
        balanceRows: 'tr[data-row], .balance-row, table tbody tr',
        assetName: '.asset-name, td:first-child, [data-field="asset"]',
        assetSymbol: '.asset-symbol, .currency-code',
        balanceAmount: '.balance-amount, td:nth-child(2), [data-field="balance"]',
        balanceValue: '.balance-value, td:nth-child(4), [data-field="value"]',
        loadingIndicator: '.loading, .spinner, [class*="Loading"]',
        dustThreshold: 0.01
      },
      binance: {
        balanceRows: '.css-1c82c04, [data-testid="spot-balances-row"], .bn-table-row',
        assetName: '.coin-name, [data-testid="asset-name"], .asset',
        assetSymbol: '.coin-symbol, [data-testid="asset-symbol"]',
        balanceAmount: '.available-balance, [data-testid="available-balance"], td:nth-child(3)',
        balanceValue: '.btc-value, [data-testid="btc-value"], td:nth-child(5)',
        loadingIndicator: '.loading-mask, .skeleton, [class*="Loading"]',
        dustThreshold: 0.0001 // BTC value
      },
      kucoin: {
        balanceRows: '.coin-list-item, .balance-item, tr[data-coin]',
        assetName: '.coin-name, .currency-name, td:nth-child(1) .name',
        assetSymbol: '.coin-symbol, .currency, td:nth-child(1) .symbol',
        balanceAmount: '.balance, .available, td:nth-child(3)',
        balanceValue: '.btc-value, .estimated-value, td:nth-child(5)',
        loadingIndicator: '.loading, .ant-spin, [class*="loading"]',
        dustThreshold: 0.0001
      },
      gemini: {
        balanceRows: '.balance-row, [data-testid="balance-row"], tr',
        assetName: '.currency-name, td:first-child',
        assetSymbol: '.currency-code, .symbol',
        balanceAmount: '.available-balance, td:nth-child(2)',
        balanceValue: '.usd-value, td:nth-child(4)',
        loadingIndicator: '.loading, .spinner',
        dustThreshold: 0.01
      }
    };

    return selectors[this.config.name.toLowerCase()] || selectors.coinbase;
  }

  /**
   * Extract all balances from the page
   */
  async extractAllBalances() {
    console.log('[BalanceScraper] Navigating to balances page...');
    
    await this.page.goto(this.config.balancesUrl, { 
      waitUntil: 'networkidle',
      timeout: 60000 
    });

    // Wait for loading to complete
    await this.waitForLoadingComplete();

    console.log('[BalanceScraper] Extracting balance data...');

    // Extract balances using page evaluation
    const balances = await this.page.evaluate((selectors) => {
      const rows = document.querySelectorAll(selectors.balanceRows);
      const data = [];

      rows.forEach(row => {
        try {
          // Try multiple selector strategies
          const nameEl = row.querySelector(selectors.assetName) || 
                        row.querySelector('td:first-child') ||
                        row.querySelector('[class*="name"]');
          
          const symbolEl = row.querySelector(selectors.assetSymbol) ||
                          row.querySelector('[class*="symbol"]') ||
                          row.querySelector('td:first-child');
          
          const amountEl = row.querySelector(selectors.balanceAmount) ||
                          row.querySelector('[class*="balance"]') ||
                          row.querySelector('td:nth-child(2)');
          
          const valueEl = row.querySelector(selectors.balanceValue) ||
                         row.querySelector('[class*="value"]') ||
                         row.querySelector('td:nth-child(3)');

          if (nameEl && amountEl) {
            const name = nameEl.textContent?.trim() || '';
            const symbol = symbolEl?.textContent?.trim() || 
                          name.match(/\(([^)]+)\)/)?.[1] || 
                          name;
            const amountText = amountEl.textContent?.trim() || '0';
            const valueText = valueEl?.textContent?.trim() || '0';

            // Parse numeric values
            const amount = parseFloat(amountText.replace(/[^0-9.-]/g, '')) || 0;
            const value = parseFloat(valueText.replace(/[^0-9.-]/g, '')) || 0;

            if (amount > 0 || value > 0) {
              data.push({
                asset: name,
                symbol: symbol.toUpperCase(),
                balance: amount,
                value: value,
                valueCurrency: valueText.includes('₿') ? 'BTC' : 
                              valueText.includes('$') ? 'USD' : 'USD'
              });
            }
          }
        } catch (e) {
          // Skip problematic rows
        }
      });

      return data;
    }, this.selectors);

    console.log(`[BalanceScraper] Extracted ${balances.length} balances`);
    
    return {
      exchange: this.config.name,
      timestamp: new Date().toISOString(),
      totalAssets: balances.length,
      balances: balances,
      totalValue: balances.reduce((sum, b) => sum + b.value, 0)
    };
  }

  /**
   * Extract only dust positions (small balances)
   */
  async extractDustPositions() {
    console.log('[BalanceScraper] Extracting dust positions...');
    
    const allBalances = await this.extractAllBalances();
    
    // Filter for dust positions
    const dustPositions = allBalances.balances.filter(balance => {
      const value = balance.value;
      const threshold = this.selectors.dustThreshold;
      
      // Consider dust if value is below threshold and balance is non-zero
      return value > 0 && value < threshold && balance.balance > 0;
    });

    console.log(`[BalanceScraper] Found ${dustPositions.length} dust positions`);

    return {
      exchange: this.config.name,
      timestamp: new Date().toISOString(),
      dustCount: dustPositions.length,
      dustPositions: dustPositions,
      totalDustValue: dustPositions.reduce((sum, b) => sum + b.value, 0),
      threshold: this.selectors.dustThreshold
    };
  }

  /**
   * Wait for loading indicators to disappear
   */
  async waitForLoadingComplete(timeout = 30000) {
    console.log('[BalanceScraper] Waiting for data to load...');
    
    const startTime = Date.now();
    
    while (Date.now() - startTime < timeout) {
      const isLoading = await this.page.evaluate((selector) => {
        const loadingElements = document.querySelectorAll(selector);
        return loadingElements.length > 0 && 
               Array.from(loadingElements).some(el => el.offsetParent !== null);
      }, this.selectors.loadingIndicator);

      if (!isLoading) {
        // Additional wait for any dynamic content
        await this.page.waitForTimeout(1000);
        return;
      }

      await this.page.waitForTimeout(500);
    }

    console.log('[BalanceScraper] Loading timeout reached, proceeding anyway');
  }

  /**
   * Get specific asset balance
   */
  async getAssetBalance(symbol) {
    const allBalances = await this.extractAllBalances();
    return allBalances.balances.find(b => 
      b.symbol.toLowerCase() === symbol.toLowerCase()
    );
  }

  /**
   * Check if exchange supports dust conversion/sweeping
   */
  async canConvertDust() {
    if (!this.config.hasDustSweeping) {
      return false;
    }

    // Look for dust conversion buttons/links
    const dustSelectors = [
      'button:has-text("Convert Dust")',
      'button:has-text("Sweep Dust")',
      'a[href*="dust"]',
      '[data-testid="dust-conversion"]'
    ];

    for (const selector of dustSelectors) {
      const element = await this.page.$(selector);
      if (element) {
        return true;
      }
    }

    return false;
  }

  /**
   * Navigate to dust conversion page if available
   */
  async navigateToDustConversion() {
    if (!await this.canConvertDust()) {
      throw new Error('Dust conversion not available on this exchange');
    }

    const dustUrls = {
      binance: 'https://www.binance.com/en/my/wallet/account/dust',
      coinbase: 'https://www.coinbase.com/accounts/dust',
      kucoin: 'https://www.kucoin.com/assets/dust'
    };

    const url = dustUrls[this.config.name.toLowerCase()];
    if (url) {
      await this.page.goto(url, { waitUntil: 'networkidle' });
      await this.waitForLoadingComplete();
    }
  }

  /**
   * Get balance summary (total value, top holdings, etc.)
   */
  async getBalanceSummary() {
    const allBalances = await this.extractAllBalances();
    
    const sortedByValue = [...allBalances.balances].sort((a, b) => b.value - a.value);
    const dustPositions = await this.extractDustPositions();

    return {
      exchange: this.config.name,
      timestamp: new Date().toISOString(),
      summary: {
        totalAssets: allBalances.totalAssets,
        totalValue: allBalances.totalValue,
        topHoldings: sortedByValue.slice(0, 5),
        dustCount: dustPositions.dustCount,
        dustValue: dustPositions.totalDustValue,
        dustPercentage: allBalances.totalValue > 0 
          ? (dustPositions.totalDustValue / allBalances.totalValue * 100).toFixed(2)
          : 0
      }
    };
  }
}

module.exports = BalanceScraper;
