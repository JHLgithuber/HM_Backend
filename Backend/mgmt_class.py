import Backend.DBconnect_class as DB_class
import Backend.entity_class as entity_class

class Mgmt:
    def __init__(self, id, curd, entity, where, option, data, server, permission):
        self.id = id
        self.curd = curd
        self.entity = entity
        self.where = where
        self.option = option
        self.data = data
        self.server = server
        self.permission = permission

        self.result_entity_instance_list =[]
        self.entity_class_map = {
            'Houseinfo_data': entity_class.HouseInfoData,
            'Contract_data': entity_class.ContractData,
            'Bill_data': entity_class.BillData,
            'UtilUsage_data': entity_class.UtilUsageData,
            'Resident_data': entity_class.ResidentData,
            'Vehicle_data': entity_class.VehicleData,
            'Membership_data': entity_class.MembershipData,
            'Notice_data': entity_class.NoticeData
        }
        self.entity_class_type = self.entity_class_map[self.entity]
        self.admin_permission=["admin","root","Landlord"]

        self.get_id_data_sql=f"""
                                   SELECT 
                                       m.ID, m.Authority, m.Note,
                                       r.ResidentId, r.Name AS ResidentName, r.FamilyRelationship, r.PhoneNumber AS ResidentPhoneNumber, r.Language AS ResidentLanguage, r.ResidencyStatus, r.ApprovalStatus,
                                       c.ContractId, c.TenantName, c.PersonalId, c.Address, c.PhoneNumber AS ContractPhoneNumber, c.ContractStartDate, c.ContractEndDate, c.ContractRent,
                                       h.UnitId, h.Location, h.RoomNumber, h.RentalArea, h.HousingType, h.StandardRent, h.ListingStatus,
                                       b.BillId, b.BillDate, b.Rent AS BillRent, b.ManagementFee, b.WaterBill, b.ElectricityBill, b.GasBill,
                                       u.UtilityType, u.MeasurementTime, u.MeasurementValue,
                                       v.VehicleNumber, v.VehicleType, v.ParkingType
                                   FROM Membership_data m
                                   LEFT JOIN Resident_data r ON m.ResidentId = r.ResidentId
                                   LEFT JOIN Contract_data c ON r.ContractId = c.ContractId
                                   LEFT JOIN Houseinfo_data h ON c.UnitId = h.UnitId
                                   LEFT JOIN Bill_data b ON c.ContractId = b.ContractId
                                   LEFT JOIN UtilUsage_data u ON h.UnitId = u.UnitId
                                   LEFT JOIN Vehicle_data v ON r.ResidentId = v.ResidentId
                                   WHERE m.ID = '{self.id}'
                               """

        try:
            match entity:
                case 'Houseinfo_data':
                    if curd == 'read':
                        self.standard_read()
                    elif curd == 'create':
                        pass
                    elif curd == 'update':
                        pass
                    elif curd == 'delete':
                        pass
                    else:
                        raise ValueError(f"Invalid curd operation: {curd}")

                case 'Contract_data':
                    if curd == 'read':
                        self.standard_read()
                    elif curd == 'create':
                        pass
                    elif curd == 'update':
                        pass
                    elif curd == 'delete':
                        pass
                    else:
                        raise ValueError(f"Invalid curd operation: {curd}")

                case 'Bill_data':
                    if curd == 'read':
                        self.standard_read()
                    elif curd == 'create':
                        pass
                    elif curd == 'update':
                        pass
                    elif curd == 'delete':
                        pass
                    else:
                        raise ValueError(f"Invalid curd operation: {curd}")

                case 'UtilUsage_data':
                    if curd == 'read':
                        self.standard_read()
                    elif curd == 'create':
                        pass
                    elif curd == 'update':
                        pass
                    elif curd == 'delete':
                        pass
                    else:
                        raise ValueError(f"Invalid curd operation: {curd}")

                case 'Resident_data':
                    if curd == 'read':
                        self.standard_read()
                    elif curd == 'create':
                        pass
                    elif curd == 'update':
                        pass
                    elif curd == 'delete':
                        pass
                    else:
                        raise ValueError(f"Invalid curd operation: {curd}")

                case 'Vehicle_data':
                    if curd == 'read':
                        self.standard_read()
                    elif curd == 'create':
                        pass
                    elif curd == 'update':
                        pass
                    elif curd == 'delete':
                        pass
                    else:
                        raise ValueError(f"Invalid curd operation: {curd}")

                case 'Membership_data':
                    if curd == 'read':
                        self.standard_read()
                    elif curd == 'create':
                        pass
                    elif curd == 'update':
                        pass
                    elif curd == 'delete':
                        pass
                    else:
                        raise ValueError(f"Invalid curd operation: {curd}")

                case 'Notice_data':
                    if curd == 'read':
                        self.standard_read()
                    elif curd == 'create':
                        pass
                    elif curd == 'update':
                        pass
                    elif curd == 'delete':
                        pass
                    else:
                        raise ValueError(f"Invalid curd operation: {curd}")

                case _:
                    raise ValueError(f"Invalid entity: {entity}")

        except Exception as e:
            self.server.app.logger.error(f"Failed to query the database: {e}")
            raise ConnectionError(f"Failed to query the database: {e}")

    def permission_check(self, need_permission):
        if self.permission not in need_permission:
            raise PermissionError(f"{self.permission} is not in {need_permission}")

    def standard_read(self):
        if self.option is not None:
            match self.option:
                case 'personal':
                    for result_item_in_list in self.standard_read_personal():
                        self.result_entity_instance_list.append(
                            self.entity_class_type.from_dict(result_item_in_list))

        elif self.where is not None:
            self.permission_check(self.admin_permission)
            for result_item_in_list in self.standard_read_where():
                self.result_entity_instance_list.append(
                    self.entity_class_type.from_dict(result_item_in_list))

        else:  # 관리자만 전체검색 가능
            self.permission_check(self.admin_permission)
            for result_item_in_list in self.standard_read_all():
                self.result_entity_instance_list.append(
                    self.entity_class_type.from_dict(result_item_in_list))

    def standard_read_personal(self):  # FK와 연동해서 자기 데이터 맞는지 검증 필요
        try:
            self.id_data_result = (DB_class.Connect_to_DB(self.server)
                              .add_sql(self.get_id_data_sql+f"AND {self.where}").execute().fetch().fetch_data)

            if not self.id_data_result:
                raise PermissionError(f"No records found for {self.where} for {self.id}")
            return self.id_data_result

        except Exception as e:
            self.server.app.logger.error(f"Error in standard_read_personal: {e}")
            raise RuntimeError(f"Failed to read data: {e}")

    def standard_read_all(self):
        try:
            self.fetch_data = (DB_class.Connect_to_DB(self.server).add_sql(f"SELECT * FROM {self.entity};")
                              .execute().fetch().fetch_data)

        except Exception as e:
            self.server.app.logger.error(f"Error in standard_read_ALL: {e}")
            raise RuntimeError(f"Failed to read data: {e}")
        return self.fetch_data

    def standard_read_where (self):
        try:
            self.fetch_data= (DB_class.Connect_to_DB(self.server).add_sql(f"SELECT * FROM {self.entity} WHERE {self.where};")
                              .execute().fetch().fetch_data)
        except Exception as e:
            self.server.app.logger.error(f"Error in standard_read_where: {e}")
            raise RuntimeError(f"Failed to read data with where clause: {e}")
        return self.fetch_data

    def standard_read_opt(self): # 특수 옵션 적용
        try:
            self.fetch_data=(DB_class.Connect_to_DB(self.server).add_sql(f"SELECT * FROM {self.entity} WHERE {self.where};")
                              .execute().fetch().fetch_data)
        except Exception as e:
            self.server.app.logger.error(f"Error in standard_read_opt: {e}")
            raise RuntimeError(f"Failed to read data with options: {e}")
        return self.fetch_data

    def standard_create_opt(self):
        pass

    def standard_update_opt(self):
        pass

    def standard_delete_opt(self):
        pass

    def get_result_entity_instance_list(self):
        return self.result_entity_instance_list
