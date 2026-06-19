/**
 * BrainBridge.js - Connects N'og nog game to AOS Brain
 * WebSocket client that sends world state and receives brain decisions
 */

class BrainBridge {
    constructor(game) {
        this.game = game;
        this.ws = null;
        this.connected = false;
        this.reconnectInterval = 5000;
        this.bridgeUrl = 'ws://localhost:8765';
        this.brainAvatar = null;
        this.brainState = 'Initializing...';
        this.lastUpdateTime = 0;
        this.updateInterval = 200; // Send state to brain every 200ms
        
        // Avatar state
        this.avatar = {
            position: new THREE.Vector3(1000, 200, 1000),
            velocity: new THREE.Vector3(0, 0, 0),
            rotation: new THREE.Euler(0, 0, 0),
            health: 100,
            fuel: 100,
            target: null,
            action: 'idle',
            lastDecision: null
        };
    }
    
    connect() {
        try {
            console.log('Connecting to Brain Bridge...');
            this.ws = new WebSocket(this.bridgeUrl);
            
            this.ws.onopen = () => {
                console.log('Connected to Brain Bridge');
                this.connected = true;
                this.brainState = 'Connected';
                this.createBrainAvatar();
                this.startUpdateLoop();
            };
            
            this.ws.onmessage = (event) => {
                this.handleMessage(JSON.parse(event.data));
            };
            
            this.ws.onclose = () => {
                console.log('Brain Bridge disconnected');
                this.connected = false;
                this.brainState = 'Disconnected';
                setTimeout(() => this.connect(), this.reconnectInterval);
            };
            
            this.ws.onerror = (error) => {
                console.error('Brain Bridge error:', error);
                this.brainState = 'Error';
            };
            
        } catch (error) {
            console.error('Failed to connect to Brain Bridge:', error);
            setTimeout(() => this.connect(), this.reconnectInterval);
        }
    }
    
    handleMessage(data) {
        switch(data.type) {
            case 'brain_action':
                this.executeBrainAction(data.action);
                break;
            case 'brain_status':
                console.log('Brain status:', data.status);
                break;
            case 'pong':
                // Heartbeat response
                break;
            case 'error':
                console.error('Bridge error:', data.message);
                break;
        }
    }
    
    executeBrainAction(action) {
        this.avatar.action = action.type || 'idle';
        this.avatar.lastDecision = action;
        this.brainState = `Brain: ${action.brain_state || 'active'} | Action: ${this.avatar.action}`;
        
        // Apply thrust
        if (action.thrust !== undefined) {
            const maxThrust = 100;
            this.avatar.velocity.add(
                new THREE.Vector3(0, 0, -1)
                    .applyEuler(this.avatar.rotation)
                    .multiplyScalar(action.thrust * maxThrust * 0.01)
            );
        }
        
        // Apply rotation
        if (action.rotation) {
            this.avatar.rotation.x += action.rotation[0] * 0.02;
            this.avatar.rotation.y += action.rotation[1] * 0.02;
            this.avatar.rotation.z += action.rotation[2] * 0.02;
        }
        
        // Fire weapon
        if (action.fire && this.game.fireWeapon) {
            // Create brain avatar projectile
            this.fireBrainProjectile();
        }
        
        // Update target
        if (action.target) {
            this.avatar.target = action.target;
        }
    }
    
    fireBrainProjectile() {
        // Create projectile from avatar
        const geometry = new THREE.SphereGeometry(0.3, 8, 8);
        const material = new THREE.MeshBasicMaterial({ 
            color: 0xff00ff,  // Brain projectiles are magenta
            emissive: 0xff00ff,
            emissiveIntensity: 2
        });
        const mesh = new THREE.Mesh(geometry, material);
        
        const forward = new THREE.Vector3(0, 0, -1).applyEuler(this.avatar.rotation);
        mesh.position.copy(this.avatar.position).add(forward.clone().multiplyScalar(10));
        
        this.game.scene.add(mesh);
        
        // Add to projectiles
        if (!this.game.brainProjectiles) this.game.brainProjectiles = [];
        this.game.brainProjectiles.push({
            mesh: mesh,
            velocity: this.avatar.velocity.clone().add(forward.multiplyScalar(2000)),
            life: 2.0,
            owner: 'brain'
        });
    }
    
