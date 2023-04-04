def find(cursor, cls, id):
    cursor.execute(f'select * from {cls.__table__} where businessentityid = {id}')
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

def save(obj, conn, cursor):
    s_str = ', '.join(len(values(obj)) * ['%s'])
    venue_str = f"""INSERT INTO {obj.__table__} ({keys(obj)}) VALUES ({s_str});"""
    cursor.execute(venue_str, list(values(obj)))
    conn.commit()

def values(obj):
    venue_attrs = obj.__dict__
    return [venue_attrs[attr] for attr in obj.columns if attr in venue_attrs.keys()]

def keys(obj):
    venue_attrs = obj.__dict__
    selected = [attr for attr in obj.columns if attr in venue_attrs.keys()]
    return ', '.join(selected)