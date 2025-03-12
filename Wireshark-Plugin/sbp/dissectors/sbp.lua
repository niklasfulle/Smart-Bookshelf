local my_info ={
    version = "1.1.0",
    description = "Dissector to parse the (SBP) Smart Bookshelf Protocol.",
    repository = ""
}

set_plugin_info(my_info)

local MD4 = require("md4");
local Stream = require("stream");

local CRC_LENGTH = 0
local CRC_OPTION = nil

-- print("#######################")

local p_sbp = Proto("sbp", "RaSTA Smart Bookshelf Protokoll")

-- Register preferences --

local ALGO_MD4 = 0
local ALGO_BLAKE2 = 1
local ALGO_SIPHASH = 2

local algo_prefs = {
    {1, "MD4", ALGO_MD4},
    {2, "Blake2b", ALGO_BLAKE2},
    {3, "SIPHASH-2-4", ALGO_SIPHASH},
}

local CRC_NONE = 0
local CRC32_EE5B42FD = 1
local CRC32_1EDC6F41 = 2
local CRC16_1021 = 3
local CRC16_8005 = 4

local crc_type = {
    {1, "None (Option A)", CRC_NONE},
    {1, "CRC32, Poly=EE5B42FD (Option B)", CRC32_EE5B42FD},
    {1, "CRC32, Poly=1EDC6F41 (Option C)", CRC32_1EDC6F41},
    {1, "CRC16, Poly=1021(Option D)", CRC16_1021},
    {1, "CRC16, Poly=8005(Option E)", CRC16_8005},
}

-- safety code parameters
p_sbp.prefs.safety_code_header = Pref.statictext("----- Safety Code -----", "Configuration option for the safety code the send/retransmission layer")
p_sbp.prefs.safety_code_len = Pref.uint("Length", 8, "Length of the safety code in bytes")
p_sbp.prefs.safety_code_algo = Pref.enum("Safety Code Algorithm", ALGO_MD4, "Safety Code Algorithm", algo_prefs, false)
p_sbp.prefs.md4_a = Pref.string( "MD4 Initial A (hex)", "67452301", "Initial A value for MD4 safety code calculation as hex string")
p_sbp.prefs.md4_b = Pref.string( "MD4 Initial B (hex)", "efcdab89", "Initial B value for MD4 safety code calculation as hex string")
p_sbp.prefs.md4_c = Pref.string( "MD4 Initial C (hex)", "98badcfe", "Initial C value for MD4 safety code calculation as hex string")
p_sbp.prefs.md4_d = Pref.string( "MD4 Initial D (hex)", "10325476", "Initial D value for MD4 safety code calculation as hex string")
p_sbp.prefs.safety_key = Pref.uint( "Key", 1193046, "Key for the safety code when MD4 is not used")

-- CRC parameters
p_sbp.prefs.crc_header = Pref.statictext("----- CRC -----", "Configuration option for the redundancy layer CRC checksum")
p_sbp.prefs.crc_algo = Pref.enum("CRC Type", CRC_NONE, "CRC algorithm parameters", crc_type, false)


local vals_message_type = {
    [3000] = "Verbindungsanfrage",
    [3010] = "Verbindungsantwort",
    [3020] = "Verbindungszustimmung",
    [3030] = "Versionsanfrage",
    [3040] = "Versionsantwort",
    [3050] = "Statusanfrage",
    [3060] = "Statusantwort",
    [3070] = "Trennaufforderung",
    [3080] = "Trennantwort",
    [3090] = "Schlafaufforderung",
    [3100] = "Schlafantwort",
    [3110] = "Neustartaufforderung",
    [3120] = "Neustartantwort",
    [5000] = "Daten",
    [6000] = "Daten Hochladen"
}


local vals_disconnect_reason = {
    [0] = "user enquiry",
    [1] = "not in use",
    [2] = "received message type not expected for the current state",
    [3] = "error in the sequence number verification during connection establishment",
    [4] = "timeout for incoming messages",
    [5] = "service not allowed in this state",
    [6] = "error in the protocol version",
    [7] = "retransmission failed, requested sequence number not available",
    [8] = "error in the protocol sequence"
}

