local input_file = "C:/Users/lilto/PokemonChatPlays/controller/input.txt"

function read_input_file()
    local inputs = {}

    local f = io.open(input_file, "r")
    if not f then
        return inputs
    end

    for line in f:lines() do
        local command = line:match("^%s*(.-)%s*$")
        if command ~= "" then
            local base, count = command:match("!(%a+)(%d*)")
            if base then
                base = string.lower(base)
                count = tonumber(count) or 1
                count = math.min(count, 10)

                for i = 1, count do
                    table.insert(inputs, base)
                end
            end
        end
    end

    f:close()
    os.remove(input_file)

    if #inputs > 0 then
        print("✅ Loaded commands from input.txt")
    end

    return inputs
end

function map_command_to_input(command)
    if type(command) ~= "string" then return nil end

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

while true do
    local commands = read_input_file()

    for _, cmd in ipairs(commands) do
        local joypad_input = map_command_to_input(cmd)

        if joypad_input and type(joypad_input) == "table" then
            print("Executing: " .. cmd)

            -- 🟢 Hold the input for 5 frames (1 step)
            local move_frames = 10
            for i = 1, move_frames do
                joypad.set(joypad_input)
                emu.frameadvance()
            end
        else
            print("⚠️ Skipping invalid command: " .. tostring(cmd))
        end
    end

    emu.frameadvance()
end
