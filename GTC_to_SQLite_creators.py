import sqlite3
import logging
import os, sys

from sqlite_class import Database
from module import GenotypeCalls, BeadPoolManifest, code2genotype
from tkinter import filedialog
import tkinter as tk



def get_manifest_names(manifest_file):
    
    try:
        logging.info(f"Getting names from '{manifest_file}'")
        names = BeadPoolManifest(manifest_file).names
        return names
    except:
        logging.error(f"Unable to get names from '{manifest_file}'")

def get_manifest_chroms(manifest_file):
   
    try:
        logging.info(f"Getting chroms from '{manifest_file}'")
        return BeadPoolManifest(manifest_file).chroms
    except:
        logging.error(f"Unable to get chromosomes from '{manifest_file}'")

def get_manifest_map_infos(manifest_file):
    
    try:
        logging.info(f"Getting map_infos from '{manifest_file}'")
        return BeadPoolManifest(manifest_file).map_infos

    except:
        logging.error(f"Unable to get map_infos from '{manifest_file}'")

def get_gtc_genotypes(gtc_file):
    
    try:
        logging.info(f"Getting genotypes from '{gtc_file}'")
        return GenotypeCalls(gtc_file).get_genotypes()
    except:
        logging.error(f"Unable to get genotypes from '{gtc_file}'")

def get_gtc_base_calls(gtc_file):
    
    try:
        logging.info(f"Getting base_calls from '{gtc_file}'")
        return GenotypeCalls(gtc_file).get_base_calls()
    except:
        logging.error(f"Unable to get base_calls from '{gtc_file}'")  


def add_manifest(db_name):


    manifest_file = filedialog.askopenfilename(title = "Select Manifest file to add to database",filetypes = (("bpm files","*.bpm"),("all files","*.*")))
    if manifest_file == '':
        print(f"No manifest file selected during add_manifest!")
        logging.error(f"No manifest file selected during add_manifest!")
        return

    names = get_manifest_names(manifest_file)
    chroms = get_manifest_chroms(manifest_file)
    bases = get_manifest_map_infos(manifest_file)

    with Database(name=db_name) as db:
        create_manifest_table = """
                            CREATE TABLE IF NOT EXISTS manifest (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL UNIQUE,
                            chrom TEXT,
                            base TEXT
                            );
                            """

        db.query(create_manifest_table)

        data = []
        for i in range(len(names)):
            
            items = (names[i], chroms[i], bases[i])
            data.append(items)

        sql_query = f"INSERT INTO manifest (name, chrom, base) VALUES(?,?,?);" #add ; ???
        db.query_many(sql_query, data)

    print(f"Manifest added to {db_name}!")


def add_multi_gtc_files(db_name):
    
    manifest_file = filedialog.askopenfilename(title = "Select Manifest file to add to database",filetypes = (("bpm files","*.bpm"),("all files","*.*")))
    if manifest_file == '':
        print(f"No manifest file selected during add_manifest!")
        logging.error(f"No manifest file selected during add_manifest!")
        return

    gtc_files = filedialog.askopenfilenames(title = "Select GTC file(s) to add to database",filetypes = (("gtc files","*.gtc"),("all files","*.*")))
    if manifest_file == []:
        print(f"No GTC file(s) selected during add_multi_gtc_files!")
        logging.error(f"No GTC file(s) selected during add_multi_gtc_files!")
        return

    manifest_names = get_manifest_names(manifest_file)

    with Database(name=db_name) as db:

        create_patients_table = """
                                CREATE TABLE IF NOT EXISTS patients (
                                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                name TEXT NOT NULL UNIQUE
                                );
                                """

        create_genotype_table = """
                                CREATE TABLE IF NOT EXISTS genotypes (
                                genotype TEXT NOT NULL,
                                base TEXT NOT NULL,
                                manifest_name TEXT NOT NULL,
                                patient_name TEXT NOT NULL,
                                FOREIGN KEY (manifest_name) REFERENCES manifest (name),
                                FOREIGN KEY (patient_name) REFERENCES patients (name)
                                );
                                """

        db.query(create_patients_table)
        db.query(create_genotype_table)


    for gtc_file in gtc_files:
        add_gtc_file(db_name, gtc_file, manifest_names)

    print(f"GTC file(s) added to {db_name}!")

def add_gtc_file(db_name, gtc_file, manifest_names):

    patient_name = os.path.basename(gtc_file) #Get patient name from gtc_file_name
    patient_name = os.path.splitext(patient_name)[0]

    with Database(name=db_name) as db:

        sql_query = f"INSERT INTO patients (name) VALUES('{patient_name}');"
        db.query(sql_query)

        base_calls = get_gtc_base_calls(gtc_file)
        genotypes = get_gtc_genotypes(gtc_file)
        
        data = []
        for i in range(len(manifest_names)):
            
            items = (code2genotype[genotypes[i]], base_calls[i].decode('utf-8'), manifest_names[i], patient_name)
            data.append(items)


        sql_query = f"INSERT INTO genotypes (genotype, base, manifest_name, patient_name) VALUES(?,?,?,?);"
        db.query_many(sql_query, data)



def main():
    # INITIALISE LOGGING #
    logging.basicConfig(filename="sqlite_help.log", level=logging.DEBUG)

    #### HARD CODED VARIABLES ####
    db_name = "snpdata.db"

    ### INITIAL MENU ###
    os.system('cls') #Clear Screen (delete if not on windows)

    while True:
        
        print(f"1. Add manifest file (bpm) to database '{db_name}'.")
        print(f"2. Add GTC file(s) (gtc) to database '{db_name}'.")
        print("3. Exit Program")
        
        selection = ""
        while selection !="1" and selection != "2" and selection != "3":
            selection = input("Select from above (1, 2 or 3): ")

        if selection == "1":
            print("Use file diaglog to select a bpm file.")
            add_manifest(db_name)
            
        elif selection == "2":
            print("Use file diaglog to select a bpm file, and then to select gtc file(s).")
            add_multi_gtc_files(db_name)
            
        else:
            print("Exiting program")
            sys.exit()

        print("*" * 20)


if __name__=="__main__":
    main()