// Milk Man Game
// DroidScript Game Engine
// Project 5912 - AOCROS
// Art + Music + Comedy + Code

// Called when application is started.
function OnStart() {
    // Create a layout with objects vertically centered.
    lay = app.CreateLayout("Linear", "VCenter,FillXY");
    
    // Create a canvas for the game.
    canvas = app.CreateCanvas(320, 480);  // 320x480 for retro resolution.
    lay.AddChild(canvas);
    
    // Add layout to app.
    app.AddLayout(lay);
    
    // Game variables.
    player = { 
        x: 50, y: 400, 
        width: 20, height: 30, 
        speed: 5, 
        jumpPower: 15, vy: 0, 
        health: 100,
        sprite: 'milkman_idle'
    };
    projectiles = [];
    enemies = [];
    bosses = [];
    level = 1;
    gravity = 0.5;
    gameOver = false;
    
    // Initialize level 1 enemies (Boy Scouts).
    for(var i = 0; i < 5; i++) { 
        enemies.push({ 
            x: 350 + i*50, y: 400, 
            width: 20, height: 20, 
            speed: 2, 
            type: "scout", 
            health: 20,
            sprite: 'scout_walk'
        }); 
    }
    
    // Start game loop (30 FPS).
    app.SetInterval(GameLoop, 1000/30);
    
    // Add touch controls for movement and actions.
    canvas.SetOnTouchDown(OnTouchDown);
    canvas.SetOnTouchUp(OnTouchUp);
    
    // Play chiptune music if available.
    // app.PlayMusic("intro_theme.mp3");
}

// Game loop: Update and draw game state.
function GameLoop() { 
    if(gameOver) return; 
    
    UpdatePlayer();
    
    // Update player physics.
    player.vy += gravity; 
    player.y += player.vy; 
    if(player.y > 400) { 
        player.y = 400; 
        player.vy = 0; 
        player.sprite = 'milkman_idle';
    }
    
    // Update enemies.
    for(var i = enemies.length-1; i >= 0; i--) { 
        var e = enemies[i]; 
        e.x -= e.speed; // Move left.
        
        if(e.x < -e.width) enemies.splice(i, 1); // Remove off-screen.
        
        // Check player-enemy collision.
        if(Collision(player, e)) { 
            player.health -= 10; 
            enemies.splice(i, 1); 
            if(player.health <= 0) EndGame(); 
        } 
    }
    
    // Update projectiles (milk sprays).
    for(var i = projectiles.length-1; i >= 0; i--) { 
        var p = projectiles[i]; 
        p.x += p.vx; 
        if(p.x > 320 || p.x < 0) projectiles.splice(i, 1); 
        
        // Check projectile-enemy collision.
        for(var j = enemies.length-1; j >= 0; j--) { 
            if(Collision(p, enemies[j])) { 
                enemies[j].health -= 10; 
                if(enemies[j].health <= 0) enemies.splice(j, 1); 
                projectiles.splice(i, 1); 
                break; 
            } 
        } 
    }
    
    // Update bosses.
    for(var i = bosses.length-1; i >= 0; i--) { 
        var b = bosses[i]; 
        b.x += b.speed; 
        if(b.x < 200 || b.x > 300) b.speed = -b.speed; // Boss pacing.
        
        // Boss attacks (Vil Laine throws lactose-free bottles).
        if(Math.random() < 0.02) {
            enemies.push({ 
                x: b.x, y: b.y, 
                width: 10, height: 10, 
                speed: 3, 
                type: "bottle", 
                health: 10 
            }); 
        }
        
        // Check player-boss collision.
        if(Collision(player, b)) { 
            player.health -= 20; 
            if(player.health <= 0) EndGame(); 
        } 
        
        // Check projectile-boss collision.
        for(var j = projectiles.length-1; j >= 0; j--) { 
            if(Collision(projectiles[j], b)) { 
                b.health -= 10; 
                projectiles.splice(j, 1); 
                if(b.health <= 0) { 
                    bosses.splice(i, 1); 
                    NextLevel(); 
                } 
            } 
        } 
    }
    
    // Draw everything.
    DrawGame();
}

