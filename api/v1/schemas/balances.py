from pydantic import BaseModel


class TopUpBalance(BaseModel):
    topped_up_balance: int
