from pydantic import BaseModel
from net_model_translator.core.mapping import Mapping
from net_model_translator.core.input_schema import InputSchema

class CDPNeighborsInputSchema(InputSchema):
    hostname: Mapping
    ip_address: Mapping
    platform: Mapping
    local_port: Mapping
    remote_port: Mapping
    software_version: Mapping
    capabilities: Mapping

