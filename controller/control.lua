-- Full path or relative to BizHawk working directory
local input_file = "controller/input.txt"

-- Reads and parses commands from the file
function read_input_file()
    local inputs = {}

    local f = io.open(input_file, "r")
    if not f then
        return inputs
    end

    for line in f:lines() do
        local command = line:match("^%s*(.-)%s*$") -- trim whitespace
        if command ~= "" then
            local base, count = command:match("!(%a+)(%d*)") -- e.g., !up3 → "up", "3"
            count = tonumber(count) or 1
            count = math.min(count, 10) -- cap to prevent spam

            for i = 1, count do
                table.insert(inputs, base)
            end
        end
    end

    f:close()
    os.remove(input_file) -- clear after reading
    return inputs
end

-- Maps parsed commands to joypad input
function map_command_to_input(command)
    local map = {
        up = {Up=true},
        down = {Down=true},
        left = {Left=true},
        right = {Right=true},
        a = {A=true},
        b = {B=true},
        start = {Start=true},
        select = {Select=true}
    }

    return map[command]
end

-- Main loop: runs every frame
while true do
    local commands = read_input_file() -- ✅ avoid shadowing the function

    for _, cmd in ipairs(commands) do
        local joypad_input = map_command_to_input(cmd)
        if joypad_input then
            print("Executing: " .. cmd)
            joypad.set(1, joypad_input)
            emu.frameadvance() -- press held for 1 frame
        else
            print("Invalid command: " .. tostring(cmd))
        end
    end

    emu.frameadvance()
end