-- sbp properties
local sbp_message_length      = ProtoField.uint16("sbp.mlen", "Nachrichtenlänge")
local sbp_message_type        = ProtoField.uint16("sbp.type", "Nachrichtentyp", base.DEC, vals_message_type)
local sbp_dest_id             = ProtoField.uint32("sbp.dest_id", "Empfängerkennung")
local sbp_src_id              = ProtoField.uint32("sbp.src_id", "Absenderkennung")
local sbp_sequence_number     = ProtoField.uint32("sbp.sn", "Sequenznummer")
local sbp_c_sequence_number   = ProtoField.uint32("sbp.cs", "Bestätigte Sequenznummer")
local sbp_timestamp           = ProtoField.uint32("sbp.ts", "Zeitstempel")
local sbp_c_timestamp         = ProtoField.uint32("sbp.cts", "Bestätigter Zeitstempel")
local sbp_protocol_version    = ProtoField.string("sbp.protocol_version", "Protokollversion")
local sbp_config_version      = ProtoField.string("sbp.config_version", "Configversion")
local sbp_bookshelf_version   = ProtoField.string("sbp.bookshelf_version", "Bookshelfversion")
local sbp_data                = ProtoField.new("Nutzdaten", "sbp.data", ftypes.BYTES)
local sbp_safety_code         = ProtoField.new("Sicherheitscode", "sbp.safety_code", ftypes.BYTES)
local sbp_safety_code_valid   = ProtoField.new("Sicherheitscode gültig", "sbp.safety_code_valid", ftypes.BOOLEAN)


p_sbp.fields = {
-- sbp packet
    sbp_message_length,
    sbp_message_type,
    sbp_dest_id,
    sbp_src_id,
    sbp_sequence_number,
    sbp_c_sequence_number,
    sbp_timestamp,
    sbp_c_timestamp,
    sbp_protocol_version,
    sbp_config_version,
    sbp_bookshelf_version,
    sbp_data,
    sbp_safety_code,
    sbp_safety_code_valid
}

