import logging
import async_timeout

_LOGGER = logging.getLogger(__name__)

class MQSolarApiClient:
    def __init__(self, host, session):
        self.host = host
        self.session = session
        self.device_type = None
        self.device_id = None
        self.endpoint = None

    async def fetch_status(self):
        async with async_timeout.timeout(5):
            async with self.session.get(f"http://{self.host}/api/status") as resp:
                data = await resp.json()
                self.device_type = data.get("device_type", "Unknown")
                self.device_id = data.get("deviceId", "unknown_id")
                return data

    async def fetch_data(self):
        if not self.endpoint:
            # Phát hiện endpoint dựa trên api/status
            try:
                async with async_timeout.timeout(2):
                    async with self.session.get(f"http://{self.host}/api/status") as resp:
                        if resp.status == 200:
                            status_data = await resp.json()
                            self.device_type = status_data.get("device_type", "Unknown")
                            self.device_id = status_data.get("deviceId", "unknown_id")
            except Exception as e:
                _LOGGER.warning("Could not fetch /api/status: %s", e)
            
            # Thử sạc MPPT trước, nếu không được thì thử Inverter
            try:
                async with async_timeout.timeout(2):
                    async with self.session.get(f"http://{self.host}/api/charger/data") as resp:
                        if resp.status == 200:
                            self.endpoint = "/api/charger/data"
                        else:
                            self.endpoint = "/api/data"
            except Exception:
                self.endpoint = "/api/data"
                    
        async with async_timeout.timeout(5):
            async with self.session.get(f"http://{self.host}{self.endpoint}") as resp:
                data = await resp.json()
                # đính kèm device info cho setup
                data["_device_type"] = self.device_type 
                data["_device_id"] = self.device_id
                return data
