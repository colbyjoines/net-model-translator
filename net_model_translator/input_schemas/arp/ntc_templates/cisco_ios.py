from net_model_translator.core.mapping import Mapping
from net_model_translator.core.input_schema import InputSchema


class ARPInputSchema(InputSchema):
    address: Mapping
    mac: Mapping
    interface: Mapping
