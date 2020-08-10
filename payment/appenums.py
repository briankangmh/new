from enum import Enum

class TxType(Enum):   # A subclass of Enum
    CR = "Credit"
    DB = "Debit"

class TxReason(Enum):   # A subclass of Enum
    ANSW = "Answer"
    CHAT = "Chat"
    ACHAT = "Achat"
    VCHAT = "Vchat"