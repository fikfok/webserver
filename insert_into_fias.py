from sqlalchemy import create_engine
from dbfread import DBF


engine = create_engine(("postgresql://postgres:postgres@localhost/fias"))

tbl = iter(DBF('/home/fikfok/Downloads/fias_dbf/ADDROB77.DBF', encoding='cp866'))
flag = True
keys = ['AOGUID', 'AOID', 'CODE', 'PARENTGUID', 'REGIONCODE', 'AUTOCODE', 'AREACODE', 'CITYCODE', 'CTARCODE', 'PLACECODE', 'STREETCODE', 'FORMALNAME', 'OFFNAME', 'AOLEVEL'] 
while flag:
    query = "INSERT INTO addrobj (aoguid, aoid, code, parentguid, regioncode, autocode, areacode, citycode, ctarcode, placecode, streetcode, formalname, offname, aolevel) VALUES "
    for i in range(100):
        try:
            new_row = {key: dict(next(tbl))[key] for key in keys}
            new_tuple = str(tuple([new_row[key] for key in keys])) + ','
            if new_tuple:
                query += new_tuple
            else:
                flag = False
                break
        except StopIteration:
            flag = False
            break
    query = query[:-1] + ';'
    engine.execute(query)
