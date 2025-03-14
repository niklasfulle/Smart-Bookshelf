local my_info ={
    version = "1.3.0",
    description = "Dissector to parse the (SBP-D) Smart Bookshelf Data Protocol.",
    repository = ""
}

set_plugin_info(my_info)

local p_sbp_d = Proto("sbp-d", "Smart Bookshelf Data Protocol")

-- sbp-d properties

local sbp_d_packet_length     = ProtoField.uint16("sbp_d.packet_length", "Paket länge")
local sbp_d_message_type     = ProtoField.uint8("sbp_d.message_type", "Protokoll Type", base.HEX, {
    [5001] = "ShowOnLight",
    [5002] = "ShowOffLight",
    [5003] = "ShowBook",
    [5004] = "ShowBooks",
    [5020] = "LightMode",
    [6001] = "DataUpSta",
    [6002] = "DataUp",
    [6003] = "DataUpCom",
    [6004] = "DataUpErr",
    [6005] = "DataUpCan",
})
local sbp_d_data                = ProtoField.new("Nutzdaten", "sbp.data", ftypes.BYTES)

p_sbp_d.fields = {
-- sbp packet
    sbp_d_packet_length,
    sbp_d_message_type,
    sbp_d_data
}

function p_sbp_d.dissector(buf, pktinfo, root)
    pktinfo.cols.protocol:set("SBP-D")

    local pktlen = buf:reported_length_remaining()
    local tree = root:add(p_sbp_d, buf:range(0, pktlen))
    local data_length = buf:range(0,2):le_uint() - 4

    -- sbp layer
    local msg_type = buf:range(2,2)
    local sbp_d = tree:add(p_sbp_d,  buf:range(0, 4 + data_length), "SBP-D Daten")

    sbp_d:add_le(sbp_d_packet_length,      buf:range(0, 2))
    sbp_d:add_le(sbp_d_message_type,        buf:range(2, 2))

    if (msg_type:le_uint() == 5003) then
        sbp_d:add_le(sbp_d_data, buf:range(4, data_length))
    elseif (msg_type:le_uint() == 5004) then
        sbp_d:add_le(sbp_d_data, buf:range(4, data_length))
    elseif (msg_type:le_uint() == 5020) then
        sbp_d:add_le(sbp_d_data, buf:range(4, data_length))
    elseif (msg_type:le_uint() == 6001) then
        sbp_d:add_le(sbp_d_data, buf:range(4, data_length))
    elseif (msg_type:le_uint() == 6002) then
        sbp_d:add_le(sbp_d_data, buf:range(4, data_length))
    elseif (msg_type:le_uint() == 6004) then
        sbp_d:add_le(sbp_d_data, buf:range(4, data_length))
    end

    return pktlen
end