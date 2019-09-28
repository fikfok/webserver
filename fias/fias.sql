with t as (
 select
     rtf_aoguid,
     concat(rtf_shorttypename, ' ', rtf_addressobjectname) as new_name,
     rtf_aolevel
 from fstf_addressobjects_addressobjecttree(a_aoguid :='dda23cea-8f99-4979-801d-e75835c75d9a')
 order by rtf_aolevel desc
),
tt as (
 select
     (array_agg(t.rtf_aoguid))[1] as lowest_aoguid,
     string_agg(t.new_name, ', ' order by t.rtf_aolevel) as full_name
 from t
 )

-- insert into fias_plain_address(aoguid, houseguid, full_name)
select
    tt.lowest_aoguid as aoguid,
    h.houseguid,
    concat(
        tt.full_name,
        ', д ',
        h.housenum,
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


select * from fias_plain_address limit 500;
select count(*) from fias_plain_address;
-- truncate table fias_plain_address ;
------------------------------------------------

with t as (
    select
        rtf_aoguid,
        concat(rtf_shorttypename, ' ', rtf_addressobjectname) as new_name,
        rtf_aolevel
    from fstf_addressobjects_addressobjecttree(a_aoguid :='5c092ca7-4066-44cc-820b-67b97772d5fc')
    order by rtf_aolevel desc
),
tt as (
select
   (array_agg(t.rtf_aoguid))[1] as lowest_aoguid,
   string_agg(t.new_name, ', ' order by t.rtf_aolevel) as full_name
from t
)
insert into fias_plain_address(aoguid, houseguid, full_name)
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



select phraseto_tsquery(full_name), full_name
from fias_plain_address
limit 10;


SELECT phraseto_tsquery('cats ate rats', true);