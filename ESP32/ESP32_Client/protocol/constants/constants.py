"""
-
"""

# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622
from utils.enum import enum

MD4_Type = enum(NONE=0, LOWER_HALF=1, FULL=2)

PACKAGE_MESSAGE_TYPE = enum(
    ConnRequest=3000,
    ConnResponse=3010,
    ConnApprove=3020,
    VerRequest=3030,
    VerResponse=3040,
    StatusRequest=3050,
    StatusResponse=3060,
    DiscRequest=3070,
    DiscResponse=3080,
    SleepRequest=3090,
    SleepResponse=3100,
    RebootRequest=3110,
    RebootResponse=3120,
    Data=5000,
    DataUpload=6000,
)

DATA_MESSAGE_TYPE = enum(
    ShowOnLight=5001, ShowOffLight=5002, ShowBook=5003, ShowBooks=5004, LightMode=5020
)

DATA_LIGHT_MODUS = enum(On=1, Off=2, Auto=3)

DATA_UPLOAD_MESSAGE_TYPE = enum(
    DataUpStart=6001,
    DataUp=6002,
    DataConfirm=6003,
    DataUpCompleted=6004,
    DataUpError=6005,
    DataUpCancel=6006,
)

DATA_UPLOAD_ERROR = enum(ParseError=1, MD4Error=2, Unknown=10)

UPDATE_CONFIG_ERROR = enum(ParseError=1, MD4Error=2, Unknown=10)

DISC_REASON = enum(
    USERREQUEST=0,
    UNEXPECTEDTYPE=2,
    SEQNERROR=3,
    TIMEOUT=4,
    SERVICENOTALLOWED=5,
    INCOMPATIBLEVERSION=6,
    RETRFAILED=7,
    PROTOCOLERROR=8,
)

STATUS = enum(OFFLINE=0, RUNNING=1, ERROR=10, UNKOWN=20)
