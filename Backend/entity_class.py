from dataclasses import dataclass
from typing import List, Optional

@dataclass
class HouseinfoData:
    unit_id: str
    furnishing: Optional[str] = None
    location: Optional[str] = None
    room_number: Optional[int] = None
    rental_area: Optional[float] = None
    housing_type: Optional[str] = None
    standard_rent: Optional[int] = None
    standard_management_fee: Optional[int] = None
    standard_deposit: Optional[int] = None
    remarks: Optional[str] = None
    listing_status: Optional[bool] = None

@dataclass
class ContractData:
    contract_id: str
    unit_id: str
    tenant_name: Optional[str] = None
    personal_id: Optional[str] = None
    address: Optional[str] = None
    phone_number: Optional[str] = None
    account_number: Optional[str] = None
    language: Optional[str] = None
    contract_start_date: Optional[str] = None
    move_in_date: Optional[str] = None
    contract_end_date: Optional[str] = None
    move_out_date: Optional[str] = None
    contract_rent: Optional[int] = None
    contract_management_fee: Optional[int] = None
    contract_deposit: Optional[int] = None
    down_payment: Optional[int] = None
    balance_payment: Optional[int] = None
    special_terms: Optional[str] = None
    contract_file: Optional[str] = None
    contract_remarks: Optional[str] = None
    move_out_return_account: Optional[str] = None
    move_out_deduction_amount: Optional[int] = None
    move_out_deduction_details: Optional[str] = None
    move_out_confirmation_file: Optional[str] = None
    move_out_remarks: Optional[str] = None

@dataclass
class BillData:
    bill_id: str
    contract_id: str
    bill_date: Optional[str] = None
    period_start_date: Optional[str] = None
    period_end_date: Optional[str] = None
    rent: Optional[int] = None
    management_fee: Optional[int] = None
    unpaid_amount: Optional[int] = None
    water_bill: Optional[int] = None
    electricity_bill: Optional[int] = None
    gas_bill: Optional[int] = None
    heating_bill: Optional[int] = None
    communication_bill: Optional[int] = None
    adjustment: Optional[str] = None
    bill_remarks: Optional[str] = None
    payment_method: Optional[str] = None
    payment_due_date: Optional[str] = None
    last_payment_date: Optional[str] = None
    paid_amount: Optional[int] = None
    payment_remarks: Optional[str] = None
    ai_comment: Optional[str] = None

@dataclass
class UtilUsageData:
    measurement_time: str
    unit_id: str
    utility_type: str
    measurement_value: Optional[float] = None

@dataclass
class ResidentData:
    resident_id: str
    contract_id: str
    name: Optional[str] = None
    family_relationship: Optional[str] = None
    phone_number: Optional[str] = None
    language: Optional[str] = None
    residency_status: Optional[bool] = None
    approval_status: Optional[bool] = None

@dataclass
class VehicleData:
    vehicle_number: str
    contract_id: str
    resident_id: str
    additional_phone_number: Optional[str] = None
    vehicle_type: Optional[str] = None
    parking_type: Optional[str] = None

@dataclass
class MembershipData:
    id: str
    password_hash: Optional[str] = None
    resident_id: Optional[str] = None
    authority: Optional[str] = None
    note: Optional[str] = None

@dataclass
class NoticeData:
    notice_id: str
    author_id: str
    content: Optional[str] = None
    notice_targets: Optional[str] = None
    created_date: Optional[str] = None
    last_modified_date: Optional[str] = None
    delivery_status: Optional[bool] = None
