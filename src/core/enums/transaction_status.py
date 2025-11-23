from enum import Enum


class TransactionStatusEnum(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