-- redundancy dissector
function p_sbp.dissector(buf, pktinfo, root)
    pktinfo.cols.protocol:set("SBP")

    local pktlen = buf:reported_length_remaining()
    local tree = root:add(p_sbp, buf:range(0, pktlen))
    local data_length = buf:range(0,2):le_uint() - 36
    -- print(pktlen)

    -- sbp layer
    local msg_type = buf:range(2,2)
    pktinfo.cols.info:append(" " .. get_sbp_type_short(msg_type:le_uint()))

    local spb = tree:add(p_sbp,  buf:range(0, 36 + data_length), "SBP Daten")

    sbp:add_le(sbp_message_length,      buf:range(0, 2))
    sbp:add_le(sbp_message_type,        buf:range(2, 2))
    sbp:add_le(sbp_dest_id,             buf:range(4, 4))
    sbp:add_le(sbp_src_id,              buf:range(8, 4))
    sbp:add_le(sbp_sequence_number,     buf:range(12, 4))
    sbp:add_le(sbp_c_sequence_number,   buf:range(16, 4))
    sbp:add_le(sbp_timestamp,           buf:range(20, 4))
    sbp:add_le(sbp_c_timestamp,         buf:range(24, 4))

    if (msg_type:le_uint() == 3040) then
        
        sbp:add_le(sbp_protocol_version, buf:range(28, 2))
        sbp:add_le(sbp_config_version, buf:range(30, 2))
        sbp:add_le(sbp_bookshelf_version, buf:range(32, 2))

    elseif (msg_type:le_uint() == 5000 or msg_type:le_uint() == 6000) then
        -- data and retransmitted data
        local payload = sbp:add_le(sbp_data, buf:range(28, data_length - p_sbp.prefs.safety_code_len))
        local pos = 36
        local max_pos = 36 + data_length - p_sbp.prefs.safety_code_len
        while  pos < max_pos do
            local msg_length = buf:range(pos,2):le_uint()
            payload:add_le(buf:range(pos+2, msg_length):string())
            pos = pos + 2 + msg_length
        end

        -- call sbp-d-dissector if possible
        if pcall(function () Dissector.get("sbp-d") end) then
            Dissector.get("sbp-d"):call(buf:range(28, data_length - p_sbp.prefs.safety_code_len):tvb(), pktinfo, root)
        end
    end

    -- check safety code
    if p_sbp.prefs.safety_code_algo == ALGO_MD4 then
        local safety_packet = buf:raw(8, pktlen - 8 - p_sbp.prefs.safety_code_len)
        local md4_a = tonumber(p_sbp.prefs.md4_a, 16)
        local md4_b = tonumber(p_sbp.prefs.md4_b, 16)
        local md4_c = tonumber(p_sbp.prefs.md4_c, 16)
        local md4_d = tonumber(p_sbp.prefs.md4_d, 16)
        local packet_md4 = MD4()
            .init(md4_a, md4_b, md4_c, md4_d)
            .update(Stream.fromString(safety_packet))
            .finish()
            .asHex()

        local expected_md4 = packet_md4:sub(0, p_sbp.prefs.safety_code_len * 2):lower()
        local actual_md4 = Stream.toHex(Stream.fromString(buf:raw(36 + data_length - 8, 8))):lower()

        local treeItm = sbp:add(safety_safety_code, buf:range(36 + data_length - 8, 8))

        if ( expected_md4 == actual_md4 ) then
          -- valid MD4
          valid_item = sbp:add(safety_safety_code_valid, buf:range(36 + data_length - 8, 8), true)
          valid_item:set_generated()
        else
          -- invalid MD4
          treeItm:add_expert_info(PI_CHECKSUM, PI_WARN, "Invalid Checksum, expected " .. expected_md4)

          valid_item = sbp:add(safety_safety_code_valid, buf:range(36 + data_length - 8, 8), false)
          valid_item:set_generated()
        end
    else
        -- blake2b and siphash-2-4 not supported
        sbp:add_expert_info(PI_CHECKSUM, PI_WARN, "Checksum algorithm not supported")
    end

    return pktlen
end

local function heuristic_checker(buffer, pinfo, tree)
    -- guard for length
    length = buffer:len()
    if length < 36 then return false end

    -- sbp message type
    local potential_msg_type = buffer(2,2):le_uint()

    if get_rasta_type_short(potential_msg_type) ~= "unknown type"
    then
        p_sbp.dissector(buffer, pinfo, tree)
        return true
    else return false end
end

p_sbp:register_heuristic("tcp", heuristic_checker)
p_sbp:register_heuristic("udp", heuristic_checker)


-- HELPER FUNCTION SECTION

function get_sbp_type_short(type)
    if      (type == 3000) then  return "ConnRequest"
    elseif  (type == 3010) then  return "ConnResponse"
    elseif  (type == 3020) then  return "ConnApprove"
    elseif  (type == 3030) then  return "VerRequest"
    elseif  (type == 3040) then  return "VerResponse"
    elseif  (type == 3050) then  return "StatusRequest"
    elseif  (type == 3060) then  return "StatusResponse"
    elseif  (type == 3070) then  return "DiscRequest"
    elseif  (type == 3080) then  return "DiscResponse"
    elseif  (type == 3090) then  return "SleepRequest"
    elseif  (type == 3100) then  return "SleepResponse"
    elseif  (type == 3110) then  return "RebootRequest"
    elseif  (type == 3120) then  return "RebootResponse"
    elseif  (type == 5000) then  return "Data"
    elseif  (type == 6000) then  return "DataUpload"
    else                         return "unknown type"
    end
end

function swap_endianness(num)
    local b0 = bit32.lshift(bit32.band(num, 0x000000ff), 24)
    local b1 = bit32.lshift(bit32.band(num, 0x0000ff00), 8)
    local b2 = bit32.rshift(bit32.band(num, 0x00ff0000), 8)
    local b3 = bit32.rshift(bit32.band(num, 0xff000000), 24)

    return bit32.bor(b0, b1, b2, b3)
end
