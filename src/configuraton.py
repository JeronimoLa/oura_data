from dotenv import dotenv_values

CONFIG = dotenv_values("src/.env")  
BASE_URL = "https://api.ouraring.com"
OURA_FIRST_DAY = "2024-12-27"
SANDBOX_RING_CONFIG_URL_SANDBOX = "/v2/sandbox/usercollection/ring_configuration"
SANDBOX_URL_PATTERN = r'\/v2\/sandbox\/usercollection\/[^\s/{}]+'
RING_CONFIG_URL = "/v2/usercollection/ring_configuration"
URL_PATTERN = r'\/v2\/usercollection\/[^\s/{}]+'
# OURA_FIRST_DAY = "2025-01-20"