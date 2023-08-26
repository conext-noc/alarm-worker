condition_onu_last_down_cause = ("Last down cause         : ", "Last up time")
condition_onu_last_down_time = ("Last down time          : ", "Last dying gasp time")
condition_onu_status = ("Run state               : ", "Config state")

port_summary = [
    {
        "name": "state",
        "start": -4,
        "end": -3,
        "header": ",onu_id,state,up_date,up_time,down_date,down_time,down_cause_1,down_cause_2,down_cause_3,down_cause_4,down_cause_5,down_cause_6,down_cause_7,down_cause_8",
    },
    {
        "name": "names",
        "start": -2,
        "end": -1,
        "header": ",onu_id,sn,device,distance,rx_tx_power,name1,name2,name3,name4,name5,name6,name7,name8,name9,name10,",
    },
]

condition_port_summary = (
    "------------------------------------------------------------------------------"
)

vp_count = {
    "1": {
        "vp_ttl": 0,
        "vp_active_cnt": 0,
        "vp_deactive_cnt": 0,
        "vp_los_cnt": 0,
        "vp_off_cnt": 0,
    },
    "2": {
        "vp_vnet": 0,
        "vp_inter": 0,
        "vp_public_ip": 0,
        "OZ_0": 0,
        "OZ_MAX": 0,
        "OZ_SKY": 0,
        "OZ_MAGICAL": 0,
        "OZ_NEXT": 0,
        "OZ_PLUS": 0,
        "OZ_DEDICADO": 0,
        "OZ_CONECTA": 0,
        "NA": 0,
    },
}


