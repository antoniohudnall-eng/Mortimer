// Store Integration Module for DroidScript Games
// Supports Payhip and Paydify store platforms

/**
 * Store Integration Manager
 * @param {Object} config - Store configuration
 */
function StoreIntegration(config) {
    this.payhipApiKey = config.payhipApiKey || null;
    this.paydifyApiKey = config.paydifyApiKey || null;
    this.payhipStoreUrl = config.payhipStoreUrl || null;
    this.paydifyStoreUrl = config.paydifyStoreUrl || null;
    this.productId = config.productId || null;
}

// ==================== PAYHIP INTEGRATION ====================

/**
 * Generate Payhip checkout URL
 * @param {Object} options
 * @param {string} options.productId - Payhip product ID
 * @param {number} options.price - Override price (optional)
 * @returns {string} Checkout URL
 */
StoreIntegration.prototype.getPayhipCheckoutUrl = function(options) {
    var productId = options.productId || this.productId;
    var url = "https://payhip.com/buy?product=" + productId;
    
    if (options.price) {
        url += "&price=" + options.price;
    }
    if (options.affiliate) {
        url += "&affiliate=" + options.affiliate;
    }
    
    return url;
};

/**
 * Open Payhip checkout in browser or WebView
 * @param {Object} options
 */
StoreIntegration.prototype.openPayhipCheckout = function(options) {
    var url = this.getPayhipCheckoutUrl(options);
    
    if (options.useWebView) {
        // Open in embedded WebView
        var web = app.CreateWebView(1, 1);
        web.LoadUrl(url);
        
        var lay = app.CreateLayout("Linear", "FillXY");
        lay.AddChild(web);
        
        var dlg = app.CreateDialog("Complete Purchase");
        dlg.AddLayout(lay);
        dlg.Show();
        
        return dlg;
    } else {
        // Open in system browser
        app.OpenUrl(url);
        return null;
    }
};

/**
 * Verify Payhip purchase via API
 * @param {string} orderId - Payhip order ID
 * @param {function} callback - Callback function(result, error)
 */
StoreIntegration.prototype.verifyPayhipPurchase = function(orderId, callback) {
    if (!this.payhipApiKey) {
        callback(null, "Payhip API key not configured");
        return;
    }
    
    var url = "https://payhip.com/api/v1/orders/" + orderId;
    
    var xhr = new XMLHttpRequest();
    xhr.open("GET", url, true);
    xhr.setRequestHeader("Authorization", "Bearer " + this.payhipApiKey);
    
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                callback(JSON.parse(xhr.responseText), null);
            } else {
                callback(null, { status: xhr.status, message: xhr.responseText });
            }
        }
    };
    
    xhr.send();
};

// ==================== PAYDIFY INTEGRATION ====================

/**
 * Generate Paydify checkout URL
 * @param {Object} options
 * @param {string} options.productId - Paydify product ID
 * @param {string} options.currency - Crypto currency (default: BTC)
 * @returns {string} Checkout URL
 */
StoreIntegration.prototype.getPaydifyCheckoutUrl = function(options) {
    var productId = options.productId || this.productId;
    var currency = options.currency || "BTC";
    
    return this.paydifyStoreUrl + "/checkout/" + productId + "?currency=" + currency;
};

/**
 * Open Paydify crypto checkout
 * @param {Object} options
 */
StoreIntegration.prototype.openPaydifyCheckout = function(options) {
    var url = this.getPaydifyCheckoutUrl(options);
    app.OpenUrl(url);
};

/**
 * Create Paydify payment session
 * @param {Object} options
 * @param {function} callback - Callback function(sessionData, error)
 */
StoreIntegration.prototype.createPaydifySession = function(options, callback) {
    if (!this.paydifyApiKey) {
        callback(null, "Paydify API key not configured");
        return;
    }
    
    var sessionData = {
        product_id: options.productId || this.productId,
        currency: options.currency || "BTC",
        customer_email: options.customerEmail,
        metadata: options.metadata || {}
    };
    
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "https://api.paydify.com/v1/sessions", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader("Authorization", "Bearer " + this.paydifyApiKey);
    
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            if (xhr.status === 200 || xhr.status === 201) {
                callback(JSON.parse(xhr.responseText), null);
            } else {
                callback(null, { status: xhr.status, message: xhr.responseText });
            }
        }
    };
    
    xhr.send(JSON.stringify(sessionData));
};

// ==================== GOOGLE PLAY INTEGRATION ====================

/**
 * Check if running as Google Play build
 * @returns {boolean}
 */
StoreIntegration.prototype.isGooglePlayBuild = function() {
    // Check for Google Play Services
    try {
        var pm = app.GetPackageManager();
        return pm.hasSystemFeature("com.google.android.feature.GOOGLE_BUILD");
    } catch(e) {
        return false;
    }
};

/**
 * Initialize Google Play Billing
 * Requires billing plugin or Google Play API
 */
StoreIntegration.prototype.initGooglePlayBilling = function(callback) {
    // Placeholder for Google Play Billing integration
    // Requires: com.android.billingclient:billing library
    
    if (callback) {
        callback({
            available: this.isGooglePlayBuild(),
            note: "Google Play Billing requires native plugin integration"
        });
    }
};

