# models/cdp_neighbors/model.py
from pydantic import BaseModel
from typing import Optional


class CDPNeighborsModel(BaseModel):
    hostname: Optional[str]
    ip_address: Optional[str]
    platform: Optional[str]
    local_port: Optional[str]
    remote_port: Optional[str]
    software_version: Optional[str]
    capabilities: Optional[str]
