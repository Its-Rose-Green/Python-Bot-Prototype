#!/usr/bin/python3 
import psycopg2
from psycopg2 import Error

class Database():

    def __init__(self) -> None:
        
        self.cxn = None
        self.cursor = None
    
    def __setUp(self) -> None:
        try:
            self.cxn = psycopg2.connect()
        except (Exception, Error) as error:
            print("Error while connecting to PostgreSQL")
    