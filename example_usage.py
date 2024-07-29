import sys
import os

# Add the project directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from net_model_translator import Translator, Mapping
from net_model_translator.schemas.cdp_neighbors.ntc_templates.cisco_ios import (
    CDPNeighborsInputSchema,
)
from net_model_translator.models.cdp_neighbors.model import CDPNeighborsModel
from netutils.interface import abbreviated_interface_name

# Define mappings
cdp_neighbors_input_schema = CDPNeighborsInputSchema(
    hostname=Mapping(source_key="destination_host", target_key="hostname"),
    ip_address=Mapping(source_key="management_ip", target_key="ip_address"),
    local_port=Mapping(
        source_key="local_port",
        target_key="local_port",
        transform=abbreviated_interface_name,
    ),
    remote_port=Mapping(
        source_key="remote_port",
        target_key="remote_port",
        transform=abbreviated_interface_name,
    ),
    platform=Mapping(source_key="platform", target_key="platform"),
    software_version=Mapping(
        source_key="software_version", target_key="software_version"
    ),
    capabilities=Mapping(source_key="capabilities", target_key="capabilities"),
)

# Sample raw data (parsed from device output)
raw_cdp_data = [
    {
        "destination_host": "DeviceA",
        "management_ip": "192.168.1.1",
        "platform": "Cisco IOS",
        "local_port": "GigabitEthernet0/1",
        "remote_port": "GigabitEthernet0/2",
        "software_version": "15.2(4)M6",
        "capabilities": "Router Switch",
    },
    # Add invalid data for testing
    {
        "destination_host": "DeviceB",
        "management_ip": "192.168.1.2",
        "platform": "Cisco IOS",
        # Missing required fields
    },
]

# Create a Translator instance for the given device type with custom schema mappers
translator = Translator(
    device_type="cisco_ios",
    input_schema=cdp_neighbors_input_schema,
    model=CDPNeighborsModel,
)

# Translate raw data to Pydantic models
cdp_models = translator.translate(raw_cdp_data)

# Output the converted models
print(cdp_models)
