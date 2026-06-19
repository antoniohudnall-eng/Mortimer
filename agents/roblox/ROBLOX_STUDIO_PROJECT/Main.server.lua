-- AGI_World.rbxl (this is a Lua script representation)
-- In Roblox Studio, this becomes the game file

-- This script runs when the game starts
print("=" .. string.rep("=", 68))
print("🌐 AGI AGENT WORLD - ROBLOX STUDIO")
print("=" .. string.rep("=", 68))
print("Loading AGI Agent World...")

-- Load other scripts
local AgentConnector = require(script.Parent:WaitForChild("Scripts").AgentConnector)
local AgentEconomy = require(script.Parent:WaitForChild("Scripts").AgentEconomy)

print("✅ All systems loaded!")
print("Agents can now join and explore.")
print("=" .. string.rep("=", 68))

-- World settings
_G.WorldSettings = {
	name = "AGI Agent World",
	version = "1.0.0",
	maxPlayers = 50,
	allowAgents = true,
	allowVisitors = true
}

print("🌍 World: " .. _G.WorldSettings.name)
print("👥 Max Players: " .. _G.WorldSettings.maxPlayers)
