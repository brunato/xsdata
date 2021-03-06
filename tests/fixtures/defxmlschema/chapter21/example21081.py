from dataclasses import dataclass, field
from typing import Optional
from tests.fixtures.defxmlschema.chapter21.example21083 import (
    CustomerType,
)
from tests.fixtures.defxmlschema.chapter21.example21082 import (
    ItemsType,
)


@dataclass
class OrderType:
    """
    :ivar customer:
    :ivar items:
    """
    customer: Optional[CustomerType] = field(
        default=None,
        metadata=dict(
            name="customer",
            type="Element",
            namespace="http://datypic.com/all",
            required=True
        )
    )
    items: Optional[ItemsType] = field(
        default=None,
        metadata=dict(
            name="items",
            type="Element",
            namespace="http://datypic.com/all",
            required=True
        )
    )


@dataclass
class Order(OrderType):
    class Meta:
        name = "order"
        namespace = "http://datypic.com/all"
