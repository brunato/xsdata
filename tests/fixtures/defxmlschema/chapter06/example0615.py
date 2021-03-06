from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Size:
    """
    :ivar value:
    """
    class Meta:
        name = "size"
        nillable = True

    value: Optional[int] = field(
        default=None,
        metadata=dict(
            name="value",
            type="Extension",
            required=True,
            nillable=True
        )
    )
