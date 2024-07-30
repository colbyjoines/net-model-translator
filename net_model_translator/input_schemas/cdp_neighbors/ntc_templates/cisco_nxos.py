from netutils.interface import abbreviated_interface_name

from net_model_translator.core.mapping import Mapping
from .schemas import CDPNeighborsInputSchema


class CiscoNXOS(CDPNeighborsInputSchema):
    hostname: Mapping = Mapping(source_key="neighbor_name")
    ip_address: Mapping = Mapping(source_key="mgmt_address")
    local_port: Mapping = Mapping(
        source_key="local_interface",
        transform=abbreviated_interface_name,
    )
    remote_port: Mapping = Mapping(
        source_key="neighbor_interface",
        transform=abbreviated_interface_name,
    )
    software_version: Mapping = Mapping(source_key="neighbor_description")
