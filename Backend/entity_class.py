from datetime import datetime
from dataclasses import dataclass, field, replace
from typing import Optional, Dict, Any

@dataclass
class HouseinfoData:
    UnitId: str  # 세대번호 (PK)
    Furnishing: Optional[str] = None  # 비품정보 (CSV - 비품명, 수량, 상태)
    Location: Optional[str] = None  # 소재지
    RoomNumber: Optional[int] = None  # 호실
    RentalArea: Optional[float] = None  # 임대면적
    HousingType: Optional[str] = None  # 주택유형
    StandardRent: Optional[int] = None  # 표준 임대료
    StandardManagementFee: Optional[int] = None  # 표준 관리비
    StandardDeposit: Optional[int] = None  # 표준 보증금
    Remarks: Optional[str] = None  # 비고
    ListingStatus: Optional[bool] = True  # 매물여부


@dataclass
class ContractData:
    ContractId: str  # 계약관리번호 (UUID, PK)
    UnitId: Optional[str] = None  # 세대번호 (FK - HouseinfoData.UnitId)
    TenantName: Optional[str] = None  # 임차인 성명
    PersonalId: Optional[str] = None  # 주민번호
    Address: Optional[str] = None  # 주소
    PhoneNumber: Optional[str] = None  # 전화번호
    AccountNumber: Optional[str] = None  # 계좌번호
    Language: Optional[str] = None  # 언어
    ContractStartDate: Optional[datetime] = None  # 계약 시작일
    MoveInDate: Optional[datetime] = None  # 입실일
    ContractEndDate: Optional[datetime] = None  # 계약 종료일
    MoveOutDate: Optional[datetime] = None  # 퇴실일
    ContractRent: Optional[int] = None  # 계약 임대료
    ContractManagementFee: Optional[int] = None  # 계약 관리비
    ContractDeposit: Optional[int] = None  # 계약 보증금
    DownPayment: Optional[int] = None  # 계약금
    BalancePayment: Optional[int] = None  # 잔금
    SpecialTerms: Optional[str] = None  # 특약사항
    ContractFile: Optional[str] = None  # 계약서 사본 (파일참조식별자)
    ContractRemarks: Optional[str] = None  # 계약비고
    MoveOutReturnAccount: Optional[str] = None  # 퇴실 반환 계좌번호
    MoveOutDeductionAmount: Optional[int] = None  # 퇴실 반환 공제액
    MoveOutDeductionDetails: Optional[str] = None  # 퇴실 반환 공제내역 (CSV - 내역, 금액)
    MoveOutConfirmationFile: Optional[str] = None  # 퇴실확인서 사본 (파일참조식별자)
    MoveOutRemarks: Optional[str] = None  # 퇴실비고

@dataclass
class BillData:
    BillId: str  # 청구관리번호 (UUID, PK)
    ContractId: Optional[str] = None  # 계약관리번호 (FK - ContractData.ContractId)
    BillDate: Optional[datetime] = None  # 청구일
    PeriodStartDate: Optional[datetime] = None  # 청구기간 시작일
    PeriodEndDate: Optional[datetime] = None  # 청구기간 종료일
    Rent: Optional[int] = None  # 임대료
    ManagementFee: Optional[int] = None  # 관리비
    UnpaidAmount: Optional[int] = None  # 미납금
    WaterBill: Optional[int] = None  # 수도청구액
    ElectricityBill: Optional[int] = None  # 전기청구액
    GasBill: Optional[int] = None  # 가스청구액
    HeatingBill: Optional[int] = None  # 난방청구액
    CommunicationBill: Optional[int] = None  # 통신청구액
    Adjustment: Optional[str] = None  # 가감액 (CSV - 내역, 금액)
    BillRemarks: Optional[str] = None  # 청구비고
    PaymentMethod: Optional[str] = None  # 납입 방식
    PaymentDueDate: Optional[datetime] = None  # 납입 기한
    LastPaymentDate: Optional[datetime] = None  # 마지막 납입 날짜
    PaidAmount: Optional[int] = None  # 납입액
    PaymentRemarks: Optional[str] = None  # 납입비고
    AIComment: Optional[str] = None  # AI 코멘트

@dataclass
class UtilUsageData:
    MeasurementTime: datetime  # 계량시각 (PK)
    UnitId: str  # 세대번호 (PK, FK - HouseinfoData.UnitId)
    UtilityType: str  # 계량대상 (PK)
    MeasurementValue: Optional[float] = None  # 계량값

@dataclass
class ResidentData:
    ResidentId: str  # 주민관리번호 (UUID, PK)
    ContractId: Optional[str] = None  # 계약관리번호 (FK - ContractData.ContractId)
    Name: Optional[str] = None  # 성명
    FamilyRelationship: Optional[str] = None  # 관계
    PhoneNumber: Optional[str] = None  # 전화번호
    Language: Optional[str] = None  # 언어
    ResidencyStatus: Optional[bool] = None  # 거주여부
    ApprovalStatus: Optional[bool] = None  # 승인상태

@dataclass
class VehicleData:
    VehicleNumber: str  # 차량번호 (PK)
    ContractId: Optional[str] = None  # 계약관리번호 (FK - ContractData.ContractId)
    ResidentId: Optional[str] = None  # 주민관리번호 (FK - ResidentData.ResidentId)
    AdditionalPhoneNumber: Optional[str] = None  # 추가전화번호
    VehicleType: Optional[str] = None  # 차종
    ParkingType: Optional[str] = None  # 주차구분 (상시 or 수시)

@dataclass
class MembershipData:
    ID: str  # ID (PK)
    PasswordHash: str  # PW (SHA-256)
    ResidentId: Optional[str] = None  # 주민관리번호 (FK - ResidentData.ResidentId)
    Authority: Optional[str] = None  # 권한
    Note: Optional[str] = None  # 비고

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        # 데이터 클래스를 생성하면서 딕셔너리 값을 반영
        return cls(**{f.name: data.get(f.name) for f in cls.__dataclass_fields__.values()})

@dataclass
class NoticeData:
    NoticeId: str  # 공지번호 (UUID, PK)
    AuthorId: Optional[str] = None  # 작성자 (FK - MembershipData.ID)
    Content: Optional[str] = None  # 내용
    NoticeTargets: Optional[str] = None  # 공지대상 (다중값 - ResidentData.ResidentId, VehicleData.VehicleNumber, ContractData.ContractId, 수동입력전화번호)
    CreatedDate: Optional[datetime] = None  # 최초작성일
    LastModifiedDate: Optional[datetime] = None  # 마지막수정일
    DeliveryStatus: Optional[bool] = None  # 발송상태


