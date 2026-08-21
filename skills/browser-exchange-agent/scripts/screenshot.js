#!/usr/bin/env node
/**
 * screenshot.js - Screenshot utility for verification and debugging
 */

const fs = require('fs').promises;
const path = require('path');

class ScreenshotUtil {
  constructor(page) {
    this.page = page;
    this.screenshotDir = path.join(process.cwd(), 'screenshots');
  }

  /**
   * Initialize screenshot directory
   */
  async initDirectory() {
    try {
      await fs.mkdir(this.screenshotDir, { recursive: true });
    } catch (error) {
      console.error('[ScreenshotUtil] Failed to create screenshot directory:', error.message);
    }
  }

  /**
   * Generate filename with timestamp
   */
  generateFilename(prefix = 'screenshot') {
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    return `${prefix}_${timestamp}.png`;
  }

  /**
   * Capture screenshot
   */
  async capture(name = 'screenshot', options = {}) {
    await this.initDirectory();

    const {
      fullPage = false,
      clip = null,
      type = 'png',
      quality = 90,
      outputPath = null,
      maskSelectors = [],
      hideSelectors = []
    } = options;

    const filename = outputPath || path.join(this.screenshotDir, this.generateFilename(name));

    console.log(`[ScreenshotUtil] Capturing screenshot: ${filename}`);

    try {
      // Hide sensitive elements before screenshot
      if (hideSelectors.length > 0) {
        await this.hideElements(hideSelectors);
      }

      // Mask sensitive data
      if (maskSelectors.length > 0) {
        await this.maskElements(maskSelectors);
      }

      const screenshotOptions = {
        path: filename,
        fullPage,
        type
      };

      if (clip) {
        screenshotOptions.clip = clip;
      }

      if (type === 'jpeg') {
        screenshotOptions.quality = quality;
      }

      await this.page.screenshot(screenshotOptions);

      // Restore hidden elements
      if (hideSelectors.length > 0) {
        await this.showElements(hideSelectors);
      }

      console.log(`[ScreenshotUtil] Screenshot saved: ${filename}`);
      return filename;

    } catch (error) {
      console.error('[ScreenshotUtil] Screenshot failed:', error.message);
      throw error;
    }
  }

  /**
   * Capture element screenshot
   */
  async captureElement(selector, name = 'element', options = {}) {
    await this.initDirectory();

    const element = await this.page.$(selector);
    if (!element) {
      throw new Error(`Element not found: ${selector}`);
    }

    const filename = options.outputPath || 
                     path.join(this.screenshotDir, this.generateFilename(name));

    await element.screenshot({ path: filename });
    console.log(`[ScreenshotUtil] Element screenshot saved: ${filename}`);
    
    return filename;
  }

  /**
   * Capture screenshot of specific region
   */
  async captureRegion(x, y, width, height, name = 'region') {
    return this.capture(name, {
      clip: { x, y, width, height }
    });
  }

  /**
   * Hide elements (useful for removing sensitive data from screenshots)
   */
  async hideElements(selectors) {
    await this.page.evaluate((selectors) => {
      selectors.forEach(selector => {
        const elements = document.querySelectorAll(selector);
        elements.forEach(el => {
          el.dataset.originalDisplay = el.style.display;
          el.style.display = 'none';
        });
      });
    }, selectors);
  }

  /**
   * Show previously hidden elements
   */
  async showElements(selectors) {
    await this.page.evaluate((selectors) => {
      selectors.forEach(selector => {
        const elements = document.querySelectorAll(selector);
        elements.forEach(el => {
          if (el.dataset.originalDisplay !== undefined) {
            el.style.display = el.dataset.originalDisplay;
            delete el.dataset.originalDisplay;
          }
        });
      });
    }, selectors);
  }

  /**
   * Mask elements with a black box (better than hiding for layout)
   */
  async maskElements(selectors) {
    await this.page.evaluate((selectors) => {
      selectors.forEach(selector => {
        const elements = document.querySelectorAll(selector);
        elements.forEach(el => {
          el.dataset.originalFilter = el.style.filter;
          el.style.filter = 'blur(10px)';
        });
      });
    }, selectors);
  }