    createBrainAvatar() {
        // Create visual representation of brain
        const group = new THREE.Group();
        
        // Core - glowing brain-like structure
        const coreGeometry = new THREE.IcosahedronGeometry(3, 1);
        const coreMaterial = new THREE.MeshBasicMaterial({ 
            color: 0xff00ff,
            emissive: 0xff00ff,
            emissiveIntensity: 0.8,
            wireframe: true
        });
        const core = new THREE.Mesh(coreGeometry, coreMaterial);
        group.add(core);
        
        // Inner glow
        const glowGeometry = new THREE.SphereGeometry(2, 16, 16);
        const glowMaterial = new THREE.MeshBasicMaterial({
            color: 0xff00ff,
            transparent: true,
            opacity: 0.5
        });
        const glow = new THREE.Mesh(glowGeometry, glowMaterial);
        group.add(glow);
        
        // Orbiting particles (neural activity)
        for (let i = 0; i < 8; i++) {
            const particleGeometry = new THREE.SphereGeometry(0.3, 8, 8);
            const particleMaterial = new THREE.MeshBasicMaterial({
                color: 0x00ffff,
                emissive: 0x00ffff
            });
            const particle = new THREE.Mesh(particleGeometry, particleMaterial);
            particle.userData = {
                orbitRadius: 4 + Math.random() * 2,
                orbitSpeed: 0.5 + Math.random() * 0.5,
                orbitAngle: (i / 8) * Math.PI * 2,
                orbitAxis: new THREE.Vector3(
                    Math.random() - 0.5,
                    Math.random() - 0.5,
                    Math.random() - 0.5
                ).normalize()
            };
            group.add(particle);
        }
        
        // Status label
        this.createStatusLabel(group);
        
        group.position.copy(this.avatar.position);
        this.game.scene.add(group);
        this.brainAvatar = group;
        
        console.log('Brain Avatar created');
    }
    
    createStatusLabel(parent) {
        // Create canvas for text
        const canvas = document.createElement('canvas');
        canvas.width = 512;
        canvas.height = 64;
        const ctx = canvas.getContext('2d');
        
        // Draw text
        ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
        ctx.fillRect(0, 0, 512, 64);
        ctx.font = 'bold 24px Courier New';
        ctx.fillStyle = '#ff00ff';
        ctx.textAlign = 'center';
        ctx.fillText('Brain Initializing...', 256, 40);
        
        const texture = new THREE.CanvasTexture(canvas);
        const material = new THREE.SpriteMaterial({ map: texture });
        const sprite = new THREE.Sprite(material);
        sprite.scale.set(20, 2.5, 1);
        sprite.position.y = 6;
        
        parent.add(sprite);
        this.statusLabel = { canvas, ctx, texture, sprite };
    }
    
    updateStatusLabel() {
        if (!this.statusLabel) return;
        
        const { ctx, texture } = this.statusLabel;
        ctx.clearRect(0, 0, 512, 64);
        ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
        ctx.fillRect(0, 0, 512, 64);
        ctx.font = 'bold 20px Courier New';
        ctx.fillStyle = '#ff00ff';
        ctx.textAlign = 'center';
        
        const state = this.brainState.substring(0, 40);
        ctx.fillText(state, 256, 35);
        
        // Health bar
        ctx.fillStyle = 'rgba(100, 100, 100, 0.5)';
        ctx.fillRect(100, 50, 312, 10);
        ctx.fillStyle = this.avatar.health > 50 ? '#00ff00' : '#ff0000';
        ctx.fillRect(100, 50, 312 * (this.avatar.health / 100), 10);
        
        texture.needsUpdate = true;
    }
    
    startUpdateLoop() {
        const loop = () => {
            if (this.connected) {
                this.sendGameState();
            }
            this.updateAvatar();
            setTimeout(loop, this.updateInterval);
        };
        loop();
    }
    
