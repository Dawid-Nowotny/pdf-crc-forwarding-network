from pydantic import BaseModel, field_validator

from src.constants import NODE_PORTS

class NodesRequest(BaseModel):
    admin_node: str
    target_node: str

    @field_validator("admin_node", "target_node")
    def validate_nodes(cls, node: str) -> str:
        if node not in NODE_PORTS:
            raise ValueError(f"Invalid node: {node}")
        return node

    @field_validator("target_node")
    def different_nodes(cls, target_node: str, admin_node: str) -> str:
        if admin_node is not None and admin_node == target_node:
            raise ValueError("Admin and target nodes must be different")
        return target_node