// SGVD Payment Integration Module
// Adds Paydify, Store, and Wallet payment support to Solar GraVitaional Duel

// Load payment libraries (assumes they're in lib/ folder)
var PaydifyPayments = require("./lib/PaydifyPayments.js");
var StoreIntegration = require("./lib/StoreIntegration.js");
var WalletPaymentDisplay = require("./lib/WalletPaymentDisplay.js");

// Payment configuration
var SGVD_PAYMENT_CONFIG = {
    paydify: {
        apiKey: null, // Set your Paydify API key
        merchantId: null, // Set your merchant ID
        currency: "BTC",
        environment: "sandbox"
    },
    payhip: {
        apiKey: null,
        storeUrl: null,
        productId: null
    },
    wallet: {
        address: "bc1q...your...btc...address",
        suggestedAmount: 0.001
    },
    pricing: {
        fullVersion: { usd: 4.99, btc: 0.00012 },
        premiumShips: { usd: 1.99, btc: 0.00005 },
        weaponPack: { usd: 0.99, btc: 0.000025 }
    }
};

var sgvdPaydify = null;
var sgvdStore = null;
var sgvdWallet = null;

function initSGVDPayments() {
    if (SGVD_PAYMENT_CONFIG.paydify.apiKey) {
        sgvdPaydify = new PaydifyPayments(SGVD_PAYMENT_CONFIG.paydify);
    }
    sgvdStore = new StoreIntegration({
        payhipApiKey: SGVD_PAYMENT_CONFIG.payhip.apiKey,
        payhipStoreUrl: SGVD_PAYMENT_CONFIG.payhip.storeUrl,
        paydifyApiKey: SGVD_PAYMENT_CONFIG.paydify.apiKey,
        productId: SGVD_PAYMENT_CONFIG.payhip.productId
    });
    sgvdWallet = new WalletPaymentDisplay({
        walletAddress: SGVD_PAYMENT_CONFIG.wallet.address,
        suggestedAmount: SGVD_PAYMENT_CONFIG.wallet.suggestedAmount,
        label: "SGVD Support"
    });
}

// ==================== IN-GAME STORE ====================

function showSGVDStore() {
    var layStore = app.CreateLayout("Linear", "VCenter,FillXY");
    layStore.SetBackgroundColor("#0a0a1a");
    
    var txtTitle = app.CreateText("🚀 SGVD Store", 0.9, -1);
    txtTitle.SetTextSize(28);
    txtTitle.SetTextColor("#00FF00");
    layStore.AddChild(txtTitle);
    
    // Full Version
    var layFull = createProductRow("Full Version", "Unlock all ships & weapons", 
        SGVD_PAYMENT_CONFIG.pricing.fullVersion, "full");
    layStore.AddChild(layFull);
    
    // Premium Ships
    var layShips = createProductRow("Premium Ships", "5 exclusive ship designs",
        SGVD_PAYMENT_CONFIG.pricing.premiumShips, "ships");
    layStore.AddChild(layShips);
    
    // Weapon Pack
    var layWeapons = createProductRow("Weapon Pack", "Advanced weaponry pack",
        SGVD_PAYMENT_CONFIG.pricing.weaponPack, "weapons");
    layStore.AddChild(layWeapons);
    
    // Close button
    var btnClose = app.CreateButton("Close", 0.5, 0.08);
    btnClose.SetMargins(0, 0.05, 0, 0);
    btnClose.SetOnTouch(function() { dlgStore.Dismiss(); });
    layStore.AddChild(btnClose);
    
    var dlgStore = app.CreateDialog("SGVD Store");
    dlgStore.SetBackColor("#0a0a1a");
    dlgStore.AddLayout(layStore);
    dlgStore.Show();
}

