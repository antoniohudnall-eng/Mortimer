# N'og nog Deployment Guide

## Quick Deploy (via Browser Terminal)

Since SSH is broken, deploy via Hostinger's browser terminal:

### Deploy v1 (First Version)
```bash
cd /var/www/nog
mkdir -p versions/v1 versions/v2 versions/v3

# Download v1
curl -L -o versions/v1/index.html https://raw.githubusercontent.com/hcindus/AOS-Brain/49c9bd4/game/index.html

# Copy to root
cp versions/v1/index.html index.html
```

### Deploy v2 (Current Game)
```bash
cd /var/www/nog
# Download from current game folder
curl -L -o versions/v2/index.html https://raw.githubusercontent.com/hcindus/AOS-Brain/master/nognog/game/index.html

# Copy to root
cp versions/v2/index.html index.html
```

### Deploy v3 (Mobile-Optimized)
```bash
cd /var/www/nog

# Download v3 (has Platform.js + GalaxyGenerator.js)
curl -L -o versions/v3/index.html https://raw.githubusercontent.com/hcindus/AOS-Brain/master/nognog/v3/index.html
curl -L -o versions/v3/js/core/Platform.js https://raw.githubusercontent.com/hcindus/AOS-Brain/master/nognog/v3/js/core/Platform.js
curl -L -o versions/v3/js/universe/GalaxyGenerator.js https://raw.githubusercontent.com/hcindus/AOS-Brain/master/nognog/v3/js/universe/GalaxyGenerator.js

# Copy to root
cp versions/v3/index.html index.html
cp -r versions/v3/js js
```

## v3 Known Issues

**Missing GalaxyGenerator Class:**
v3 references `GalaxyGenerator` from Platform.js, but the class is not imported in index.html.

**Fix needed:**
Add to index.html before the game script:
```html
<script src="js/universe/GalaxyGenerator.js"></script>
<script src="js/core/Platform.js"></script>
```

## Files Structure

```
/var/www/nog/
├── index.html          # Current live version
├── versions/
│   ├── v1/
│   │   └── index.html  # First commit version
│   ├── v2/
│   │   └── index.html  # Current game version
│   └── v3/
│       ├── index.html  # Mobile optimized (needs fix)
│       └── js/
│           ├── core/
│           │   └── Platform.js
│           └── universe/
│               └── GalaxyGenerator.js
```

## URLs

- Live: http://myl0nr0s.cloud/nog
- Versions: http://myl0nr0s.cloud/nog/versions/v1/, /v2/, /v3/

## SSH Key Fix Needed

mortimer_private is corrupted (398 bytes). Need to:
1. Generate new SSH key pair in Hostinger panel
2. Download private key
3. Save to /root/.ssh/myl0nr0s_ed25519
4. Enable automatic deployments
