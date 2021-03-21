import sqlite3
import logging

from sqlite_class import Database


logging.basicConfig(filename="sqlite_help.log", level=logging.DEBUG)
db_name = "snpdata.db"


with Database(name=db_name) as db:


    columns = "patient_name, manifest_name, base"
    table = "genotypes"
    #manifest_names = "'rs1799945','rs1800562'"
    manifest_names = "'rs1800562'"
    
    test2 = db.read_query(f"SELECT {columns} FROM {table} WHERE manifest_name IN ({manifest_names});")
    
    for patient in test2:
        print(patient)
    

