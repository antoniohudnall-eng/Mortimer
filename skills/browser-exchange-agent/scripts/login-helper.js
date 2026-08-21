#!/usr/bin/env node
/**
 * login-helper.js - Handles exchange login flows with 2FA and CAPTCHA support
 */

const speakeasy = require('speakeasy');

class LoginHelper {
  constructor(page, exchangeConfig) {
    this.page = page;
    this.config = exchangeConfig;
    this.selectors = this.getSelectors();
  }

  /**
   * Get CSS selectors for the current exchange
   */
  getSelectors() {
    const selectors = {
      coinbase: {
        usernameField: 'input[name="email"], input[type="email"], #email',
        passwordField: 'input[name="password"], input[type="password"], #password',
        submitButton: 'button[type="submit"], [data-testid="submit-button"], input[type="submit"]',
        twoFactorField: 'input[name="code"], input[name="totp"], input[name="2fa"], input[type="tel"]',
        twoFactorSubmit: 'button[type="submit"], [data-testid="verify-button"]',
        captchaFrame: 'iframe[src*="captcha"], iframe[src*="recaptcha"], iframe[src*="hcaptcha"]',
        staySignedIn: 'input[name="remember_me"], input[name="stay_signed_in"]',
        errorMessage: '[data-testid="error-message"], .error-message, .alert-error, [role="alert"]'
      },
      kraken: {
        usernameField: 'input[name="username"], input[name="email"], #username',
        passwordField: 'input[name="password"], input[type="password"], #password',
        submitButton: 'button[type="submit"], .button[type="submit"], .sign-in-button',
        twoFactorField: 'input[name="otp"], input[name="totp"], input[name="code"], #otp',
        twoFactorSubmit: 'button[type="submit"], .button[type="submit"]',
        captchaFrame: 'iframe[src*="captcha"], iframe[src*="recaptcha"]',
        staySignedIn: 'input[name="remember"]',
        errorMessage: '.error, .alert, .notification-error'
      },
      binance: {
        usernameField: 'input[name="email"], input[id="email"], input[data-testid="email-input"]',
        passwordField: 'input[name="password"], input[type="password"], input[id="password"]',
        submitButton: 'button[type="submit"], .login-btn, button[id="click_login_submit"]',
        twoFactorField: 'input[name="code"], input[id="code"], input[placeholder*="2FA"], input[placeholder*="authenticator"]',
        twoFactorSubmit: 'button[type="submit"], .verify-btn',
        captchaFrame: 'iframe[id*="captcha"], .geetest_canvas_slice, #clickCaptcha',
        staySignedIn: 'input[name="remember"], .remember-checkbox',
        errorMessage: '.error-msg, .toast-error, [data-testid="error"]'
      },
      kucoin: {
        usernameField: 'input[name="email"], input[name="loginName"], input[type="email"]',
        passwordField: 'input[name="password"], input[type="password"]',
        submitButton: 'button[type="submit"], .login-btn, button.login',
        twoFactorField: 'input[name="code"], input[name="otp"], input[placeholder*="2FA"]',
        twoFactorSubmit: 'button[type="submit"], .verify-btn',
        captchaFrame: 'iframe[src*="captcha"], .geetest-wrap',
        staySignedIn: 'input[name="remember"]',
        errorMessage: '.error-tip, .error-message, .ant-message-error'
      },
      gemini: {
        usernameField: 'input[name="email"], input[type="email"], #email',
        passwordField: 'input[name="password"], input[type="password"], #password',
        submitButton: 'button[type="submit"], input[type="submit"]',
        twoFactorField: 'input[name="code"], input[name="twoFactorCode"], input[placeholder*="code"]',
        twoFactorSubmit: 'button[type="submit"], button:has-text("Verify")',
        captchaFrame: 'iframe[src*="captcha"], iframe[src*="recaptcha"]',
        staySignedIn: 'input[name="rememberDevice"]',
        errorMessage: '.error, .alert-danger, [role="alert"]'
      }
    };

    return selectors[this.config.name.toLowerCase()] || selectors.coinbase;
  }

  /**
   * Main login method
   */
  async login(credentials) {
    const { username, password, twoFactorSecret } = credentials;

    if (!username || !password) {
      throw new Error('Username and password are required');
    }

    console.log(`[LoginHelper] Navigating to ${this.config.name} login page...`);
    
    // Navigate to login page
    await this.page.goto(this.config.loginUrl, { 
      waitUntil: 'networkidle',
      timeout: 60000 
    });

    // Wait for page to be fully loaded
    await this.page.waitForLoadState('domcontentloaded');
    
    // Check for CAPTCHA
    const hasCaptcha = await this.detectCaptcha();
    if (hasCaptcha) {
      console.log('[LoginHelper] CAPTCHA detected - manual intervention required');
      await this.handleCaptcha();
    }

    // Fill username
    console.log('[LoginHelper] Filling username...');
    await this.fillField(this.selectors.usernameField, username);

    // Fill password
    console.log('[LoginHelper] Filling password...');
    await this.fillField(this.selectors.passwordField, password);

    // Check "stay signed in" if available
    await this.checkStaySignedIn();

    // Submit login form
    console.log('[LoginHelper] Submitting login form...');
    await this.clickElement(this.selectors.submitButton);

    // Wait for navigation
    await this.page.waitForLoadState('networkidle');

    // Check for 2FA
    if (this.config.requires2FA) {
      const needs2FA = await this.detect2FA();
      if (needs2FA) {
        console.log('[LoginHelper] 2FA required');
        await this.handle2FA(twoFactorSecret);
      }
    }

    // Verify login success
    const loginSuccess = await this.verifyLoginSuccess();
    
    if (!loginSuccess) {
      const errorMessage = await this.getErrorMessage();
      throw new Error(`Login failed: ${errorMessage || 'Unknown error'}`);
    }

    console.log('[LoginHelper] Login successful');
    return { success: true, timestamp: new Date().toISOString() };
  }

