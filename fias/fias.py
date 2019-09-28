from sqlalchemy import create_engine


engine = create_engine('postgres://postgres:postgres@localhost:5432/fias')
query_adresses = """
SELECT aoguid FROM fias_addressobjects
where actstatus = 1;
"""
query_plain_address = """
with t as (
    select
        rtf_aoguid,
        concat(rtf_shorttypename, ' ', rtf_addressobjectname) as new_name,
        rtf_aolevel
    from fstf_addressobjects_addressobjecttree(a_aoguid :='{a_aoguid}')
    order by rtf_aolevel desc
),
tt as (
select
   (array_agg(t.rtf_aoguid))[1] as lowest_aoguid,
   string_agg(t.new_name, ', ' order by t.rtf_aolevel) as full_name
from t
)
select
    tt.lowest_aoguid as aoguid,
    h.houseguid,
    concat(
        tt.full_name,
        case
            when coalesce(h.housenum, '') <> '' then concat(', д ', h.housenum)
            else ''
        end,        
        case
            when coalesce(h.strucnum, '') <> '' then concat(', корп ', h.strucnum)
            else ''
        end,
        case
            when coalesce(h.buildnum, '') <> '' then concat(', стр ', h.buildnum)
            else ''
        end
    ) as full_name
from tt
inner join fias_houseobjects as h on tt.lowest_aoguid = h.aoid and h.statstatus = 0
order by h.housenum;
"""
with engine.connect() as con:
    adreses = con.execute(query_adresses)
    for adr in adreses:
        # print(adr[0])
        # a_aoguid = 'dda23cea-8f99-4979-801d-e75835c75d9a'
        a_aoguid = adr[0]
        plain_addresses = con.execute(query_plain_address.format(a_aoguid=a_aoguid))
        if plain_addresses.rowcount:
            insert_query = """
            insert into fias_plain_address(aoguid, houseguid, full_name) 
            values """
            values = []
            for pl_adr in plain_addresses:
                values += ["('{}', '{}', '{}')".format(pl_adr[0], pl_adr[1], pl_adr[2])]
            insert_query += ', '.join(values)
            con.execute(insert_query)
