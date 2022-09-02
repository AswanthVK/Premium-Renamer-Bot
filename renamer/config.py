import os

class Config:
    ACTIVE_DOWNLOADS = {}
    API_ID = int(os.environ.get("API_ID", '6795023'))
    API_HASH = os.environ.get("API_HASH", '48eb04ae416967495ba9930f87d4f4da')
    PAID_BOT = os.environ.get("PAID_BOT", "YES")
    STRING_SESSION = os.environ.get("STRING_SESSION", "BQBnrw8AFqfuh25HzE4bIsID4lnXwMZ3t16uPyXR_3Gu5QB45BLM2CHhoDiUJMpQ4Azl88qH5-9BGN45xP8Cx-zRXgIVez7JXPCo-PEkWCAaWovW7BTvozfEH6ZsniSIoMty_BbIQBEQj7oCWBZWEoKbWhGuQc5hzfb5HLXF4yUXKt-zW3XKCFacO5KoaUCCq1nRH2O4WmwlYsr967nag9nFxasm_zKm4uZbX0oR9lh0OYEcpWLaXka4KS_c9SxSRSVmwGuCbTwCuDl_6jzdCeuo-lwPMP62o8SvomgsysHa2EecrhfKQbA5Kpu1ISN8KAyhWXZKobopebqiOTojqrald20fBQAAAABuVPm6AA")
    AUTH_USERS =  [int(i) for i in os.environ.get("AUTH_USERS", "1805398747").split(" ")]
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "5028427286:AAGggDShZZwX7lnfkeaH9i0FalwBBkh2cGU")
    DATABASE_URL = os.environ.get("DATABASE_URL", "mongodb+srv://dkbotz:786@cluster0.pczec.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    DOWNLOAD_LOCATION = "./DOWNLOADS"
    DB_CHANNEL_ID = -1001769216579
    RESTART_TIME = []
    TIME_GAP1 = {}
    TIME_GAP2 = {}
    timegap_message = {}