  /**
   * Fill a form field with retry logic
   */
  async fillField(selector, value, retries = 3) {
    for (let i = 0; i < retries; i++) {
      try {
        const element = await this.page.waitForSelector(selector, { timeout: 10000 });
        await element.click();
        await element.fill(value);
        
        // Verify value was entered
        const actualValue = await element.inputValue();
        if (actualValue === value) {
          return;
        }
      } catch (error) {
        if (i === retries - 1) throw error;
        await this.page.waitForTimeout(1000);
      }
    }
  }

  /**
   * Click an element with retry logic
   */
  async clickElement(selector, retries = 3) {
    for (let i = 0; i < retries; i++) {
      try {
        const element = await this.page.waitForSelector(selector, { timeout: 10000 });
        await element.click();
        return;
      } catch (error) {
        if (i === retries - 1) throw error;
        await this.page.waitForTimeout(1000);
      }
    }
  }

  /**
   * Detect if CAPTCHA is present
   */
  async detectCaptcha() {
    try {
      const captchaFrame = await this.page.$(this.selectors.captchaFrame);
      return captchaFrame !== null;
    } catch {
      return false;
    }
  }

  /**
   * Handle CAPTCHA - requires manual intervention in headed mode
   */
  async handleCaptcha() {
    // In headed mode, wait for user to solve CAPTCHA
    console.log('[LoginHelper] Waiting for CAPTCHA to be solved (60 seconds)...');
    
    // Wait for CAPTCHA frame to disappear
    await this.page.waitForFunction(
      (selector) => !document.querySelector(selector),
      this.selectors.captchaFrame,
      { timeout: 60000 }
    );
    
    console.log('[LoginHelper] CAPTCHA appears to be solved');
  }

  /**
   * Check "stay signed in" checkbox
   */
  async checkStaySignedIn() {
    try {
      const checkbox = await this.page.$(this.selectors.staySignedIn);
      if (checkbox) {
        const isChecked = await checkbox.isChecked();
        if (!isChecked) {
          await checkbox.check();
        }
      }
    } catch {
      // Checkbox may not exist, that's ok
    }
  }

  /**
   * Detect if 2FA is required
   */
  async detect2FA() {
    try {
      // Wait a moment for 2FA field to appear
      await this.page.waitForTimeout(2000);
      
      const twoFactorField = await this.page.$(this.selectors.twoFactorField);
      return twoFactorField !== null;
    } catch {
      return false;
    }
  }

  /**
   * Handle 2FA authentication
   */
  async handle2FA(twoFactorSecret) {
    if (!twoFactorSecret) {
      throw new Error('2FA secret is required but not provided');
    }

    console.log('[LoginHelper] Generating 2FA code...');
    
    // Generate TOTP code
    const token = speakeasy.totp({
      secret: twoFactorSecret,
      encoding: 'base32'
    });

    console.log('[LoginHelper] Entering 2FA code...');
    await this.fillField(this.selectors.twoFactorField, token);

    // Submit 2FA
    await this.clickElement(this.selectors.twoFactorSubmit);

    // Wait for navigation
    await this.page.waitForLoadState('networkidle');
  }

  /**
   * Verify login was successful
   */
  async verifyLoginSuccess() {
    // Check if we're on the balances/dashboard page
    const currentUrl = this.page.url();
    
    // Success indicators
    const successIndicators = [
      currentUrl.includes('accounts'),
      currentUrl.includes('dashboard'),
      currentUrl.includes('wallet'),
      currentUrl.includes('balances'),
      currentUrl.includes('portfolio'),
      currentUrl.includes('trade'),
      !currentUrl.includes('login'),
      !currentUrl.includes('signin')
    ];

    // Check for error messages
    const hasError = await this.page.$(this.selectors.errorMessage) !== null;
    
    return successIndicators.some(indicator => indicator) && !hasError;
  }

  /**
   * Get error message if login failed
   */
  async getErrorMessage() {
    try {
      const errorElement = await this.page.$(this.selectors.errorMessage);
      if (errorElement) {
        return await errorElement.textContent();
      }
    } catch {
      // No error message found
    }
    return null;
  }

  /**
   * Check if session is still valid
   */
  async isSessionValid() {
    try {
      await this.page.goto(this.config.balancesUrl, { 
        waitUntil: 'domcontentloaded',
        timeout: 30000 
      });
      
      const currentUrl = this.page.url();
      return !currentUrl.includes('login') && !currentUrl.includes('signin');
    } catch {
      return false;
    }
  }

  /**
   * Logout from exchange
   */
  async logout() {
    console.log('[LoginHelper] Logging out...');
    
    // Common logout selectors
    const logoutSelectors = [
      'a[href*="logout"]',
      'button:has-text("Log out")',
      'button:has-text("Sign out")',
      '[data-testid="logout-button"]'
    ];

    for (const selector of logoutSelectors) {
      try {
        const logoutButton = await this.page.$(selector);
        if (logoutButton) {
          await logoutButton.click();
          await this.page.waitForLoadState('networkidle');
          console.log('[LoginHelper] Logout successful');
          return true;
        }
      } catch {
        // Try next selector
      }
    }

    console.log('[LoginHelper] Could not find logout button');
    return false;
  }
}

module.exports = LoginHelper;
