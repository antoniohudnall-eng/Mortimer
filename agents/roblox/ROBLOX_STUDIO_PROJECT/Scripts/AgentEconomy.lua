-- AgentEconomy.lua
-- Place in ServerScriptService

local DataStoreService = game:GetService("DataStoreService")
local Players = game:GetService("Players")

-- Data stores
local agentCurrency = DataStoreService:GetDataStore("AgentCurrency_v1")
local agentInventory = DataStoreService:GetDataStore("AgentInventory_v1")

-- Configuration
local STARTING_ROBUX = 100
local DAILY_STIPEND = 50

-- Currency manager
local function getAgentFunds(player)
	local success, funds = pcall(function()
		return agentCurrency:GetAsync("funds_" .. player.UserId)
	end)
	
	if success and funds then
		return funds
	else
		-- Initialize
		pcall(function()
			agentCurrency:SetAsync("funds_" .. player.UserId, STARTING_ROBUX)
		end)
		return STARTING_ROBUX
	end
end

local function updateAgentFunds(player, amount)
	local success = pcall(function()
		agentCurrency:UpdateAsync("funds_" .. player.UserId, function(old)
			return (old or STARTING_ROBUX) + amount
		end)
	end)
	return success
end

-- Daily login bonus
local function giveDailyStipend(player)
	local success = updateAgentFunds(player, DAILY_STIPEND)
	if success then
		print("💰 Daily stipend given to " .. player.Name)
	end
end

-- Player joins
Players.PlayerAdded:Connect(function(player)
	-- Give starting funds
	local current = getAgentFunds(player)
	if current == STARTING_ROBUX then
		print("💰 New agent " .. player.Name .. " received " .. STARTING_ROBUX .. " Robux")
	else
		print("💰 Welcome back " .. player.Name .. "! Balance: " .. current)
	end
end)

-- Expose functions to other scripts
_G.AgentEconomy = {
	getFunds = getAgentFunds,
	updateFunds = updateAgentFunds,
	giveStipend = giveDailyStipend
}

print("💰 Agent Economy loaded")
