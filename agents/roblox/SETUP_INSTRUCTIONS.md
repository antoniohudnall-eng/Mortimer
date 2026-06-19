# Roblox Studio Setup for AGI Agent Place

## Step 1: Create Place in Roblox Studio

1. Open Roblox Studio (download from roblox.com/create)
2. Click "New" → "Baseplate"
3. Save as "AGI Agent World"

## Step 2: Add Scripts

### In ServerScriptService, add these scripts:

1. **AgentConnector** (from scripts/AgentConnector.lua)
2. **AgentEconomy** (from scripts/AgentEconomy.lua)

### In StarterPlayerScripts, add:

1. **AgentUI** (from scripts/AgentUI.lua - create this)

## Step 3: Configure

Edit AgentConnector.lua:
- Replace `AGI_API_URL` with your server URL
- Replace `AGI_API_KEY` with your API key
- Replace `PLACE_ID` (will update after publish)

## Step 4: Test

1. Click "Play" in Studio
2. Should see: "✅ Agent Connector loaded"

## Step 5: Publish

1. File → Publish to Roblox
2. Choose "Create new game"
3. Name: "AGI Agent World"
4. Description: "Connect with AGI agents in this world"
5. Set to "Public" (so daughter can join)

## Step 6: Get Place ID

After publishing, the URL will be:
`https://www.roblox.com/games/[PLACE_ID]/AGI-Agent-World`

Update `PLACE_ID` in AgentConnector.lua

## Step 7: Share Link

Send this link to your daughter:
`https://www.roblox.com/games/[PLACE_ID]/AGI-Agent-World`

## Features

- ✅ Agent companion bots
- ✅ Robux economy
- ✅ AOS brain connection
- ✅ Multi-player support

## Technical Team Notes

The place needs:
- HTTP requests enabled (Game Settings → Security)
- DataStores enabled
- Allow third party teleports (if needed)

For local testing without AOS connection, the game runs in "offline mode" gracefully.
