#!/usr/bin/python3

import re
import csv
import sqlite3

def create_tables(db):
  cursor = db.cursor()
  cursor.execute('drop table if exists DELoad')
  cursor.execute('drop table if exists classification_totals')
  
  print('Creating tables...')
  # create loading table
  cursor.execute('''create table DELoad(
      objectNumber varchar(20),
      isHighlight boolean,
      isPublicDomain boolean,
      objectID int primary key,
      department varchar(30),
      objectName varchar(50),
      title varchar(200),
      culture varchar(50),
      period varchar(100),
      dynasty varchar(20),
      reign varchar(20),
      portfolio varchar(20),
      artistRole varchar(100),
      artistPrefix varchar(100),
      artistDisplayName varchar(200),
      artistDisplayBio varchar(200),
      artistSuffix varchar(50),
      artistAlphaSort varchar(50),
      artistNationality varchar(50),
      artistBeginDate varchar(20),
      artistEndDate varchar(20),
      objectDate varchar(20),
      medium varchar(10),
      dimensions text,
      creditLine text,
      geographyType varchar(100),
      city varchar(20),
      state varchar(20),
      county varchar(20),
      country varchar(20),
      region varchar(20),
      subregion varchar(20),
      locale varchar(20),
      locus varchar(20),
      excavation varchar(20),
      river varchar(20),
      classification varchar(50),
      rightsandReproduction varchar(50),
      linkResource varchar(100),
      metadataDate datetime,
      repository varchar(50),
      tags varchar(100)
    )
  ''')

  # create classifications table
  cursor.execute('''create table classification_totals (
    classification varchar(50) primary key,
    classification_count int
  )
  ''')
  db.commit()

def load_records(db, csv_file):
  object_number_re = re.compile(r"\A\d+\.\d+\.\d+\Z")
  query = '''insert into DELoad values (
    ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,
    ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
  '''
  cursor = db.cursor();

  csv_lines = 0
  print('Loading CSV file...')
  with open(csv_file) as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
      csv_lines += 1
      if object_number_re.match(row[0]):
        cursor.execute(query, row)
  db.commit()

  print('Getting count...')
  cursor.execute("select count(*) from DELoad")
  sql_count = cursor.fetchone()[0]
  print('CSV Count: {}; SQL Count: {}'.format(csv_lines, sql_count))

def load_classifications(db):
  print('Calculating Classifications...')
  cursor = db.cursor()
  cursor.execute('''
    insert into classification_totals
    select classification, count() from DELoad 
    where classification is not null and classification != '(not assigned)' 
    group by classification
  ''')
  db.commit()

  cursor.execute("select count(*) from classification_totals")
  sql_count = cursor.fetchone()[0]
  print('Classification Count: {}'.format(sql_count))

def read_from_db(db):
  print('Reading from DB...')
  cursor = db.cursor();
  cursor.execute("select * from DELoad limit 10 offset 500")
  for r in cursor:
    print(r)
  cursor.execute('select * from classification_totals')
  for r in cursor:
    print(r)

def main():
  db = sqlite3.connect('DE.db')
  csvfile = 'DataEngineerDataSet.csv'
  create_tables(db)
  load_records(db, csvfile)
  load_classifications(db)
  
  # this is for debugging purposes.
  #read_from_db(db)

if __name__ == "__main__":
  main()
