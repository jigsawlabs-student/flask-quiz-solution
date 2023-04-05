from api.lib.orm import build_from_record
from api.lib.db import save
class Person:
    __table__ = 'person.person'
    columns = ['businessentityid', 'persontype', 'namestyle', 'title', 'firstname',
      'middlename', 'lastname', 'suffix', 'emailpromotion', 
      'additionalcontactinfo', 'demographics', 'rowguid', 'modifieddata']
    
    def __init__(self, **kwargs):
        for key in kwargs.keys():
            if key not in self.columns:
                raise ValueError(f'{key} not in columns: {self.columns}')
        self.__dict__ = kwargs

    @classmethod
    def find_or_create_by_first_last_name_and_id(self, conn, firstname, lastname, businessentityid):
        cursor = conn.cursor()
        query = f'''select * from person.person where firstname = %s and lastname = %s and businessentityid = %s'''
        cursor.execute(query, (firstname, lastname, businessentityid))
        record = cursor.fetchone()
        if record:
            return build_from_record(Person, record)
        else:
            person = Person(firstname = firstname, lastname = lastname, businessentityid = businessentityid)
            saved_person = save(person, conn, cursor)
            return saved_person