import Backend.DBconnect_class as DB_class

class mgmt:
    def __init__(self, id, CURD, entity, where, option, data, server, permission):
        self.id = id
        self.CURD = CURD
        self.entity = entity
        self.where = where
        self.option = option
        self.data = data
        self.server = server
        self.permission = permission

        try:
            match entity:
                case 'Houseinfo_data':
                    if CURD == 'read':
                        self.standard_read_ALL()
                    elif CURD == 'create':
                        pass
                    elif CURD == 'update':
                        pass
                    elif CURD == 'delete':
                        pass
                    else:
                        raise ValueError(f"Invalid CURD operation: {CURD}")

                case 'Contract_data':
                    if CURD == 'read':
                        pass
                    elif CURD == 'create':
                        pass
                    elif CURD == 'update':
                        pass
                    elif CURD == 'delete':
                        pass
                    else:
                        raise ValueError(f"Invalid CURD operation: {CURD}")

                case 'Bill_data':
                    if CURD == 'read':
                        pass
                    elif CURD == 'create':
                        pass
                    elif CURD == 'update':
                        pass
                    elif CURD == 'delete':
                        pass
                    else:
                        raise ValueError(f"Invalid CURD operation: {CURD}")

                case 'UtilUsage_data':
                    if CURD == 'read':
                        pass
                    elif CURD == 'create':
                        pass
                    elif CURD == 'update':
                        pass
                    elif CURD == 'delete':
                        pass
                    else:
                        raise ValueError(f"Invalid CURD operation: {CURD}")

                case 'Resident_data':
                    if CURD == 'read':
                        pass
                    elif CURD == 'create':
                        pass
                    elif CURD == 'update':
                        pass
                    elif CURD == 'delete':
                        pass
                    else:
                        raise ValueError(f"Invalid CURD operation: {CURD}")

                case 'Vehicle_data':
                    if CURD == 'read':
                        self.standard_read_ALL()
                    elif CURD == 'create':
                        pass
                    elif CURD == 'update':
                        pass
                    elif CURD == 'delete':
                        pass
                    else:
                        raise ValueError(f"Invalid CURD operation: {CURD}")

                case 'Membership_data':
                    if CURD == 'read':
                        pass
                    elif CURD == 'create':
                        pass
                    elif CURD == 'update':
                        pass
                    elif CURD == 'delete':
                        pass
                    else:
                        raise ValueError(f"Invalid CURD operation: {CURD}")

                case 'Notice_data':
                    if CURD == 'read':
                        pass
                    elif CURD == 'create':
                        pass
                    elif CURD == 'update':
                        pass
                    elif CURD == 'delete':
                        pass
                    else:
                        raise ValueError(f"Invalid CURD operation: {CURD}")

                case _:
                    raise ValueError(f"Invalid entity: {entity}")

        except Exception as e:
            self.server.app.logger.error(f"Failed to query the database: {e}")
            raise ConnectionError(f"Failed to query the database: {e}")

    def permission_check(self, need_permission):
        if self.permission not in need_permission:
            raise PermissionError(f"{self.permission} is not in {need_permission}")

    def standard_read_ALL(self):
        try:
            self.result = DB_class.Connect_to_DB(self.server).add_sql(f"SELECT * FROM {self.entity};").execute().fetch().fetch_data
        except Exception as e:
            self.server.app.logger.error(f"Error in standard_read_ALL: {e}")
            raise RuntimeError(f"Failed to read data: {e}")
        return self

    def standard_read_where(self):
        try:
            self.result = DB_class.Connect_to_DB(self.server).add_sql(f"SELECT * FROM {self.entity} WHERE {self.where};").execute().fetch().fetch_data
        except Exception as e:
            self.server.app.logger.error(f"Error in standard_read_where: {e}")
            raise RuntimeError(f"Failed to read data with where clause: {e}")
        return self

    def standard_read_opt(self): # 특수 옵션 적용
        try:
            self.result = DB_class.Connect_to_DB(self.server).add_sql(f"SELECT * FROM {self.entity};").execute().fetch().fetch_data
        except Exception as e:
            self.server.app.logger.error(f"Error in standard_read_opt: {e}")
            raise RuntimeError(f"Failed to read data with options: {e}")
        return self

    def standard_create_opt(self):
        pass

    def standard_update_opt(self):
        pass

    def standard_delete_opt(self):
        pass
