import repository
import sqlite3
import unittest


db_path = 'bankaccountoperations.db'

class RepositoryTest(unittest.TestCase):

    def setUp(self):
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('''INSERT INTO Bankaccountoperations (id, op_date, balance) VALUES(1,'2016-05-30', 1500)''')
        c.execute('''INSERT INTO Bankaccountoperationsitems (title, balance, in_out, bankaccountoperations_id) VALUES('wplata',1000,500,1)''')
        c.execute('''INSERT INTO Bankaccountoperationsitems (title, balance, in_out, bankaccountoperations_id) VALUES('wyplata',1000,50,1)''')
        conn.commit()
        conn.close()

    def tearDown(self):
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('DELETE FROM Bankaccountoperationsitems')
        c.execute('DELETE FROM Bankaccountoperations')
        conn.commit()
        conn.close()

    def testGetByIdInstance(self):
        bankaccountoperations = repository.BankaccountoperationsRepository().getById(1)
        self.assertIsInstance(bankaccountoperations, repository.Bankaccountoperations, "Obiekt nie jest klasy Bankaccountoperations")

    def testGetByIdNotFound(self):
        self.assertEqual(repository.BankaccountoperationsRepository().getById(22),
                None, "Powinno wyjsc None")

    def testGetByIdBankaaccountoperationsitemsLen(self):
        self.assertEqual(len(repository.BankaccountoperationsRepository().getById(1).bankaccountoperationsitems),
                2, "Powinno wyjsc 2")

    def testDeleteNotFound(self):
        self.assertRaises(repository.RepositoryException,
                repository.BankaccountoperationsRepository().delete, 22)



if __name__=='main':
    unittest.main()
