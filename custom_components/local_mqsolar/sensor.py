from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.const import (
    UnitOfElectricPotential,
    UnitOfElectricCurrent,
    UnitOfPower,
    UnitOfEnergy,
    UnitOfTemperature,
)
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    data = coordinator.data
    
    entities = []
    
    device_id = data.get("_device_id", "unknown")
    device_type = data.get("_device_type", "MQSolar")
    
    device_info = {
        "identifiers": {(DOMAIN, device_id)},
        "name": f"MQ {device_type} {device_id}",
        "manufacturer": "Mạnh Quân",
        "model": device_type,
    }
    
    if "charger" in data:
        entities.extend([
            MQSolarSensor(coordinator, device_info, "pvVoltage", "PV Voltage", UnitOfElectricPotential.VOLT, SensorDeviceClass.VOLTAGE, "charger"),
            MQSolarSensor(coordinator, device_info, "pvCurrent", "PV Current", UnitOfElectricCurrent.AMPERE, SensorDeviceClass.CURRENT, "charger"),
            MQSolarSensor(coordinator, device_info, "batVoltage", "Battery Voltage", UnitOfElectricPotential.VOLT, SensorDeviceClass.VOLTAGE, "charger"),
            MQSolarSensor(coordinator, device_info, "batCurrent", "Battery Current", UnitOfElectricCurrent.AMPERE, SensorDeviceClass.CURRENT, "charger"),
            MQSolarSensor(coordinator, device_info, "chargingPower", "Charging Power", UnitOfPower.WATT, SensorDeviceClass.POWER, "charger"),
            MQSolarSensor(coordinator, device_info, "powerToday", "Energy Today", UnitOfEnergy.KILO_WATT_HOUR, SensorDeviceClass.ENERGY, "charger", SensorStateClass.TOTAL_INCREASING),
            MQSolarSensor(coordinator, device_info, "powerTotal", "Energy Total", UnitOfEnergy.KILO_WATT_HOUR, SensorDeviceClass.ENERGY, "charger", SensorStateClass.TOTAL),
            MQSolarSensor(coordinator, device_info, "temperature", "Temperature", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, "charger"),
            MQSolarTextSensor(coordinator, device_info, "statusText", "Status", "charger"),
        ])
    elif "inverter" in data:
        entities.extend([
            MQSolarSensor(coordinator, device_info, "dcVoltage", "DC Voltage", UnitOfElectricPotential.VOLT, SensorDeviceClass.VOLTAGE, "inverter"),
            MQSolarSensor(coordinator, device_info, "acVoltage", "AC Voltage", UnitOfElectricPotential.VOLT, SensorDeviceClass.VOLTAGE, "inverter"),
            MQSolarSensor(coordinator, device_info, "outputPower", "Output Power", UnitOfPower.WATT, SensorDeviceClass.POWER, "inverter"),
            MQSolarSensor(coordinator, device_info, "limiterPower", "Grid Power", UnitOfPower.WATT, SensorDeviceClass.POWER, "inverter"),
            MQSolarSensor(coordinator, device_info, "limiterToday", "Grid Today", UnitOfEnergy.KILO_WATT_HOUR, SensorDeviceClass.ENERGY, "inverter", SensorStateClass.TOTAL_INCREASING),
            MQSolarSensor(coordinator, device_info, "limiterTotal", "Grid Total", UnitOfEnergy.KILO_WATT_HOUR, SensorDeviceClass.ENERGY, "inverter", SensorStateClass.TOTAL),
            MQSolarSensor(coordinator, device_info, "temperature", "Temperature", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, "inverter"),
            MQSolarSensor(coordinator, device_info, "energyToday", "Energy Today", UnitOfEnergy.KILO_WATT_HOUR, SensorDeviceClass.ENERGY, "inverter", SensorStateClass.TOTAL_INCREASING),
            MQSolarSensor(coordinator, device_info, "energyTotal", "Energy Total", UnitOfEnergy.KILO_WATT_HOUR, SensorDeviceClass.ENERGY, "inverter", SensorStateClass.TOTAL),
            MQSolarTextSensor(coordinator, device_info, "statusText", "Status", "inverter"),
        ])
        
    async_add_entities(entities)

class MQSolarSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, device_info, key, name, unit, device_class, data_key, state_class=SensorStateClass.MEASUREMENT):
        super().__init__(coordinator)
        self._device_info = device_info
        self._key = key
        self._data_key = data_key
        
        self._attr_name = name
        self._attr_native_unit_of_measurement = unit
        self._attr_device_class = device_class
        self._attr_state_class = state_class
        # generate unique id
        base_id = list(device_info['identifiers'])[0][1]
        self._attr_unique_id = f"{base_id}_{key}"

    @property
    def device_info(self):
        return self._device_info

    @property
    def native_value(self):
        if self.coordinator.data and self.coordinator.data.get("hasData"):
            return self.coordinator.data.get(self._data_key, {}).get(self._key)
        return None

class MQSolarTextSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, device_info, key, name, data_key):
        super().__init__(coordinator)
        self._device_info = device_info
        self._key = key
        self._data_key = data_key
        
        self._attr_name = name
        
        base_id = list(device_info['identifiers'])[0][1]
        self._attr_unique_id = f"{base_id}_{key}"

    @property
    def device_info(self):
        return self._device_info

    @property
    def native_value(self):
        if self.coordinator.data and self.coordinator.data.get("hasData"):
            return self.coordinator.data.get(self._data_key, {}).get(self._key)
        return None