// Draw game.
function DrawGame() {
    canvas.Clear();
    
    // Draw background (Dairyopolis streets).
    canvas.SetPaintColor("#87CEEB"); // Sky blue.
    canvas.DrawRectangle(0, 0, 320, 480);
    canvas.SetPaintColor("#FFD700"); // Golden ground.
    canvas.DrawRectangle(0, 400, 320, 80);
    
    // Draw player (Milk Man as white rectangle with MM emblem).
    canvas.SetPaintColor("#FFFFFF");
    canvas.DrawRectangle(player.x, player.y, player.width, player.height);
    canvas.SetPaintColor("#000000");
    canvas.DrawText("MM", player.x+5, player.y+20);
    
    // Draw enemies.
    for(var i = 0; i < enemies.length; i++) { 
        if(enemies[i].type == "scout") 
            canvas.SetPaintColor("#228B22"); // Green for Boy Scouts.
        else 
            canvas.SetPaintColor("#FF4500"); // Orange for bottles.
        canvas.DrawRectangle(enemies[i].x, enemies[i].y, enemies[i].width, enemies[i].height);
    }
    
    // Draw projectiles (milk sprays as small white circles).
    canvas.SetPaintColor("#FFFFFF");
    for(var i = 0; i < projectiles.length; i++) { 
        canvas.DrawCircle(projectiles[i].x, projectiles[i].y, 5);
    }
    
    // Draw bosses.
    for(var i = 0; i < bosses.length; i++) { 
        canvas.SetPaintColor(bosses[i].type == "villaine" ? "#800080" : "#FF69B4"); // Purple for Vil Laine, pink for Madame Shoezete.
        canvas.DrawRectangle(bosses[i].x, bosses[i].y, bosses[i].width, bosses[i].height);
        canvas.SetPaintColor("#000000");
        canvas.DrawText(bosses[i].type == "villaine" ? "VL" : "MS", bosses[i].x+10, bosses[i].y+30);
    }
    
    // Draw health bar.
    canvas.SetPaintColor("#FF0000");
    canvas.DrawRectangle(10, 10, player.health, 10);
    
    // Draw level indicator.
    canvas.SetPaintColor("#000000");
    canvas.DrawText("Level: " + level, 10, 40);
    
    canvas.Refresh();
}

// Collision detection.
function Collision(obj1, obj2) { 
    return obj1.x < obj2.x + obj2.width && 
           obj1.x + obj1.width > obj2.x && 
           obj1.y < obj2.y + obj2.height && 
           obj1.y + obj1.height > obj2.y; 
}

// Handle touch input.
var touchLeft = false, touchRight = false, touchJump = false, touchShoot = false; 

function OnTouchDown(e) { 
    if(e.y > 400) {
        if(e.x < 160) touchLeft = true;
        else touchRight = true;
    } else if(e.x < 160) touchJump = true; 
    else touchShoot = true; 
}

function OnTouchUp(e) { 
    if(e.y > 400) {
        if(e.x < 160) touchLeft = false; 
        else touchRight = false; 
    } else if(e.x < 160) touchJump = false; 
    else touchShoot = false; 
}

// Update player movement based on touch.
function UpdatePlayer() { 
    if(touchLeft) {
        player.x -= player.speed;
        player.sprite = 'milkman_walk';
    }
    if(touchRight) {
        player.x += player.speed;
        player.sprite = 'milkman_walk';
    }
    if(touchJump && player.y == 400) {
        player.vy = -player.jumpPower;
        player.sprite = 'milkman_jump';
        app.PlaySound("jump");
    }
    if(touchShoot) {
        projectiles.push({ 
            x: player.x + player.width, y: player.y + 10,
            vx: 10, width: 10, height: 10 
        });
        app.PlaySound("splash");
    }
    if(player.x < 0) player.x = 0; 
    if(player.x > 320 - player.width) player.x = 320 - player.width;
}

// Advance to next level.
function NextLevel() { 
    level++; 
    enemies = []; 
    bosses = []; 
    
    if(level == 2) {
        // Level 2: Vil Laine's Lair - Add children throwing bottles.
        for(var i = 0; i < 5; i++) { 
            enemies.push({ 
                x: 350 + i*50, y: 400, 
                width: 15, height: 25, 
                speed: 3, 
                type: "bottle", 
                health: 15 
            }); 
        }
        bosses.push({ 
            x: 250, y: 350, 
            width: 30, height: 40, 
            speed: 2, 
            type: "villaine", 
            health: 100,
            sprite: 'villaine_idle'
        });
    } else if(level == 3) {
        // Level 3: Madame Shoezete's Fortress.
        for(var i = 0; i < 3; i++) { 
            enemies.push({ 
                x: 350 + i*70, y: 400, 
                width: 15, height: 25, 
                speed: 4, 
                type: "bottle", 
                health: 15 
            }); 
        }
        bosses.push({ 
            x: 250, y: 350, 
            width: 30, height: 40, 
            speed: 3, 
            type: "shoezete", 
            health: 150,
            sprite: 'shoezete_idle'
        });
    } else { 
        GameComplete(); // Game complete.
    } 
}

// End game.
function EndGame() { 
    gameOver = true; 
    canvas.Clear(); 
    canvas.SetPaintColor("#000000");
    canvas.DrawText("GAME OVER", 100, 220);
    canvas.DrawText("Score: " + (level * 100), 100, 250);
    canvas.Refresh();
    app.PlaySound("gameover");
}

// Game complete (victory).
function GameComplete() {
    gameOver = true;
    canvas.Clear();
    canvas.SetPaintColor("#000000");
    canvas.DrawText("VICTORY!", 110, 220);
    canvas.DrawText("Dairyopolis is saved!", 60, 250);
    canvas.Refresh();
    app.PlaySound("victory");
}

// Reset game.
function ResetGame() {
    gameOver = false;
    player.health = 100;
    player.x = 50;
    player.y = 400;
    level = 1;
    enemies = [];
    bosses = [];
    projectiles = [];
    
    // Re-initialize level 1.
    for(var i = 0; i < 5; i++) { 
        enemies.push({ 
            x: 350 + i*50, y: 400, 
            width: 20, height: 20, 
            speed: 2, 
            type: "scout", 
            health: 20 
        }); 
    }
}
