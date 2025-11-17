from enum import Enum


class ProductTypeEnum(Enum):
    CONSUMABLE = "consumable"
    PERMANENT = "permanent"


class TransactionStatusEnum(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
