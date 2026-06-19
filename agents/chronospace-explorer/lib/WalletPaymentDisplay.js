// Direct Wallet Payment Display for DroidScript
// Simple fallback for crypto payments without API integration

/**
 * Wallet Payment Display
 * Shows a BTC wallet address for direct payments
 * @param {Object} config - Configuration
 * @param {string} config.walletAddress - Your BTC wallet address
 * @param {number} config.suggestedAmount - Suggested payment amount in BTC
 * @param {string} config.label - Payment label/description
 */
function WalletPaymentDisplay(config) {
    this.walletAddress = config.walletAddress;
    this.suggestedAmount = config.suggestedAmount || 0.001;
    this.label = config.label || "Game Purchase";
    this.qrCodeUrl = null;
}

/**
 * Generate BIP21 payment URI
 * @returns {string} Bitcoin payment URI
 */
WalletPaymentDisplay.prototype.generatePaymentURI = function(amount, label) {
    amount = amount || this.suggestedAmount;
    label = label || this.label;
    return "bitcoin:" + this.walletAddress + "?amount=" + amount + "&label=" + encodeURIComponent(label);
};

/**
 * Generate QR code URL using Google Chart API
 * @param {string} data - Data to encode
 * @returns {string} QR code image URL
 */
WalletPaymentDisplay.prototype.generateQRCode = function(data) {
    var encoded = encodeURIComponent(data);
    return "https://chart.googleapis.com/chart?cht=qr&chs=300x300&chl=" + encoded;
};

/**
 * Display payment screen on game exit
 * @param {Object} options
 * @param {number} options.amount - Payment amount
 * @param {string} options.message - Custom message
 * @param {function} options.onDismiss - Callback when dismissed
 */
WalletPaymentDisplay.prototype.showExitPaymentScreen = function(options) {
    options = options || {};
    var amount = options.amount || this.suggestedAmount;
    var message = options.message || "Support the developer!";
    
    // Create dialog layout
    var layDlg = app.CreateLayout("Linear", "VCenter,FillXY");
    layDlg.SetBackgroundColor("#1a1a2e");
    
    // Title
    var txtTitle = app.CreateText("☕ Buy Me a Coffee", 0.9, -1);
    txtTitle.SetTextSize(28);
    txtTitle.SetTextColor("#FFD700");
    layDlg.AddChild(txtTitle);
    
    // Message
    var txtMsg = app.CreateText(message, 0.9, -1, "Multiline");
    txtMsg.SetTextSize(16);
    txtMsg.SetTextColor("#FFFFFF");
    txtMsg.SetMargins(0, 0.02, 0, 0.02);
    layDlg.AddChild(txtMsg);
    
    // Suggested amount buttons
    var layAmounts = app.CreateLayout("Linear", "Horizontal");
    var amounts = [0.0001, 0.001, 0.01];
    var self = this;
    
    amounts.forEach(function(amt) {
        var btn = app.CreateButton(amt + " BTC", 0.28, 0.08);
        btn.SetOnTouch(function() {
            self.updatePaymentDisplay(layQR, amt);
        });
        layAmounts.AddChild(btn);
    });
    layDlg.AddChild(layAmounts);
    
    // QR Code display area
    var layQR = app.CreateLayout("Linear", "VCenter");
    layQR.SetMargins(0, 0.05, 0, 0.05);
    layDlg.AddChild(layQR);
    
    // Initial display
    this.updatePaymentDisplay(layQR, amount);
    
    // Wallet address (copyable text)
    var txtAddress = app.CreateText(
        "Wallet: " + this.walletAddress.substring(0, 12) + "..." + this.walletAddress.substring(this.walletAddress.length - 8),
        0.9, -1
    );
    txtAddress.SetTextSize(12);
    txtAddress.SetTextColor("#AAAAAA");
    layDlg.AddChild(txtAddress);
    
    // Copy address button
    var btnCopy = app.CreateButton("Copy Address", 0.6, 0.08);
    btnCopy.SetOnTouch(function() {
        app.SetClipboardText(self.walletAddress);
        app.ShowPopup("Address copied!");
    });
    layDlg.AddChild(btnCopy);
    
    // Dismiss button
    var btnDismiss = app.CreateButton("Maybe Later", 0.6, 0.08);
    btnDismiss.SetMargins(0, 0.02, 0, 0);
    btnDismiss.SetOnTouch(function() {
        dlg.Dismiss();
        if (options.onDismiss) options.onDismiss();
    });
    layDlg.AddChild(btnDismiss);
    
    // Show dialog
    var dlg = app.CreateDialog("Support Development");
    dlg.SetBackColor("#1a1a2e");
    dlg.AddLayout(layDlg);
    dlg.Show();
    
    return dlg;
};

/**
 * Update QR code display
 * @private
 */
WalletPaymentDisplay.prototype.updatePaymentDisplay = function(layout, amount) {
    layout.RemoveAllViews();
    
    var uri = this.generatePaymentURI(amount);
    var qrUrl = this.generateQRCode(uri);
    
    var txtAmount = app.CreateText("Send " + amount + " BTC", 0.8, -1);
    txtAmount.SetTextSize(18);
    txtAmount.SetTextColor("#00FF00");
    layout.AddChild(txtAmount);
    
    var imgQR = app.CreateImage(qrUrl, 0.5, -1);
    layout.AddChild(imgQR);
    
    // Open wallet button
    var self = this;
    var btnOpen = app.CreateButton("Open Wallet App", 0.5, 0.07);
    btnOpen.SetOnTouch(function() {
        app.OpenUrl(uri);
    });
    layout.AddChild(btnOpen);
};

/**
 * Simple payment verification (manual check)
 * In production, use block explorer API or payment processor
 * @param {string} txid - Transaction ID
 * @param {function} callback - Callback function(verified, confirmations)
 */
WalletPaymentDisplay.prototype.verifyPayment = function(txid, callback) {
    // Use blockchain.info API for verification
    var url = "https://blockchain.info/rawtx/" + txid;
    
    var xhr = new XMLHttpRequest();
    xhr.open("GET", url, true);
    
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                var data = JSON.parse(xhr.responseText);
                callback(true, data.confirmations || 0);
            } else {
                callback(false, 0);
            }
        }
    };
    
    xhr.send();
};

/**
 * Check wallet balance (public address only)
 * @param {function} callback - Callback function(balance, error)
 */
WalletPaymentDisplay.prototype.checkBalance = function(callback) {
    var url = "https://blockchain.info/q/addressbalance/" + this.walletAddress;
    
    var xhr = new XMLHttpRequest();
    xhr.open("GET", url, true);
    
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                // Balance is in satoshis, convert to BTC
                var satoshis = parseInt(xhr.responseText);
                var btc = satoshis / 100000000;
                callback(btc, null);
            } else {
                callback(null, "Failed to fetch balance");
            }
        }
    };
    
    xhr.send();
};

// Export
if (typeof module !== 'undefined' && module.exports) {
    module.exports = WalletPaymentDisplay;
}
