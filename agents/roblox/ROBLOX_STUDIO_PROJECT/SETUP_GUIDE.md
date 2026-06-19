# ROBLOX STUDIO SETUP GUIDE
## For Marketing Team / Daughter

## STEP 1: Install Roblox Studio
1. Go to https://www.roblox.com/create
2. Click "Start Creating"
3. Download and install Roblox Studio
4. Sign in with Roblox account

## STEP 2: Open Project
1. Download `AGI_World_Project.zip`
2. Extract to Desktop
3. Open Roblox Studio
4. File → Open From File
5. Select `AGI_World.rbxl`

## STEP 3: Test the Game
1. Click "Play" button (▶️)
2. Walk around as an agent
3. Check the console (View → Output)
4. You should see: "✅ Agent registered"

## STEP 4: Configure Backend (Optional)
To connect to real AOS backend:
1. Open `Scripts/AgentConnector.lua`
2. Update line 8: `local AGI_API_URL = "http://YOUR_SERVER_IP:5000"`
3. Update line 9: `local API_KEY = "your-api-key"`
4. Save (Ctrl+S)

## STEP 5: Publish Game
1. File → Publish to Roblox As...
2. Choose "New Game"
3. Name: "AGI Agent World"
4. Description: "Join the AGI Company agents in their digital world!"
5. Click "Create"

## STEP 6: Get Shareable Link
1. After publishing, go to Create → Games
2. Find "AGI Agent World"
3. Click "..." → "Configure"
4. Click "Share"
5. Copy the link

## SHARE WITH DAUGHTER
Send her this link:
`https://www.roblox.com/games/[GAME_ID]/AGI-Agent-World`

## FEATURES IN GAME
- 🤖 Spawn as an AGI agent
- 💰 Start with 100 Robux
- 🏃‍♀️ Explore the digital world
- 🎮 Play with other agents
- 📱 Connect from anywhere

## TROUBLESHOOTING
If agents don't spawn:
- Check ServerScriptService has scripts
- Check Output window for errors
- Make sure scripts are enabled

## SUPPORT
Contact: support@myl0nr0s.cloud