// ==================== UNIFIED STORE UI ====================

/**
 * Display store selection dialog
 * Shows all available purchase options
 * @param {Object} options
 * @param {string} options.productName - Name of product
 * @param {number} options.priceUsd - Price in USD
 * @param {number} options.priceBtc - Price in BTC
 */
StoreIntegration.prototype.showStoreSelector = function(options) {
    var self = this;
    
    var layDlg = app.CreateLayout("Linear", "VCenter,FillXY");
    layDlg.SetBackgroundColor("#1a1a2e");
    
    // Title
    var txtTitle = app.CreateText("Get " + options.productName, 0.9, -1);
    txtTitle.SetTextSize(26);
    txtTitle.SetTextColor("#FFD700");
    layDlg.AddChild(txtTitle);
    
    // Price display
    var txtPrice = app.CreateText(
        "$" + options.priceUsd + " USD | " + options.priceBtc + " BTC",
        0.9, -1
    );
    txtPrice.SetTextSize(18);
    txtPrice.SetTextColor("#00FF00");
    txtPrice.SetMargins(0, 0.02, 0, 0.05);
    layDlg.AddChild(txtPrice);
    
    // Paydify (Crypto) option
    if (this.paydifyStoreUrl) {
        var btnPaydify = app.CreateButton("💎 Pay with Crypto (Paydify)", 0.85, 0.1);
        btnPaydify.SetTextSize(18);
        btnPaydify.SetOnTouch(function() {
            self.openPaydifyCheckout({ currency: "BTC" });
        });
        layDlg.AddChild(btnPaydify);
    }
    
    // Payhip (Fiat) option
    if (this.payhipStoreUrl) {
        var btnPayhip = app.CreateButton("💳 Pay with Card (Payhip)", 0.85, 0.1);
        btnPayhip.SetTextSize(18);
        btnPayhip.SetMargins(0, 0.02, 0, 0);
        btnPayhip.SetOnTouch(function() {
            self.openPayhipCheckout({ useWebView: true });
        });
        layDlg.AddChild(btnPayhip);
    }
    
    // Google Play option
    if (this.isGooglePlayBuild()) {
        var btnPlay = app.CreateButton("📱 Google Play Store", 0.85, 0.1);
        btnPlay.SetTextSize(18);
        btnPlay.SetMargins(0, 0.02, 0, 0);
        btnPlay.SetOnTouch(function() {
            app.OpenUrl("https://play.google.com/store/apps/details?id=" + app.GetPackageName());
        });
        layDlg.AddChild(btnPlay);
    }
    
    // Direct wallet option
    var btnWallet = app.CreateButton("₿ Direct BTC Transfer", 0.85, 0.1);
    btnWallet.SetTextSize(18);
    btnWallet.SetMargins(0, 0.02, 0, 0);
    btnWallet.SetOnTouch(function() {
        if (options.onDirectWallet) options.onDirectWallet();
    });
    layDlg.AddChild(btnWallet);
    
    // Cancel
    var btnCancel = app.CreateButton("Cancel", 0.6, 0.08);
    btnCancel.SetMargins(0, 0.05, 0, 0);
    btnCancel.SetOnTouch(function() {
        dlg.Dismiss();
    });
    layDlg.AddChild(btnCancel);
    
    var dlg = app.CreateDialog("Choose Payment Method");
    dlg.SetBackColor("#1a1a2e");
    dlg.AddLayout(layDlg);
    dlg.Show();
    
    return dlg;
};

// ==================== LICENSE VERIFICATION ====================

/**
 * Simple license key validation
 * In production, use server-side validation
 * @param {string} licenseKey - User's license key
 * @param {function} callback - Callback function(valid, error)
 */
StoreIntegration.prototype.validateLicense = function(licenseKey, callback) {
    // TODO: Implement server-side license validation
    // This is a placeholder - real implementation needs backend
    
    var url = "https://your-server.com/api/validate-license";
    
    var xhr = new XMLHttpRequest();
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                var result = JSON.parse(xhr.responseText);
                callback(result.valid, result.error);
            } else {
                callback(false, "Validation failed");
            }
        }
    };
    
    xhr.send(JSON.stringify({
        license_key: licenseKey,
        device_id: app.GetDeviceId()
    }));
};

/**
 * Store purchase token locally
 * @param {string} token - Purchase token or license key
 */
StoreIntegration.prototype.storePurchaseToken = function(token) {
    app.SaveText("purchase_token", token);
    app.SaveText("purchase_date", new Date().toISOString());
};

/**
 * Retrieve stored purchase token
 * @returns {string|null}
 */
StoreIntegration.prototype.getPurchaseToken = function() {
    return app.LoadText("purchase_token");
};

/**
 * Check if user has purchased
 * @returns {boolean}
 */
StoreIntegration.prototype.hasPurchased = function() {
    return this.getPurchaseToken() !== null;
};

// Export
if (typeof module !== 'undefined' && module.exports) {
    module.exports = StoreIntegration;
}
