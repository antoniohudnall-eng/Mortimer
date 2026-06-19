/**
 * Platform.js - Platform Detection and Optimization
 * Detects device type and adjusts settings accordingly
 */

class PlatformDetector {
    constructor() {
        this.platform = this.detect();
        this.optimizeSettings();
    }
    
    detect() {
        const ua = navigator.userAgent;
        const platform = {
            // Device type
            mobile: /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(ua),
            tablet: /iPad|Android(?!.*Mobile)|Tablet/i.test(ua),
            desktop: false,
            
            // OS
            ios: /iPhone|iPad|iPod/i.test(ua),
            android: /Android/i.test(ua),
            windows: /Windows/i.test(ua),
            mac: /Macintosh|Mac OS X/i.test(ua),
            linux: /Linux/i.test(ua),
            
            // Browser
            chrome: /Chrome/i.test(ua) && !/Edge/i.test(ua),
            firefox: /Firefox/i.test(ua),
            safari: /Safari/i.test(ua) && !/Chrome/i.test(ua),
            edge: /Edge/i.test(ua),
            
            // Capabilities
            touch: 'ontouchstart' in window || navigator.maxTouchPoints > 0,
            webgl: !!window.WebGLRenderingContext,
            webgl2: !!window.WebGL2RenderingContext,
            webgpu: !!navigator.gpu,
            webxr: 'xr' in navigator,
            gamepad: !!navigator.getGamepads,
            
            // Screen
            screenWidth: window.screen.width,
            screenHeight: window.screen.height,
            devicePixelRatio: window.devicePixelRatio || 1,
            
            // Performance indicators
            memory: navigator.deviceMemory || 4,
            cores: navigator.hardwareConcurrency || 2,
            
            // Network
            connection: navigator.connection || navigator.mozConnection || navigator.webkitConnection,
            
            // Battery
            battery: null
        };
        
        platform.desktop = !platform.mobile && !platform.tablet;
        
        // Estimate performance tier
        platform.tier = this.calculateTier(platform);
        
        return platform;
    }
    
    calculateTier(platform) {
        let score = 0;
        
        // Memory (GB)
        if (platform.memory >= 8) score += 3;
        else if (platform.memory >= 4) score += 2;
        else score += 1;
        
        // CPU cores
        if (platform.cores >= 8) score += 3;
        else if (platform.cores >= 4) score += 2;
        else score += 1;
        
        // WebGL support
        if (platform.webgl2) score += 2;
        else if (platform.webgl) score += 1;
        
        // Desktop bonus
        if (platform.desktop) score += 1;
        
        // Mobile penalty (heat/throttling)
        if (platform.mobile) score -= 1;
        
        if (score >= 8) return 'high';
        if (score >= 5) return 'medium';
        return 'low';
    }
    
    optimizeSettings() {
        const p = this.platform;
        
        this.settings = {
            // Rendering
            pixelRatio: p.tier === 'high' ? Math.min(p.devicePixelRatio, 2) :
                       p.tier === 'medium' ? Math.min(p.devicePixelRatio, 1.5) : 1,
            antialias: p.tier !== 'low',
            shadows: p.tier === 'high',
            bloom: p.tier === 'high',
            particles: p.tier !== 'low',
            
            // Galaxy rendering
            starCount: p.tier === 'high' ? 10000 :
                      p.tier === 'medium' ? 5000 : 2000,
            nebulaQuality: p.tier === 'high' ? 2 : 1,
            galaxyDistance: p.tier === 'high' ? 1000 : 500,
            
            // Physics
            physicsSteps: p.tier === 'high' ? 60 : 30,
            gravityComplexity: p.tier === 'high' ? 'full' : 'simple',
            
            // Audio
            audioQuality: p.tier === 'high' ? 'high' : 'low',
            spatialAudio: p.tier === 'high',
            reverb: p.tier === 'high',
            
            // UI
            touchControls: p.touch,
            hudOpacity: p.mobile ? 0.9 : 0.8,
            fontSize: p.mobile ? 14 : 16,
            
            // Network
            updateRate: p.connection?.saveData ? 10 : 60,
            compression: p.connection?.saveData || p.connection?.effectiveType === '2g',
            
            // Save settings
            autoSaveInterval: 60,
            maxSaveSlots: p.memory >= 8 ? 10 : 5,
            
            // Controls
            mouseSensitivity: p.mobile ? 0.5 : 1.0,
            joystickDeadzone: 0.15,
            aimAssist: p.mobile ? 0.3 : 0,
            
            // Battery awareness
            batterySaveMode: false
        };
        
        // Check battery status
        if ('getBattery' in navigator) {
            navigator.getBattery().then(battery => {
                p.battery = battery;
                
                // Enable battery save mode if low
                if (battery.level < 0.2 && !battery.charging) {
                    this.enableBatterySave();
                }
                
                // Listen for changes
                battery.addEventListener('levelchange', () => {
                    if (battery.level < 0.2 && !battery.charging) {
                        this.enableBatterySave();
                    }
                });
            });
        }
        
        // Listen for network changes
        if (p.connection) {
            p.connection.addEventListener('change', () => {
                this.optimizeSettings();
            });
        }
    }
    
    enableBatterySave() {
        this.settings.batterySaveMode = true;
        this.settings.pixelRatio = 1;
        this.settings.shadows = false;
        this.settings.bloom = false;
        this.settings.particles = false;
        this.settings.starCount = 1000;
        this.settings.physicsSteps = 30;
        this.settings.updateRate = 30;
        
        console.log('[Platform] Battery save mode enabled');
    }
    
    getSettings() {
        return this.settings;
    }
    
    getPlatform() {
        return this.platform;
    }
    
    isMobile() {
        return this.platform.mobile;
    }
    
    isTouch() {
        return this.platform.touch;
    }
    
    getTier() {
        return this.platform.tier;
    }
    
    // Get optimal texture size
    getTextureSize(baseSize) {
        const multiplier = this.settings.pixelRatio;
        return Math.floor(baseSize * multiplier);
    }
    
    // Get optimal shadow map size
    getShadowMapSize() {
        if (!this.settings.shadows) return 0;
        return this.platform.tier === 'high' ? 2048 : 1024;
    }
    
    // Should we use instanced rendering?
    useInstancing() {
        return this.platform.tier !== 'low' && !!window.WebGL2RenderingContext;
    }
    
    // Get recommended max draw distance
    getMaxDrawDistance() {
        return this.platform.tier === 'high' ? 10000 :
               this.platform.tier === 'medium' ? 5000 : 2000;
    }
}

// Export
if (typeof module !== 'undefined' && module.exports) {
    module.exports = PlatformDetector;
}
