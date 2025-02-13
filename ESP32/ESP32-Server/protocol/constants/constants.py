"""
    -
"""
# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,C0103
from utils.enum import enum

PACKAGE_MESSAGE_TYPE = enum(
    ConnRequest=3000,
    ConnResponse=3010,
    ConnApprove=3020,
    VerRequest=3030,
    VerResponse=3040,
    StatusRequest=3050,
    StatusResponse=3060,
    DiscRequest=3070,
    SleepRequest=3080,
    RebootRequest=3090,
    Data=5000,
    DataUpload=6000
)

DATA_MESSAGE_TYPE = enum(
    ShowOnLight=5001,
    ShowOffLight=5002,
    ShowBook=5003,
    ShowBooks=5004,
    LightMode=5020
)

DATA_LIGHT_MODUS = enum(
    
)

DATA_UPLOAD_MESSAGE_TYPE = enum(
    DataUpStart=6001,
    DataUp=6002,
    DataUpCompleted=6003,
    DataUpError=6004,
    DataUpCancel=6005
)

DATA_UPLOAD_ERROR = enum(
    
)