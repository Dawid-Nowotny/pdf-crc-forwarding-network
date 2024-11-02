from pydantic import BaseModel, field_validator

from src.constants import NODE_PORTS

class AdminNodeRequest(BaseModel):
    admin_node: str

    @field_validator("admin_node")
    def validate_node(cls, node: str) -> str:
        print(f"Walidacja węzła: {node}")
        if node not in NODE_PORTS:
            raise ValueError(f"Invalid node: {node}")
        return node