    sendGameState() {
        if (!this.ws || this.ws.readyState !== WebSocket.OPEN) return;
        
        // Get player position from game
        const player = this.game.player;
        const nearby = this.getNearbyObjects();
        const threats = this.getThreats();
        
        const gameState = {
            type: 'game_state',
            state: {
                player_pos: player ? [player.position.x, player.position.y, player.position.z] : [0, 0, 0],
                player_vel: player ? [player.velocity.x, player.velocity.y, player.velocity.z] : [0, 0, 0],
                avatar_pos: [this.avatar.position.x, this.avatar.position.y, this.avatar.position.z],
                avatar_vel: [this.avatar.velocity.x, this.avatar.velocity.y, this.avatar.velocity.z],
                avatar_health: this.avatar.health,
                avatar_fuel: this.avatar.fuel,
                nearby: nearby,
                threats: threats,
                universe: this.game.currentUniverse ? this.game.currentUniverse.type : 'PRIME',
                system: this.game.currentSolarSystem ? this.game.currentSolarSystem.star.name : 'Unknown'
            }
        };
        
        this.ws.send(JSON.stringify(gameState));
    }
    
    getNearbyObjects() {
        // Find nearby planets, stars, etc.
        const nearby = [];
        const playerPos = this.game.player ? this.game.player.position : new THREE.Vector3();
        
        // Check for nearby planets
        if (this.game.currentSolarSystem) {
            this.game.currentSolarSystem.planets.forEach(planet => {
                const pos = new THREE.Vector3(
                    Math.cos(planet.angle) * planet.distance / 1e9,
                    0,
                    Math.sin(planet.angle) * planet.distance / 1e9
                );
                const dist = pos.distanceTo(playerPos);
                if (dist < 10000) {
                    nearby.push({
                        type: 'planet',
                        name: planet.name,
                        distance: dist,
                        position: [pos.x, pos.y, pos.z]
                    });
                }
            });
        }
        
        return nearby;
    }
    
    getThreats() {
        // Identify threats (could be expanded for enemies)
        const threats = [];
        
        // Player is always a potential interaction target
        if (this.game.player) {
            const dist = this.avatar.position.distanceTo(this.game.player.position);
            threats.push({
                type: 'player',
                distance: dist,
                hostility: dist < 500 ? 'close' : 'distant'
            });
        }
        
        return threats;
    }
    
    updateAvatar() {
        if (!this.brainAvatar) return;
        
        // Update physics
        const dt = 0.016; // Approximate delta time
        
        // Apply velocity
        this.avatar.position.add(this.avatar.velocity.clone().multiplyScalar(dt));
        
        // Apply drag
        this.avatar.velocity.multiplyScalar(0.99);
        
        // Update mesh position
        this.brainAvatar.position.copy(this.avatar.position);
        this.brainAvatar.rotation.x += 0.01;
        this.brainAvatar.rotation.y += 0.02;
        
        // Update orbiting particles
        this.brainAvatar.children.forEach(child => {
            if (child.userData && child.userData.orbitRadius) {
                const ud = child.userData;
                ud.orbitAngle += ud.orbitSpeed * dt;
                
                const axis = ud.orbitAxis;
                const radius = ud.orbitRadius;
                
                child.position.x = Math.cos(ud.orbitAngle) * radius * axis.x;
                child.position.y = Math.sin(ud.orbitAngle) * radius * axis.y;
                child.position.z = Math.cos(ud.orbitAngle * 0.7) * radius * axis.z;
            }
        });
        
        // Make status label face camera
        if (this.statusLabel && this.statusLabel.sprite) {
            this.statusLabel.sprite.lookAt(this.game.camera.position);
        }
        
        // Update label text
        this.updateStatusLabel();
    }
    
    disconnect() {
        if (this.ws) {
            this.ws.close();
        }
    }
}

// Export for use in game
if (typeof module !== 'undefined' && module.exports) {
    module.exports = BrainBridge;
}
