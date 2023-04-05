def find(cursor, cls, id):
    
    query = f'select * from {cls.__table__} where businessentityid = %s'
    
    cursor.execute(query, (id,))
    record = cursor.fetchone()
    return build_from_record(cls, record)

def find_all(cursor, cls, limit = 10):
    cursor.execute(f'select * from {cls.__table__} limit {limit}')
    records = cursor.fetchall()
    objs = [build_from_record(cls, record) for record in records]
    return objs



def build_from_record(Class, record):
    if not record: return None
    attr = dict(zip(Class.columns, record))
    obj = Class()
    obj.__dict__ = attr
    return obj

