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

        try:
            match entity:
                case 'Houseinfo_data':
                    if curd == 'read':
                        if where is not None:
                            for result_item_in_list in self.standard_read_where():
                                self.result_entity_instance_list.append(entity_class.HouseInfoData.from_dict(result_item_in_list))
                        else:
                            for result_item_in_list in self.standard_read_all():
                                self.result_entity_instance_list.append(entity_class.HouseInfoData.from_dict(result_item_in_list))

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
                        pass
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
                        pass
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
                        pass
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
                        pass
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
                        self.standard_read_all()
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
                        pass
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
                        pass
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
