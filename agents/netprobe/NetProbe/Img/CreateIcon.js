// Img/CreateIcon.js — Run once in DroidScript to generate icon

function CreateIcon() {
    // Create 128x128 canvas
    var img = app.CreateImage(null, 0.3, 0.3);
    
    // Background - dark blue
    img.DrawRectangle(0, 0, 128, 128, "#161b22");
    
    // Satellite body (center circle)
    img.DrawCircle(64, 64, 18, "#58a6ff", 0, "#58a6ff");
    
    // Solar panel - left
    img.DrawRectangle(15, 55, 45, 73, "#238636");
    img.DrawLine(15, 64, 45, 64, "#3fb950", 1);
    
    // Solar panel - right
    img.DrawRectangle(83, 55, 113, 73, "#238636");
    img.DrawLine(83, 64, 113, 64, "#3fb950", 1);
    
    // Antenna
    img.DrawLine(64, 46, 64, 20, "#c9d1d9", 3);
    img.DrawCircle(64, 18, 5, "#c9d1d9", 0, "#c9d1d9");
    
    // Signal waves (arcs)
    img.SetLineWidth(2);
    img.SetPaintColor("#a371f7");
    // Note: DroidScript DrawArc syntax is different, using lines simulate
    for (var i = 0; i < 3; i++) {
        var r = 12 + (i * 5);
        img.DrawLine(64 + r * 0.7, 18 - r * 0.7, 64 + r, 18);
    }
    
    // Save icon
    img.Save("Img/Satellite.png");
    
    app.ShowPopup("✅ Satellite icon created: Img/Satellite.png");
}

CreateIcon();