function createProductRow(name, description, pricing, productKey) {
    var layRow = app.CreateLayout("Linear", "Horizontal");
    layRow.SetMargins(0, 0.02, 0, 0);
    
    var layInfo = app.CreateLayout("Linear", "Vertical");
    layInfo.SetSize(0.5, -1);
    
    var txtName = app.CreateText(name, 0.5, -1);
    txtName.SetTextSize(18);
    txtName.SetTextColor("#FFFFFF");
    layInfo.AddChild(txtName);
    
    var txtDesc = app.CreateText(description, 0.5, -1, "Multiline");
    txtDesc.SetTextSize(12);
    txtDesc.SetTextColor("#AAAAAA");
    layInfo.AddChild(txtDesc);
    
    layRow.AddChild(layInfo);
    
    var layPrice = app.CreateLayout("Linear", "Vertical");
    layPrice.SetSize(0.25, -1);
    
    var txtPrice = app.CreateText("$" + pricing.usd, 0.25, -1);
    txtPrice.SetTextSize(16);
    txtPrice.SetTextColor("#00FF00");
    layPrice.AddChild(txtPrice);
    
    var txtBTC = app.CreateText(pricing.btc + " BTC", 0.25, -1);
    txtBTC.SetTextSize(12);
    txtBTC.SetTextColor("#FFD700");
    layPrice.AddChild(txtBTC);
    
    layRow.AddChild(layPrice);
    
    var btnBuy = app.CreateButton("Buy", 0.2, 0.08);
    btnBuy.SetOnTouch(function() {
        showPaymentOptions(productKey, name, pricing);
    });
    layRow.AddChild(btnBuy);
    
    return layRow;
}

function showPaymentOptions(productKey, productName, pricing) {
    var layOptions = app.CreateLayout("Linear", "VCenter,FillXY");
    layOptions.SetBackgroundColor("#0a0a1a");
    
    var txtTitle = app.CreateText("Pay for " + productName, 0.9, -1);
    txtTitle.SetTextSize(22);
    txtTitle.SetTextColor("#FFFFFF");
    layOptions.AddChild(txtTitle);
    
    var txtPrice = app.CreateText("$" + pricing.usd + " / " + pricing.btc + " BTC", 0.9, -1);
    txtPrice.SetTextSize(18);
    txtPrice.SetTextColor("#00FF00");
    layOptions.AddChild(txtPrice);
    
    // Crypto option
    var btnCrypto = app.CreateButton("💎 Pay with Crypto", 0.8, 0.1);
    btnCrypto.SetMargins(0, 0.03, 0, 0);
    btnCrypto.SetOnTouch(function() {
        purchaseWithCrypto(productKey, pricing.btc);
    });
    layOptions.AddChild(btnCrypto);
    
    // Card option
    var btnCard = app.CreateButton("💳 Pay with Card", 0.8, 0.1);
    btnCard.SetMargins(0, 0.02, 0, 0);
    btnCard.SetOnTouch(function() {
        purchaseWithCard(productKey);
    });
    layOptions.AddChild(btnCard);
    
    // Wallet option
    var btnWallet = app.CreateButton("₿ Direct BTC", 0.8, 0.1);
    btnWallet.SetMargins(0, 0.02, 0, 0);
    btnWallet.SetOnTouch(function() {
        showDirectWalletPayment(pricing.btc, productName);
    });
    layOptions.AddChild(btnWallet);
    
    // Cancel
    var btnCancel = app.CreateButton("Cancel", 0.5, 0.08);
    btnCancel.SetMargins(0, 0.03, 0, 0);
    btnCancel.SetOnTouch(function() { dlgOptions.Dismiss(); });
    layOptions.AddChild(btnCancel);
    
    var dlgOptions = app.CreateDialog("Payment Options");
    dlgOptions.SetBackColor("#0a0a1a");
    dlgOptions.AddLayout(layOptions);
    dlgOptions.Show();
}

function purchaseWithCrypto(productKey, amount) {
    if (!sgvdPaydify) {
        app.ShowPopup("Crypto payments not configured");
        return;
    }
    
    sgvdPaydify.createPayment({
        amount: amount,
        description: "SGVD " + productKey,
        orderId: "SGVD-" + productKey + "-" + Date.now()
    }, function(paymentData, error) {
        if (error) {
            app.ShowPopup("Payment failed: " + error.message);
            return;
        }
        
        var layPayment = app.CreateLayout("Linear", "VCenter,FillXY");
        layPayment.SetBackgroundColor("#0a0a1a");
        
        sgvdPaydify.displayPaymentUI(paymentData, {
            layout: layPayment,
            onSuccess: function(data) {
                unlockProduct(productKey);
                app.ShowPopup("✅ " + productKey + " unlocked!");
                setTimeout(function() { dlgPayment.Dismiss(); }, 2000);
            },
            onFailure: function(data) {
                app.ShowPopup("❌ Payment failed");
            }
        });
        
        var dlgPayment = app.CreateDialog("Complete Payment");
        dlgPayment.SetBackColor("#0a0a1a");
        dlgPayment.AddLayout(layPayment);
        dlgPayment.Show();
    });
}

function purchaseWithCard(productKey) {
    if (!SGVD_PAYMENT_CONFIG.payhip.storeUrl) {
        app.ShowPopup("Card payments not configured");
        return;
    }
    sgvdStore.openPayhipCheckout({ useWebView: true });
}

