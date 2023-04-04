from api.models.person import Person

def test_person_accepts_mass_assignment():
    person = Person(PersonType = 'EM', NameStyle = 'f', 
                    FirstName = 'Ken', MiddleName = 'J', LastName = 'Sanchez')
    assert person.FirstName == 'Ken'

def test_person_has_property_of__table__():
    assert Person.__table__ == 'person.person'

def test_person_has_property_of_columns():
    assert Person.columns == ['BusinessEntityId', 'PersonType', 
    'NameStyle', 'Title', 'FirstName', 'MiddleName', 
    'LastName', 'Suffix', 
    'EmailPromotion', 'AdditionalContactInfo', 
    'Demographics', 'rowguid', 'ModifiedData']

def build_records(conn, cursor):
    cursor.execute(f"ALTER SEQUENCE movies_id_seq RESTART WITH 1;")
    conn.commit()
    for i in range(1, 15):
        fast_and_furious = Movie(title = f'Fast and Furious: {i}')
        save(fast_and_furious, conn, cursor)
