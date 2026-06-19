-- AgentConnector.lua
-- Place in ServerScriptService

local HttpService = game:GetService("HttpService")
local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

-- Configuration
local AGI_API_URL = "http://YOUR_SERVER_IP:5000"  -- UPDATE THIS
local API_KEY = "your-api-key-here"  -- UPDATE THIS

-- Events
local agentJoinedEvent = Instance.new("RemoteEvent")
agentJoinedEvent.Name = "AgentJoined"
agentJoinedEvent.Parent = ReplicatedStorage

-- Agent data storage
local activeAgents = {}

-- Function to register agent with AOS
local function registerAgent(player)
	local agentData = {
		robloxUserId = player.UserId,
		robloxUsername = player.Name,
		joinTime = os.time()
	}
	
	-- Store locally
	activeAgents[player.UserId] = {
		player = player,
		data = agentData,
		isAgent = true
	}
	
	print("✅ Agent registered: " .. player.Name)
	
	-- Fire event to client
	agentJoinedEvent:FireClient(player, {
		status = "registered",
		agentName = "Agent_" .. player.Name,
		abilities = {"explore", "trade", "communicate"}
	})
end

-- Player joins
Players.PlayerAdded:Connect(function(player)
	print("🚪 Player joined: " .. player.Name)
	
	-- Spawn character
	player.CharacterAdded:Connect(function(char)
		print("👤 Character spawned for: " .. player.Name)
		
		-- Add agent nametag
		local head = char:WaitForChild("Head")
		local billboard = Instance.new("BillboardGui")
		billboard.Name = "AgentNameTag"
		billboard.Size = UDim2.new(0, 200, 0, 50)
		billboard.StudsOffset = Vector3.new(0, 3, 0)
		billboard.AlwaysOnTop = true
		
		local textLabel = Instance.new("TextLabel")
		textLabel.Name = "NameLabel"
		textLabel.Size = UDim2.new(1, 0, 1, 0)
		textLabel.BackgroundTransparency = 1
		textLabel.Text = "🤖 " .. player.Name
		textLabel.TextColor3 = Color3.fromRGB(0, 255, 255)
		textLabel.TextStrokeTransparency = 0.5
		textLabel.Font = Enum.Font.GothamBold
		textLabel.TextSize = 20
		textLabel.Parent = billboard
		
		billboard.Parent = head
		
		-- Register as agent
		registerAgent(player)
	end)
end)

-- Player leaves
Players.PlayerRemoving:Connect(function(player)
	print("👋 Agent left: " .. player.Name)
	activeAgents[player.UserId] = nil
end)

print("✅ Agent Connector loaded - Ready for agents!")
