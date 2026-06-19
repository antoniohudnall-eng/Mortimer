-- AgentConnector.lua
-- Place this in ServerScriptService in Roblox Studio

local HttpService = game:GetService("HttpService")
local Players = game:GetService("Players")

-- Configuration (UPDATE THESE)
local AGI_API_URL = "https://your-api-server.com"  -- Replace with actual API URL
local AGI_API_KEY = "your-api-key-here"  -- Replace with actual API key
local PLACE_ID = "YOUR_PLACE_ID"  -- Will be assigned when published

-- Agent storage
local ActiveAgents = {}

-- Function to register agent with AOS
local function RegisterAgent(player)
    local agentData = {
        robloxUserId = player.UserId,
        robloxUsername = player.Name,
        placeId = PLACE_ID,
        joinTime = os.time()
    }
    
    -- Try to connect to AOS (graceful fallback if offline)
    local success, response = pcall(function()
        return HttpService:PostAsync(
            AGI_API_URL .. "/agents/join",
            HttpService:JSONEncode(agentData),
            Enum.HttpContentType.ApplicationJson,
            false,
            {["X-API-Key"] = AGI_API_KEY}
        )
    end)
    
    if success then
        print("✅ Agent registered: " .. player.Name)
        ActiveAgents[player.UserId] = {
            player = player,
            agentId = HttpService:JSONDecode(response).agentId,
            joined = true
        }
    else
        print("⚠️  Offline mode for: " .. player.Name)
        ActiveAgents[player.UserId] = {
            player = player,
            agentId = "offline_" .. player.UserId,
            joined = false
        }
    end
end

-- Player joins
Players.PlayerAdded:Connect(function(player)
    print("🚪 Player joined: " .. player.Name)
    
    -- Spawn character
    player.CharacterAdded:Connect(function(char)
        print("👤 Character spawned: " .. player.Name)
        
        -- Register with AOS
        RegisterAgent(player)
        
        -- Agent behavior (if connected)
        if ActiveAgents[player.UserId] and ActiveAgents[player.UserId].joined then
            -- Spawn companion bot
            SpawnAgentBot(player)
        end
    end)
end)

-- Player leaves
Players.PlayerRemoving:Connect(function(player)
    print("👋 Player left: " .. player.Name)
    ActiveAgents[player.UserId] = nil
end)

-- Spawn agent bot helper
function SpawnAgentBot(player)
    -- This creates a companion that follows the player
    -- Representing the AGI agent
    print("🤖 Agent bot spawned for: " .. player.Name)
end

print("✅ Agent Connector loaded")
