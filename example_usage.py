from net_model_translator.core.model_list import ModelList
from net_model_translator.core.translator import Translator
from net_model_translator.input_schemas.cdp_neighbors.ntc_templates import (
    CiscoIOS,
    CiscoNXOS,
)
from net_model_translator.models import mapping
from net_model_translator.core.core_model import CoreModel


# Example Pydantic models for NXOS and IOS
class NXOSCDPNeighborsModel(CoreModel):
    device_id: str
    local_interface: str
    port_id: str
    platform: str
    capabilities: str
    nxos_specific: str


class IOSCDPNeighborsModel(CoreModel):
    hostname: str
    ip_address: str
    local_port: str
    remote_port: str
    platform: str
    capabilities: str
    ios_specific: str


# Example raw data for NXOS and IOS
raw_nxos_data = [
    {
        "neighbor_name": f"NXOS_Device_{i}",
        "mgmt_address": f"192.168.1.{i}",
        "local_interface": f"Ethernet{i}/0/{i}",
        "neighbor_interface": f"Ethernet{i}/0/{i+1}",
        "port_id": f"Gig{i}/0/{i+1}",
        "platform": f"Cisco NXOS {i}",
        "capabilities": "Switch",
        "neighbor_description": f"NXOS Detail {i}",
    }
    for i in range(1, 11)
]

raw_ios_data = [
    {
        "neighbor_name": f"IOS_Device_{i}",
        "mgmt_address": f"192.168.1.{i}",
        "local_interface": f"Gig{i}/0/{i}",
        "neighbor_interface": f"Gig{i}/0/{i+1}",
        "platform": f"Cisco IOS {i}",
        "capabilities": "Router",
        "software_version": f"IOS Detail {i}",
        "ios_specific": f"IOS Specific Field {i}",
    }
    for i in range(1, 11)
]

# Translator usage with schema autodetection
nxos_translator = Translator(data_type="cdp_neighbors", raw_data=raw_nxos_data)
ios_translator = Translator(data_type="cdp_neighbors", raw_data=raw_ios_data)

nxos_models = nxos_translator.translate(raw_nxos_data)
ios_models = ios_translator.translate(raw_ios_data)

# Print the translated models using to_table
print("NXOS Models:")
print(nxos_models.to_table())

print("\nIOS Models:")
print(ios_models.to_table())

# Example usage of Translator with a custom input schema
custom_ios_translator = Translator(
    data_type="cisco_ios",
    model=IOSCDPNeighborsModel,
    raw_data=raw_ios_data,
    input_schema=CiscoIOS,
)

custom_ios_models = custom_ios_translator.translate()

print("\nCustom IOS Models:")
print(custom_ios_models.to_table())

# Example usage of calculating average capabilities length
print(
    "\nAverage capabilities length in NXOS Models:", nxos_models.average("capabilities")
)
print("Average capabilities length in IOS Models:", ios_models.average("capabilities"))
print(
    "Average capabilities length in Custom IOS Models:",
    custom_ios_models.average("capabilities"),
)

# Demonstrate exporting to JSON and YAML
print("\nNXOS Models in JSON:")
print(nxos_models.to_json())

print("\nIOS Models in YAML:")
print(ios_models.to_yaml())