function showDirectWalletPayment(amount, productName) {
    if (!sgvdWallet) {
        app.ShowPopup("Wallet not configured");
        return;
    }
    sgvdWallet.showExitPaymentScreen({
        amount: amount,
        message: "Send " + amount + " BTC to unlock " + productName,
        onDismiss: function() {}
    });
}

// ==================== UNLOCK MANAGEMENT ====================

function unlockProduct(productKey) {
    app.SaveText("sgvd_unlock_" + productKey, "true");
    app.SaveText("sgvd_unlock_date_" + productKey, new Date().toISOString());
    
    switch(productKey) {
        case "full":
            unlockFullVersion();
            break;
        case "ships":
            unlockPremiumShips();
            break;
        case "weapons":
            unlockWeaponPack();
            break;
    }
}

function unlockFullVersion() {
    player.maxSpeed = 8;
    // Unlock all ship types
    app.ShowPopup("🚀 Full version unlocked!");
}

function unlockPremiumShips() {
    // Add premium ship types to available models
    app.ShowPopup("🛸 Premium ships unlocked!");
}

function unlockWeaponPack() {
    // Unlock advanced weapons immediately
    app.ShowPopup("⚡ Advanced weapons unlocked!");
}

function isProductUnlocked(productKey) {
    return app.LoadText("sgvd_unlock_" + productKey) === "true";
}

function checkUnlocksOnStart() {
    if (isProductUnlocked("full")) {
        player.maxSpeed = 8;
    }
}

// ==================== EXIT SCREEN ====================

function showSGVDExitScreen() {
    if (isProductUnlocked("full")) {
        app.Exit();
        return;
    }
    
    if (!sgvdWallet) {
        app.Exit();
        return;
    }
    
    sgvdWallet.showExitPaymentScreen({
        message: "Thanks for playing SGVD!\n\n" +
                 "Support development with a coffee? ☕\n" +
                 "Or upgrade to Full Version!",
        onDismiss: function() {
            app.Exit();
        }
    });
}

// ==================== ENHANCED PAUSE MENU ====================

function showSGVDPauseMenu() {
    var layPause = app.CreateLayout("Linear", "VCenter,FillXY");
    layPause.SetBackgroundColor("#0a0a1a");
    
    var txtTitle = app.CreateText("PAUSED", 0.8, -1);
    txtTitle.SetTextSize(32);
    txtTitle.SetTextColor("#00FF00");
    layPause.AddChild(txtTitle);
    
    // Store button
    var btnStore = app.CreateButton("🛒 Store", 0.6, 0.1);
    btnStore.SetMargins(0, 0.02, 0, 0);
    btnStore.SetOnTouch(function() {
        dlgPause.Dismiss();
        showSGVDStore();
    });
    layPause.AddChild(btnStore);
    
    // Resume
    var btnResume = app.CreateButton("Resume", 0.6, 0.1);
    btnResume.SetMargins(0, 0.02, 0, 0);
    btnResume.SetOnTouch(function() {
        dlgPause.Dismiss();
        isRunning = true;
    });
    layPause.AddChild(btnResume);
    
    // Restart
    var btnRestart = app.CreateButton("Restart", 0.6, 0.1);
    btnRestart.SetMargins(0, 0.02, 0, 0);
    btnRestart.SetOnTouch(function() {
        dlgPause.Dismiss();
        restartGame();
    });
    layPause.AddChild(btnRestart);
    
    // Exit
    var btnExit = app.CreateButton("Exit", 0.6, 0.1);
    btnExit.SetMargins(0, 0.02, 0, 0);
    btnExit.SetOnTouch(function() {
        dlgPause.Dismiss();
        showSGVDExitScreen();
    });
    layPause.AddChild(btnExit);
    
    var dlgPause = app.CreateDialog("Game Paused");
    dlgPause.SetBackColor("#0a0a1a");
    dlgPause.AddLayout(layPause);
    dlgPause.Show();
    
    isRunning = false;
}

// Export
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        initSGVDPayments: initSGVDPayments,
        showSGVDStore: showSGVDStore,
        showSGVDPauseMenu: showSGVDPauseMenu,
        showSGVDExitScreen: showSGVDExitScreen,
        checkUnlocksOnStart: checkUnlocksOnStart,
        isProductUnlocked: isProductUnlocked,
        SGVD_PAYMENT_CONFIG: SGVD_PAYMENT_CONFIG
    };
}
