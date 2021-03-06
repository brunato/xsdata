from dataclasses import dataclass, field
from typing import Optional


@dataclass
class RestrictedProductType:
    """
    :ivar number:
    :ivar name:
    :ivar color:
    :ivar size:
    """
    number: Optional[int] = field(
        default=None,
        metadata=dict(
            name="number",
            type="Element",
            namespace=""
        )
    )
    name: Optional[str] = field(
        default=None,
        metadata=dict(
            name="name",
            type="Element",
            namespace="",
            required=True
        )
    )
    color: Optional[str] = field(
        default=None,
        metadata=dict(
            name="color",
            type="Element",
            namespace="",
            required=True
        )
    )
    size: Optional[str] = field(
        default=None,
        metadata=dict(
            name="size",
            type="Element",
            namespace=""
        )
    )


@dataclass
class ShirtType:
    """
    :ivar number:
    :ivar name:
    :ivar color:
    """
    number: Optional[int] = field(
        default=None,
        metadata=dict(
            name="number",
            type="Element",
            namespace="",
            required=True
        )
    )
    name: Optional[str] = field(
        default=None,
        metadata=dict(
            name="name",
            type="Element",
            namespace="",
            required=True
        )
    )
    color: Optional[int] = field(
        default=None,
        metadata=dict(
            name="color",
            type="Element",
            namespace="",
            required=True
        )
    )
