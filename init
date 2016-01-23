import sqlite3


db_path = 'bankaccountoperations.db'
conn = sqlite3.connect(db_path)

c = conn.cursor()

c.execute('''
          CREATE TABLE Bankaccountoperations
          ( id INTEGER PRIMARY KEY,
            op_date DATE NOT NULL,
			balance FLOAT
          )
          ''')
c.execute('''
          CREATE TABLE Bankaccountoperationsitems
          ( title VARCHAR(30),
            balance FLOAT,
			in_out NUMERIC NOT NULL,
			bankaccountoperations_id INTEGER,
			FOREIGN KEY(bankaccountoperations_id) REFERENCES Bankaccountoperations(id),
            PRIMARY KEY (title, bankaccountoperations_id)
			)
          ''')
