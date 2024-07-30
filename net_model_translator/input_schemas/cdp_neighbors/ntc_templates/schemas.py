from net_model_translator.core.mapping import Mapping
from net_model_translator.core.input_schema import InputSchema

from netutils.interface import abbreviated_interface_name


class CDPNeighborsInputSchema(InputSchema):
    hostname: Mapping = Mapping()
    ip_address: Mapping = Mapping()
    platform: Mapping = Mapping()
    local_port: Mapping = Mapping(transform=abbreviated_interface_name)
    remote_port: Mapping = Mapping(transform=abbreviated_interface_name)
    software_version: Mapping = Mapping()
    capabilities: Mapping = Mapping()
