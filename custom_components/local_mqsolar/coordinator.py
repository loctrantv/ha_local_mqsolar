from datetime import timedelta
import logging
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .api import MQSolarApiClient

_LOGGER = logging.getLogger(__name__)

class MQSolarCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, host):
        super().__init__(
            hass,
            _LOGGER,
            name="Mạnh Quân Solar Data",
            update_interval=timedelta(seconds=1),  # Update mỗi 1 giây
        )
        self.api = MQSolarApiClient(host, async_get_clientsession(hass))

    async def _async_update_data(self):
        try:
            return await self.api.fetch_data()
        except Exception as err:
            raise UpdateFailed(f"Update failed: {err}")
