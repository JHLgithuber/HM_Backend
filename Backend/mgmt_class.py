import Backend.DBconnect_class as DB_class

class mgmt:
    def __init__(self,id,CURD,entity,option,data,server):
        self.id=id
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
                    raise

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
                    raise
                
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
                    raise
                
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
                    raise
                
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
                    raise
                
            case 'Vehicle_data':
                if CURD=='read':
                    self.standard_select_ALL()
                elif CURD=='create':
                    pass
                elif CURD=='update':
                    pass
                elif CURD=='delete':
                    pass
                else:
                    raise
                
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
                    raise
                
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
                    raise
    
    def standard_read_ALL(self):
        self.result=DB_class.Connect_to_DB(self.server).add_sql(f"SELECT * FROM {self.entity};").execute().fetch().fetch_data
        return self
    