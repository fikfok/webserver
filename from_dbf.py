from sqlalchemy import create_engine
from dbfread import DBF


engine = create_engine('postgresql://postgres:postgres@localhost/fias')
tbl = iter(DBF('/home/fikfok/Downloads/fias/HOUSE77.DBF'))
flag = True
while flag:
    query = 'insert into fias_houseobjects (AOID, BUILDNUM, HOUSEGUID, HOUSEID, HOUSENUM, STATSTATUS, STRUCNUM) values '
    for i in range(10000):
        try:
            values = tuple(next(tbl).values())
            query += str((values[0], values[1], values[4], values[5], values[6], values[7], values[14])) + ','
        except StopIteration:
            flag = False
            break
    query = query[:-1] + ';'
    engine.execute(query)


# values = tuple(next(tbl).values())
# print(values[0], values[1], values[4], values[5], values[6], values[7], values[14])