  /**
   * Unmask elements
   */
  async unmaskElements(selectors) {
    await this.page.evaluate((selectors) => {
      selectors.forEach(selector => {
        const elements = document.querySelectorAll(selector);
        elements.forEach(el => {
          if (el.dataset.originalFilter !== undefined) {
            el.style.filter = el.dataset.originalFilter;
            delete el.dataset.originalFilter;
          }
        });
      });
    }, selectors);
  }

  /**
   * Capture screenshot with sensitive data masked
   */
  async captureSecure(name = 'secure', options = {}) {
    const defaultHideSelectors = [
      'input[type="password"]',
      '[data-testid="api-key"]',
      '[data-testid="secret-key"]',
      '.private-key',
      '.seed-phrase'
    ];

    const defaultMaskSelectors = [
      '.balance-amount',
      '.account-value',
      '.wallet-address',
      '[data-testid="balance"]'
    ];

    return this.capture(name, {
      ...options,
      hideSelectors: [...defaultHideSelectors, ...(options.hideSelectors || [])],
      maskSelectors: [...defaultMaskSelectors, ...(options.maskSelectors || [])]
    });
  }

  /**
   * Capture screenshot on error
   */
  async captureError(errorContext = {}) {
    const { error, context = 'error' } = errorContext;
    
    console.log(`[ScreenshotUtil] Capturing error screenshot for: ${context}`);
    
    const filename = await this.capture(`error_${context}`, {
      fullPage: true
    });

    // Also save error details
    const errorLogPath = filename.replace('.png', '.json');
    const errorData = {
      timestamp: new Date().toISOString(),
      context,
      url: this.page.url(),
      error: error ? {
        message: error.message,
        stack: error.stack
      } : null
    };

    try {
      await fs.writeFile(errorLogPath, JSON.stringify(errorData, null, 2));
    } catch (e) {
      console.error('[ScreenshotUtil] Failed to save error log:', e.message);
    }

    return { screenshot: filename, log: errorLogPath };
  }

  /**
   * Capture before/after screenshots for comparison
   */
  async captureComparison(action, actionFn, options = {}) {
    const beforePath = await this.capture('before_' + action, options);
    
    await actionFn();
    
    const afterPath = await this.capture('after_' + action, options);

    return {
      before: beforePath,
      after: afterPath
    };
  }

  /**
   * Clean up old screenshots
   */
  async cleanup(maxAge = 7 * 24 * 60 * 60 * 1000) { // 7 days default
    try {
      const files = await fs.readdir(this.screenshotDir);
      const now = Date.now();
      let deleted = 0;

      for (const file of files) {
        const filePath = path.join(this.screenshotDir, file);
        const stats = await fs.stat(filePath);
        
        if (now - stats.mtime.getTime() > maxAge) {
          await fs.unlink(filePath);
          deleted++;
        }
      }

      console.log(`[ScreenshotUtil] Cleaned up ${deleted} old screenshots`);
      return deleted;
    } catch (error) {
      console.error('[ScreenshotUtil] Cleanup failed:', error.message);
      return 0;
    }
  }

  /**
   * Get list of all screenshots
   */
  async listScreenshots() {
    try {
      const files = await fs.readdir(this.screenshotDir);
      const screenshots = [];

      for (const file of files) {
        if (file.endsWith('.png') || file.endsWith('.jpg') || file.endsWith('.jpeg')) {
          const filePath = path.join(this.screenshotDir, file);
          const stats = await fs.stat(filePath);
          
          screenshots.push({
            filename: file,
            path: filePath,
            size: stats.size,
            created: stats.birthtime,
            modified: stats.mtime
          });
        }
      }

      return screenshots.sort((a, b) => b.modified - a.modified);
    } catch (error) {
      console.error('[ScreenshotUtil] Failed to list screenshots:', error.message);
      return [];
    }
  }
}

module.exports = ScreenshotUtil;
