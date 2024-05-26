import Backend.DBconnect_class as DB_class

class mgmt:
    def __init__(self,id,CURD,entity,where,option,data,server,permission):
        self.id=id
        self.CURD=CURD
        self.entity=entity
        self.where=where
        self.option=option
        self.data=data
        self.server=server
        self.permission=permission
        
        match entity:
            case 'Houseinfo_data':                
                if CURD=='read':
                    self.standard_read_ALL()
                elif CURD=='create':
                    pass
                elif CURD=='update':
                    pass
                elif CURD=='delete':
                    pass
                else:
                    raise ValueError

            case 'Contract_data':
                if CURD=='read':
                    pass
                elif CURD=='create':
                    pass
                elif CURD=='update':
                    pass
                elif CURD=='delete':
                    pass
                else:
                    raise ValueError
                
            case 'Bill_data':
                if CURD=='read':
                    pass
                elif CURD=='create':
                    pass
                elif CURD=='update':
                    pass
                elif CURD=='delete':
                    pass
                else:
                    raise ValueError
                
            case 'UtilUsage_data':
                if CURD=='read':
                    pass
                elif CURD=='create':
                    pass
                elif CURD=='update':
                    pass
                elif CURD=='delete':
                    pass
                else:
                    raise ValueError
                
            case 'Resident_data':
                if CURD=='read':
                    pass
                elif CURD=='create':
                    pass
                elif CURD=='update':
                    pass
                elif CURD=='delete':
                    pass
                else:
                    raise ValueError
                
            case 'Vehicle_data':
                if CURD=='read':
                    self.standard_read_ALL()
                elif CURD=='create':
                    pass
                elif CURD=='update':
                    pass
                elif CURD=='delete':
                    pass
                else:
                    raise ValueError
                
            case 'Membership_data':
                if CURD=='read':
                    pass
                elif CURD=='create':
                    pass
                elif CURD=='update':
                    pass
                elif CURD=='delete':
                    pass
                else:
                    raise ValueError
                
            case 'Notice_data':
                if CURD=='read':
                    pass
                elif CURD=='create':
                    pass
                elif CURD=='update':
                    pass
                elif CURD=='delete':
                    pass
                else:
                    raise ValueError
    
    def permission_check(self,need_permission):
        if self.permission not in need_permission:
            raise PermissionError(f"{self.permission}is not in {need_permission}")
    
    def standard_read_ALL(self):
        self.result=DB_class.Connect_to_DB(self.server).add_sql(f"SELECT * FROM {self.entity};").execute().fetch().fetch_data
        return self
    
    def standard_read_where(self):
        pass
        self.result=DB_class.Connect_to_DB(self.server).add_sql(f"SELECT * FROM {self.entity} WHERE {self.where};").execute().fetch().fetch_data

    def standard_read_opt(self): #특수옵션적용
        self.result=DB_class.Connect_to_DB(self.server).add_sql(f"SELECT * FROM {self.entity};").execute().fetch().fetch_data
        return self


    def standard_create_opt(self):
        pass
    def standard_update_opt(self):
        pass
    def standard_delete_opt(self):
        pass
    