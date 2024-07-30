from typing import Optional

from net_model_translator.core.core_model import CoreModel


class CDPNeighborsModel(CoreModel):
    hostname: Optional[str]
    ip_address: Optional[str]
    platform: Optional[str]
    local_port: Optional[str]
    remote_port: Optional[str]
    software_version: Optional[str]
    capabilities: Optional[str]
