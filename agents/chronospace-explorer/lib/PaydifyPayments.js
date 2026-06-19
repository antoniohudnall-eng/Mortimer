// Paydify Payment Integration for DroidScript
// Skill: paydify-payments

/**
 * Initialize Paydify Payment Handler
 * @param {Object} config - Configuration object
 * @param {string} config.apiKey - Paydify API key
 * @param {string} config.merchantId - Your merchant ID
 * @param {string} config.currency - Default currency (BTC, ETH, etc.)
 * @param {string} config.environment - 'sandbox' or 'production'
 */
function PaydifyPayments(config) {
    this.apiKey = config.apiKey;
    this.merchantId = config.merchantId;
    this.currency = config.currency || "BTC";
    this.environment = config.environment || "sandbox";
    this.baseUrl = this.environment === "production" 
        ? "https://api.paydify.com/v1" 
        : "https://sandbox-api.paydify.com/v1";
    this.pendingPayments = {};
}

/**
 * Create a new payment request
 * @param {Object} options
 * @param {number} options.amount - Amount to charge
 * @param {string} options.currency - Crypto currency (BTC, ETH, etc.)
 * @param {string} options.description - Payment description
 * @param {string} options.orderId - Your internal order ID
 * @param {function} callback - Callback function(paymentData, error)
 */
PaydifyPayments.prototype.createPayment = function(options, callback) {
    var self = this;
    var paymentData = {
        merchant_id: this.merchantId,
        amount: options.amount,
        currency: options.currency || this.currency,
        description: options.description,
        order_id: options.orderId,
        callback_url: options.callbackUrl || "",
        metadata: options.metadata || {}
    };

    var xhr = new XMLHttpRequest();
    xhr.open("POST", this.baseUrl + "/payments", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader("Authorization", "Bearer " + this.apiKey);
    
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            if (xhr.status === 200 || xhr.status === 201) {
                var response = JSON.parse(xhr.responseText);
                self.pendingPayments[response.payment_id] = response;
                if (callback) callback(response, null);
            } else {
                if (callback) callback(null, {
                    status: xhr.status,
                    message: xhr.responseText
                });
            }
        }
    };
    
    xhr.send(JSON.stringify(paymentData));
};

/**
 * Display payment QR code in game
 * @param {Object} paymentData - Data from createPayment
 * @param {Object} uiConfig - UI configuration
 */
PaydifyPayments.prototype.displayPaymentUI = function(paymentData, uiConfig) {
    var lay = uiConfig.layout || app.CreateLayout("Linear", "VCenter,FillXY");
    
    // Payment amount display
    var txtAmount = app.CreateText(
        "Pay " + paymentData.amount + " " + paymentData.currency,
        0.8, -1, "Multiline"
    );
    txtAmount.SetTextSize(24);
    txtAmount.SetTextColor("#FFFFFF");
    lay.AddChild(txtAmount);
    
    // QR Code image
    var imgQR = app.CreateImage(paymentData.qr_code_url, 0.5, -1);
    imgQR.SetMargins(0, 0.05, 0, 0.05);
    lay.AddChild(imgQR);
    
    // Wallet address (copyable)
    var txtAddress = app.CreateText(
        "Address: " + paymentData.wallet_address.substring(0, 20) + "...",
        0.8, -1
    );
    txtAddress.SetTextSize(14);
    txtAddress.SetTextColor("#AAAAAA");
    lay.AddChild(txtAddress);
    
    // Status text
    var txtStatus = app.CreateText("Waiting for payment...", 0.8, -1);
    txtStatus.SetTextSize(16);
    txtStatus.SetTextColor("#FFD700");
    lay.AddChild(txtStatus);
    
    // Start polling for payment status
    this.pollPaymentStatus(paymentData.payment_id, function(status) {
        txtStatus.SetText("Status: " + status);
        if (status === "confirmed") {
            txtStatus.SetTextColor("#00FF00");
            if (uiConfig.onSuccess) uiConfig.onSuccess(paymentData);
        } else if (status === "expired" || status === "failed") {
            txtStatus.SetTextColor("#FF0000");
            if (uiConfig.onFailure) uiConfig.onFailure(paymentData);
        }
    });
    
    return lay;
};

/**
 * Poll for payment status
 * @param {string} paymentId - Payment ID to check
 * @param {function} callback - Callback function(status, paymentData)
 * @param {number} interval - Polling interval in ms (default: 5000)
 */
PaydifyPayments.prototype.pollPaymentStatus = function(paymentId, callback, interval) {
    var self = this;
    interval = interval || 5000;
    
    var checkStatus = function() {
        var xhr = new XMLHttpRequest();
        xhr.open("GET", self.baseUrl + "/payments/" + paymentId, true);
        xhr.setRequestHeader("Authorization", "Bearer " + self.apiKey);
        
        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4 && xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                var status = response.status;
                
                if (callback) callback(status, response);
                
                // Continue polling if pending
                if (status === "pending" || status === "unconfirmed") {
                    setTimeout(checkStatus, interval);
                }
            }
        };
        
        xhr.send();
    };
    
    checkStatus();
};

/**
 * Verify payment webhook signature
 * @param {string} payload - Raw request body
 * @param {string} signature - Signature header
 * @param {string} secret - Webhook secret
 * @returns {boolean} - Valid signature
 */
PaydifyPayments.prototype.verifyWebhook = function(payload, signature, secret) {
    // Simplified verification - use crypto library in production
    return signature === "sha256=" + this.simpleHash(payload + secret);
};

PaydifyPayments.prototype.simpleHash = function(str) {
    var hash = 0;
    for (var i = 0; i < str.length; i++) {
        var char = str.charCodeAt(i);
        hash = ((hash << 5) - hash) + char;
        hash = hash & hash;
    }
    return hash.toString(16);
};

/**
 * Get payment history
 * @param {function} callback - Callback function(payments, error)
 * @param {Object} filters - Optional filters (startDate, endDate, status)
 */
PaydifyPayments.prototype.getPaymentHistory = function(callback, filters) {
    var url = this.baseUrl + "/payments?merchant_id=" + this.merchantId;
    
    if (filters) {
        if (filters.startDate) url += "&start_date=" + filters.startDate;
        if (filters.endDate) url += "&end_date=" + filters.endDate;
        if (filters.status) url += "&status=" + filters.status;
    }
    
    var xhr = new XMLHttpRequest();
    xhr.open("GET", url, true);
    xhr.setRequestHeader("Authorization", "Bearer " + this.apiKey);
    
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

// Export for DroidScript
if (typeof module !== 'undefined' && module.exports) {
    module.exports = PaydifyPayments;
}
