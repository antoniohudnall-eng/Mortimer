// Chronospace Explorer - Payment Integration Module
// Integrates Paydify, Store Selector, and Wallet Display

// Load payment libraries
var PaydifyPayments = require("./lib/PaydifyPayments.js");
var StoreIntegration = require("./lib/StoreIntegration.js");
var WalletPaymentDisplay = require("./lib/WalletPaymentDisplay.js");

// Payment configuration
var PAYMENT_CONFIG = {
    // Paydify (Crypto payments)
    paydify: {
        apiKey: null, // Set your API key
        merchantId: null, // Set your merchant ID
        currency: "BTC",
        environment: "sandbox" // Change to "production" when live
    },
    
    // Payhip (Fiat payments)
    payhip: {
        apiKey: null, // Set your API key
        storeUrl: null, // e.g., "https://payhip.com/yourstore"
        productId: null // Your product ID
    },
    
    // Direct wallet (Simple BTC payments)
    wallet: {
        address: "bc1q...your...wallet...address", // Set your BTC address
        suggestedAmount: 0.001 // 0.001 BTC default
    },
    
    // Pricing
    pricing: {
        fullVersion: {
            usd: 4.99,
            btc: 0.00012
        },
        donation: {
            amounts: [0.0001, 0.001, 0.01] // BTC
        }
    }
};

// Initialize payment handlers
var paydify = null;
var store = null;
var walletDisplay = null;

function initPayments() {
    // Initialize Paydify if configured
    if (PAYMENT_CONFIG.paydify.apiKey) {
        paydify = new PaydifyPayments(PAYMENT_CONFIG.paydify);
    }
    
    // Initialize Store Integration
    store = new StoreIntegration({
        payhipApiKey: PAYMENT_CONFIG.payhip.apiKey,
        payhipStoreUrl: PAYMENT_CONFIG.payhip.storeUrl,
        paydifyApiKey: PAYMENT_CONFIG.paydify.apiKey,
        paydifyStoreUrl: null, // Set if you have Paydify store
        productId: PAYMENT_CONFIG.payhip.productId
    });
    
    // Initialize Wallet Display
    walletDisplay = new WalletPaymentDisplay({
        walletAddress: PAYMENT_CONFIG.wallet.address,
        suggestedAmount: PAYMENT_CONFIG.wallet.suggestedAmount,
        label: "Chronospace Explorer Support"
    });
}

// ==================== IN-GAME PAYMENT UI ====================

/**
 * Show payment options from pause menu
 */
function showPaymentMenu() {
    var layMenu = app.CreateLayout("Linear", "VCenter,FillXY");
    layMenu.SetBackgroundColor("#1a1a2e");
    
    var txtTitle = app.CreateText("⚡ Upgrade to Full Version", 0.9, -1);
    txtTitle.SetTextSize(24);
    txtTitle.SetTextColor("#FFD700");
    layMenu.AddChild(txtTitle);
    
    var txtDesc = app.CreateText(
        "Unlock all features:\n" +
        "• All 3 Chronal Levels\n" +
        "• Premium ship skins\n" +
        "• No ads\n" +
        "• Priority support",
        0.8, -1, "Multiline"
    );
    txtDesc.SetTextSize(14);
    txtDesc.SetTextColor("#FFFFFF");
    txtDesc.SetMargins(0, 0.02, 0, 0.03);
    layMenu.AddChild(txtDesc);
    
    // Price
    var txtPrice = app.CreateText(
        "$" + PAYMENT_CONFIG.pricing.fullVersion.usd + " or " +
        PAYMENT_CONFIG.pricing.fullVersion.btc + " BTC",
        0.8, -1
    );
    txtPrice.SetTextSize(20);
    txtPrice.SetTextColor("#00FF00");
    layMenu.AddChild(txtPrice);
    
    // Payment options
    var btnCrypto = app.CreateButton("💎 Pay with Crypto", 0.8, 0.1);
    btnCrypto.SetMargins(0, 0.03, 0, 0);
    btnCrypto.SetOnTouch(function() {
        showCryptoPaymentOptions();
    });
    layMenu.AddChild(btnCrypto);
    
    var btnCard = app.CreateButton("💳 Pay with Card", 0.8, 0.1);
    btnCard.SetMargins(0, 0.02, 0, 0);
    btnCard.SetOnTouch(function() {
        showCardPayment();
    });
    layMenu.AddChild(btnCard);
    
    var btnWallet = app.CreateButton("₿ Direct BTC Transfer", 0.8, 0.1);
    btnWallet.SetMargins(0, 0.02, 0, 0);
    btnWallet.SetOnTouch(function() {
        showDirectWalletPayment();
    });
    layMenu.AddChild(btnWallet);
    
    // Cancel
    var btnCancel = app.CreateButton("Continue Demo", 0.6, 0.08);
    btnCancel.SetMargins(0, 0.03, 0, 0);
    btnCancel.SetOnTouch(function() {
        dlgMenu.Dismiss();
    });
    layMenu.AddChild(btnCancel);
    
    var dlgMenu = app.CreateDialog("Upgrade");
    dlgMenu.SetBackColor("#1a1a2e");
    dlgMenu.AddLayout(layMenu);
    dlgMenu.Show();
}

/**
 * Show crypto payment options (Paydify)
 */
