from dotenv import dotenv_values

CONFIG = dotenv_values(".env")  
BASE_URL = "https://api.ouraring.com"
OURA_FIRST_DAY = "2024-12-27"
RING_CONFIG_URL = "/v2/sandbox/usercollection/ring_configuration"