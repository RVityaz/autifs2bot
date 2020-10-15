from AmizoneAPI import amizone_api
import config


amizone_api.login(config.amizone_id, config.amizone_password)
amizone_api.getTimeTable()
