from datetime import datetime
from enum import Enum

from pydantic import BaseModel, EmailStr, Field


class Role(str, Enum):
    PROPRIETOR = 'PROPRIETOR'
    MSME = 'MSME'
    CA_FIRM = 'CA_FIRM'


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    role: Role
    organization_name: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: Role
    organization_name: str


class DocumentIngestionRequest(BaseModel):
    document_type: str
    source_name: str
    content: str


class TransactionInput(BaseModel):
    description: str
    amount: float
    counterparty_gstin: str | None = None


class GSTComputationRequest(BaseModel):
    transactions: list[TransactionInput]


class TDSComputationRequest(BaseModel):
    transactions: list[TransactionInput]


class RiskScoreRequest(BaseModel):
    turnover_gst: float
    turnover_itr: float
    presumptive_income_rate: float
    advance_tax_paid: float
    expected_advance_tax: float
    unsecured_loans: float
    missed_tds_count: int


class ReportResponse(BaseModel):
    generated_at: datetime
    report_type: str
    payload: dict
