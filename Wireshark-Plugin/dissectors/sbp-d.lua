local my_info ={
    version = "1.1.0",
    description = "Dissector to parse the (SBP-D) Smart Bookshelf Data Protocol.",
    repository = ""
}

set_plugin_info(info)

local p_sbp_d = Proto("sbp-d", "Smart Bookshelf Data Protocol")

-- sbp-d properties
