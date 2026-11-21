local Players = game:GetService("Players")
local TweenService = game:GetService("TweenService")

local player = Players.LocalPlayer
local camera = workspace.CurrentCamera

local trigger = workspace:WaitForChild("CutsceneTrigger")
local camPoint = workspace:WaitForChild("CameraPoint")
local door = workspace:WaitForChild("Door")

local played = false

local function playCutscene()
	local humanoid = player.Character:WaitForChild("Humanoid")
	humanoid.WalkSpeed = 0

	camera.CameraType = Enum.CameraType.Scriptable

	local flyInfo = TweenInfo.new(2, Enum.EasingStyle.Sine)
	local flyGoal = { CFrame = CFrame.lookAt(camPoint.Position, door.Position) }
	local flyIn = TweenService:Create(camera, flyInfo, flyGoal)
	flyIn:Play()
	flyIn.Completed:Wait()

	local doorInfo = TweenInfo.new(1.5)
	local doorGoal = { Position = door.Position + Vector3.new(0, door.Size.Y, 0) }
	local openDoor = TweenService:Create(door, doorInfo, doorGoal)
	openDoor:Play()
	openDoor.Completed:Wait()
	task.wait(1)

	camera.CameraType = Enum.CameraType.Custom
	humanoid.WalkSpeed = 16
end

trigger.Touched:Connect(function(hit)
	if played then
		return
	end
	if hit.Parent == player.Character then
		played = true
		playCutscene()
	end
end)