function showCryptoPaymentOptions() {
    if (!paydify) {
        app.ShowPopup("Crypto payments not configured. Use direct wallet instead.");
        showDirectWalletPayment();
        return;
    }
    
    paydify.createPayment({
        amount: PAYMENT_CONFIG.pricing.fullVersion.btc,
        description: "Chronospace Explorer Full Version",
        orderId: "CE-" + Date.now() + "-" + Math.random().toString(36).substr(2, 9)
    }, function(paymentData, error) {
        if (error) {
            app.ShowPopup("Payment creation failed: " + (error.message || "Unknown error"));
            return;
        }
        
        // Display payment UI
        var layPayment = app.CreateLayout("Linear", "VCenter,FillXY");
        layPayment.SetBackgroundColor("#1a1a2e");
        
        paydify.displayPaymentUI(paymentData, {
            layout: layPayment,
            onSuccess: function(data) {
                app.ShowPopup("✅ Payment confirmed! Full version unlocked!");
                unlockFullVersion();
                setTimeout(function() {
                    dlgPayment.Dismiss();
                }, 2000);
            },
            onFailure: function(data) {
                app.ShowPopup("❌ Payment failed or expired");
            }
        });
        
        var dlgPayment = app.CreateDialog("Complete Payment");
        dlgPayment.SetBackColor("#1a1a2e");
        dlgPayment.AddLayout(layPayment);
        dlgPayment.Show();
    });
}

/**
 * Show card payment (Payhip)
 */
function showCardPayment() {
    if (!PAYMENT_CONFIG.payhip.storeUrl) {
        app.ShowPopup("Card payments not configured");
        return;
    }
    
    store.openPayhipCheckout({
        useWebView: true
    });
}

/**
 * Show direct wallet payment
 */
function showDirectWalletPayment() {
    if (!walletDisplay) {
        app.ShowPopup("Wallet not configured");
        return;
    }
    
    walletDisplay.showExitPaymentScreen({
        amount: PAYMENT_CONFIG.pricing.fullVersion.btc,
        message: "Send exactly " + PAYMENT_CONFIG.pricing.fullVersion.btc + 
                 " BTC to unlock the full version instantly!",
        onDismiss: function() {
            // Continue with demo
        }
    });
}

// ==================== EXIT SCREEN PAYMENT ====================

/**
 * Show payment screen on game exit
 */
function showExitPaymentScreen() {
    if (!walletDisplay) {
        app.Exit();
        return;
    }
    
    // Check if already purchased
    if (store && store.hasPurchased()) {
        app.Exit();
        return;
    }
    
    walletDisplay.showExitPaymentScreen({
        message: "Thanks for playing Chronospace Explorer!\n\n" +
                 "Support development with a coffee? ☕",
        onDismiss: function() {
            app.Exit();
        }
    });
}

// ==================== UNLOCK MANAGEMENT ====================

function unlockFullVersion() {
    // Store unlock status
    app.SaveText("ce_full_version", "unlocked");
    app.SaveText("ce_unlock_date", new Date().toISOString());
    
    // Apply unlocks
    player.maxSpeed = 8; // Increased speed
    // Add more unlock effects here
    
    app.ShowPopup("🎉 Full version unlocked! Enjoy!");
}

function isFullVersion() {
    return app.LoadText("ce_full_version") === "unlocked";
}

function checkUnlockOnStart() {
    if (isFullVersion()) {
        // Apply full version settings
        player.maxSpeed = 8;
        app.ShowPopup("Welcome back! Full version active.");
    }
}

// ==================== PAUSE MENU INTEGRATION ====================

/**
 * Enhanced pause menu with payment option
 */
function showPauseMenu() {
    var layPause = app.CreateLayout("Linear", "VCenter,FillXY");
    layPause.SetBackgroundColor("#1a1a2e");
    
    var txtTitle = app.CreateText("PAUSED", 0.8, -1);
    txtTitle.SetTextSize(32);
    txtTitle.SetTextColor("#FFFFFF");
    layPause.AddChild(txtTitle);
    
    // Show upgrade button if not full version
    if (!isFullVersion()) {
        var btnUpgrade = app.CreateButton("⚡ Upgrade to Full ($" + 
            PAYMENT_CONFIG.pricing.fullVersion.usd + ")", 0.8, 0.1);
        btnUpgrade.SetTextColor("#FFD700");
        btnUpgrade.SetOnTouch(function() {
            dlgPause.Dismiss();
            showPaymentMenu();
        });
        layPause.AddChild(btnUpgrade);
    }
    
    var btnResume = app.CreateButton("Resume", 0.6, 0.1);
    btnResume.SetMargins(0, 0.02, 0, 0);
    btnResume.SetOnTouch(function() {
        dlgPause.Dismiss();
        isRunning = true;
    });
    layPause.AddChild(btnResume);
    
    var btnRestart = app.CreateButton("Restart", 0.6, 0.1);
    btnRestart.SetMargins(0, 0.02, 0, 0);
    btnRestart.SetOnTouch(function() {
        dlgPause.Dismiss();
        restartGame();
    });
    layPause.AddChild(btnRestart);
    
    var btnExit = app.CreateButton("Exit Game", 0.6, 0.1);
    btnExit.SetMargins(0, 0.02, 0, 0);
    btnExit.SetOnTouch(function() {
        dlgPause.Dismiss();
        showExitPaymentScreen();
    });
    layPause.AddChild(btnExit);
    
    var dlgPause = app.CreateDialog("Game Paused");
    dlgPause.SetBackColor("#1a1a2e");
    dlgPause.AddLayout(layPause);
    dlgPause.Show();
    
    isRunning = false;
}

// ==================== INITIALIZATION ====================

// Call this in OnStart()
function initPaymentSystem() {
    initPayments();
    checkUnlockOnStart();
}

// Export for use in main game
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        initPaymentSystem: initPaymentSystem,
        showPaymentMenu: showPaymentMenu,
        showExitPaymentScreen: showExitPaymentScreen,
        showPauseMenu: showPauseMenu,
        isFullVersion: isFullVersion,
        PAYMENT_CONFIG: PAYMENT_CONFIG
    };
}
