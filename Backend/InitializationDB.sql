-- Database 생성
CREATE DATABASE HouseManager;
USE HouseManager;

-- 1. 주택정보 테이블
CREATE TABLE Houseinfo_data (
    UnitId VARCHAR(36) PRIMARY KEY, -- 세대번호 (PK)
    Furnishing TEXT, -- 비품정보 (CSV - 비품명, 수량, 상태)
    Location VARCHAR(255), -- 소재지
    RoomNumber INT, -- 호실
    RentalArea FLOAT, -- 임대면적
    HousingType VARCHAR(50), -- 주택유형
    StandardRent INT, -- 표준 임대료
    StandardManagementFee INT, -- 표준 관리비
    StandardDeposit INT, -- 표준 보증금
    Remarks TEXT, -- 비고
    ListingStatus BOOLEAN -- 매물여부
);

-- 2. 계약관리 테이블
CREATE TABLE Contract_data (
    ContractId VARCHAR(36) PRIMARY KEY, -- 계약관리번호 (UUID, PK)
    UnitId VARCHAR(36), -- 세대번호 (FK - Houseinfo_data.UnitId)
    TenantName VARCHAR(100), -- 임차인 성명
    PersonalId VARCHAR(20), -- 주민번호
    Address TEXT, -- 주소
    PhoneNumber VARCHAR(20), -- 전화번호
    AccountNumber VARCHAR(50), -- 계좌번호
    Language VARCHAR(20), -- 언어
    ContractStartDate DATE, -- 계약 시작일
    MoveInDate DATE, -- 입실일
    ContractEndDate DATE, -- 계약 종료일
    MoveOutDate DATE, -- 퇴실일
    ContractRent INT, -- 계약 임대료
    ContractManagementFee INT, -- 계약 관리비
    ContractDeposit INT, -- 계약 보증금
    DownPayment INT, -- 계약금
    BalancePayment INT, -- 잔금
    SpecialTerms TEXT, -- 특약사항
    ContractFile VARCHAR(255), -- 계약서 사본 (파일참조식별자)
    ContractRemarks TEXT, -- 계약비고
    MoveOutReturnAccount VARCHAR(50), -- 퇴실 반환 계좌번호
    MoveOutDeductionAmount INT, -- 퇴실 반환 공제액
    MoveOutDeductionDetails TEXT, -- 퇴실 반환 공제내역 (CSV - 내역, 금액)
    MoveOutConfirmationFile VARCHAR(255), -- 퇴실확인서 사본 (파일참조식별자)
    MoveOutRemarks TEXT, -- 퇴실비고
    FOREIGN KEY (UnitId) REFERENCES Houseinfo_data(UnitId)
);

-- 3. 청구서 테이블
CREATE TABLE Bill_data (
    BillId VARCHAR(36) PRIMARY KEY, -- 청구관리번호 (UUID, PK)
    ContractId VARCHAR(36), -- 계약관리번호 (FK - Contract_data.ContractId)
    BillDate DATE, -- 청구일
    PeriodStartDate DATE, -- 청구기간 시작일
    PeriodEndDate DATE, -- 청구기간 종료일
    Rent INT, -- 임대료
    ManagementFee INT, -- 관리비
    UnpaidAmount INT, -- 미납금
    WaterBill INT, -- 수도청구액
    ElectricityBill INT, -- 전기청구액
    GasBill INT, -- 가스청구액
    HeatingBill INT, -- 난방청구액
    CommunicationBill INT, -- 통신청구액
    Adjustment TEXT, -- 가감액 (CSV - 내역, 금액)
    BillRemarks TEXT, -- 청구비고
    PaymentMethod VARCHAR(50), -- 납입 방식
    PaymentDueDate DATE, -- 납입 기한
    LastPaymentDate DATE, -- 마지막 납입 날짜
    PaidAmount INT, -- 납입액
    PaymentRemarks TEXT, -- 납입비고
    AIComment TEXT, -- AI 코멘트
    FOREIGN KEY (ContractId) REFERENCES Contract_data(ContractId)
);

-- 4. 공과금 사용량정보 테이블
CREATE TABLE UtilUsage_data (
    MeasurementTime TIMESTAMP, -- 계량시각 (PK)
    UnitId VARCHAR(36), -- 세대번호 (PK, FK - Houseinfo_data.UnitId)
    UtilityType VARCHAR(50), -- 계량대상 (PK)
    MeasurementValue FLOAT, -- 계량값
    PRIMARY KEY (MeasurementTime, UnitId, UtilityType),
    FOREIGN KEY (UnitId) REFERENCES Houseinfo_data(UnitId)
);

-- 5. 주민정보 테이블
CREATE TABLE Resident_data (
    ResidentId VARCHAR(36) PRIMARY KEY, -- 주민관리번호 (UUID, PK)
    ContractId VARCHAR(36), -- 계약관리번호 (FK - Contract_data.ContractId)
    Name VARCHAR(100), -- 성명
    FamilyRelationship VARCHAR(50), -- 관계
    PhoneNumber VARCHAR(20), -- 전화번호
    Language VARCHAR(20), -- 언어
    ResidencyStatus BOOLEAN, -- 거주여부
    ApprovalStatus BOOLEAN, -- 승인상태
    FOREIGN KEY (ContractId) REFERENCES Contract_data(ContractId)
);

-- 6. 차량정보 테이블
CREATE TABLE Vehicle_data (
    VehicleNumber VARCHAR(20) PRIMARY KEY, -- 차량번호 (PK)
    ContractId VARCHAR(36), -- 계약관리번호 (FK - Contract_data.ContractId)
    ResidentId VARCHAR(36), -- 주민관리번호 (FK - Resident_data.ResidentId)
    AdditionalPhoneNumber VARCHAR(20), -- 추가전화번호
    VehicleType VARCHAR(50), -- 차종
    ParkingType VARCHAR(20), -- 주차구분 (상시 or 수시)
    FOREIGN KEY (ContractId) REFERENCES Contract_data(ContractId),
    FOREIGN KEY (ResidentId) REFERENCES Resident_data(ResidentId)
);

-- 7. 회원정보 테이블
CREATE TABLE Membership_data (
    ID VARCHAR(50) PRIMARY KEY, -- ID (PK)
    PasswordHash CHAR(64), -- PW (SHA-256)
    ResidentId VARCHAR(36), -- 주민관리번호 (FK - Resident_data.ResidentId)
    Authority BOOLEAN, -- 권한
    Note TEXT, -- 비고
    FOREIGN KEY (ResidentId) REFERENCES Resident_data(ResidentId)
);

-- 8. 공지문 테이블
CREATE TABLE Notice_data (
    NoticeId VARCHAR(36) PRIMARY KEY, -- 공지번호 (UUID, PK)
    AuthorId VARCHAR(50), -- 작성자 (FK - Membership_data.ID)
    Content TEXT, -- 내용
    NoticeTargets TEXT, -- 공지대상 (다중값 - Resident_data.ResidentId, Vehicle_data.VehicleNumber, Contract_data.ContractId, 수동입력전화번호)
    CreatedDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- 최초작성일
    LastModifiedDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, -- 마지막수정일
    DeliveryStatus BOOLEAN, -- 발송상태
    FOREIGN KEY (AuthorId) REFERENCES Membership_data(ID)
);
