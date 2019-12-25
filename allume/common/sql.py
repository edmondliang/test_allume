import os
from allume.common.model import Model
from functools import lru_cache


def upsert(object, tablename, ignore=[], key_field='id'):
    keys = remove_elements_from_list(dict(object).keys(), ignore)
    return f'''insert into {tablename} ({",".join(keys)}) values ({",".join( "%(" + x + ")s" for x in keys)})
            ON CONFLICT({key_field}) DO UPDATE SET ({",".join(keys)})=({",".join( "EXCLUDED."+x for x in keys)})
            returning *'''


def insert(object, tablename, ignore=[]):
    keys = remove_elements_from_list(dict(object).keys(), ignore)
    return f'''insert into {tablename} ({",".join(keys)}) values ({",".join( "%(" + x + ")s" for x in keys)}) returning *'''


def update(object, tablename, ignore=[]):
    keys = remove_elements_from_list(dict(object).keys(), ignore)

    return f'update {tablename} set ({",".join(keys)}) = ({",".join( "%(" + x + ")s" for x in keys)}) where id =%(id)s returning *'


def remove_elements_from_list(source, elements_to_remove):
    return [x for x in source if x not in elements_to_remove]


def delete_by_field(tablename, field):
    return f'delete from {tablename} where {field} =%({field})s'


def select_by_fields(tablename, fields):
    return f'select * from {tablename} where {" and ".join( f"{key} =%({key})s" for key in fields)}'


def delete_by_fields(tablename, fields):
    return f'delete from {tablename} where {" and ".join( f"{key} =%({key})s" for key in fields)}'


@lru_cache(maxsize=32)
def load_from_file(directory, filename):
    with open(os.path.join(directory, filename)) as sqlfile:
        query = sqlfile.read()
    return query