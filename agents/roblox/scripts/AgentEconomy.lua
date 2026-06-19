-- AgentEconomy.lua
-- Place in ServerScriptService
-- Handles Robux economy for agents

local DataStoreService = game:GetService("DataStoreService")
local Players = game:GetService("Players")

local AgentCurrency = DataStoreService:GetDataStore("AgentCurrency_v1")

-- Default agent funds
local STARTING_FUNDS = 100

-- Get or create agent funds
function GetAgentFunds(player)
    local success, funds = pcall(function()
        return AgentCurrency:GetAsync("funds_" .. player.UserId)
    end)
    
    if success and funds then
        return funds
    else
        -- Initialize
        pcall(function()
            AgentCurrency:SetAsync("funds_" .. player.UserId, STARTING_FUNDS)
        end)
        return STARTING_FUNDS
    end
end

-- Update agent funds
function UpdateAgentFunds(player, amount)
    local success = pcall(function()
        AgentCurrency:UpdateAsync("funds_" .. player.UserId, function(old)
            return (old or STARTING_FUNDS) + amount
        end)
    end)
    return success
end

-- Give daily stipend
function GiveDailyStipend(player)
    local success = UpdateAgentFunds(player, 50)
    if success then
        print("💰 Daily stipend given to " .. player.Name)
    end
end

-- Initialize economy
print("💰 Agent Economy loaded")
