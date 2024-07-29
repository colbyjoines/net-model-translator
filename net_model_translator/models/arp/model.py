from pydantic import BaseModel

class ARPModel(BaseModel):
    address: str
    mac: str
    interface: str

