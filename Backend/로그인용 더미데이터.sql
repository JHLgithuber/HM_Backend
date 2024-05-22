-- 1. 주민정보 테이블에 admin과 guest 더미 데이터 추가
INSERT INTO Resident_data (ResidentId, ContractId, Name, FamilyRelationship, PhoneNumber, Language, ResidencyStatus, ApprovalStatus)
VALUES ('admin_resident_id', NULL, 'admin', '관리자', '010-0000-0000', '한국어', TRUE, TRUE);

INSERT INTO Resident_data (ResidentId, ContractId, Name, FamilyRelationship, PhoneNumber, Language, ResidencyStatus, ApprovalStatus)
VALUES ('guest_resident_id', NULL, 'guest', '게스트', '010-0000-0001', '한국어', TRUE, TRUE);

-- 2. 회원정보 테이블에 admin과 guest 추가
INSERT INTO Membership_data (ID, PasswordHash, ResidentId, Authority, Note)
VALUES ('admin', 1234, 'admin_resident_id', 'Landlord', '관리자 계정');

INSERT INTO Membership_data (ID, PasswordHash, ResidentId, Authority, Note)
VALUES ('guest', 1234, 'guest_resident_id', 'Tenant', '게스트 계정');
