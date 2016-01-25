# -*- coding: utf-8 -*-
import sqlite3
from datetime import datetime

db_path = 'bankaccountoperations.db'

class RepositoryException(Exception):
    def __init__(self, message, *errors):
        Exception.__init__(self, message)
        self.errors = errors


class Bankaccountoperations():
    def __init__(self, id, op_date= datetime.now(), bankaccountoperationsitems=[]):
        self.id = id
        self.op_date = op_date
        self.bankaccountoperationsitems = bankaccountoperationsitems
        self.balance = sum([item.balance*item.in_out for item in self.bankaccountoperationsitems])


    def __repr__(self):
        return "<Bankaccountoperations(id='%s', op_date='%s', balance='%s', items='%s')>" % (
                    self.id, self.op_date, str(self.balance), str(self.bankaccountoperationsitems)
                )


class Bankaccountoperationsitems():
     def __init__(self, title, balance, in_out) :
        self.title = title
        self.balance = balance
        self.in_out = in_out

     def __repr__(self):
        return "<Bankaccountoperationsitems(title='%s', balance='%s', in_out='%s')>" % (
                    self.title, str(self.balance), str(self.in_out)
                )

class Repository():
     def __init__(self):
        try:
            self.conn = self.get_connection()
        except Exception as e:
            raise RepositoryException('GET CONNECTION:', *e.args)
        self._complete = False


     def __enter__(self):
        return self


     def __exit__(self, type_, value, traceback):
        self.close()

     def complete(self):
        self._complete = True

     def get_connection(self):
        return sqlite3.connect(db_path)

     def close(self):
        if self.conn:
            try:
                if self._complete:
                    self.conn.commit()
                else:
                    self.conn.rollback()
            except Exception as e:
                raise RepositoryException(*e.args)
            finally:
                try:
                    self.conn.close()
                except Exception as e:
                    raise RepositoryException(*e.args)


class BankaccountoperationsRepository(Repository):
    def add(self, bankaccountoperations):

        try:
            c = self.conn.cursor()
            balance = sum([item.balance*item.in_out for item in bankaccountoperations.bankaccountoperationsitems])
            c.execute('INSERT INTO Bankaccountoperations (id, op_date, balance) VALUES(?, ?, ?)',
                        (bankaccountoperations.id, str(bankaccountoperations.op_date), bankaccountoperations.balance)
                    )
            if bankaccountoperations.bankaccountoperationsitems:
                for bankaccountoperationsitems in bankaccountoperations.bankaccountoperationsitems:
                    try:
                        c.execute('INSERT INTO Bankaccountoperationsitems (title, balance, in_out, bankaccountoperations_id) VALUES(?,?,?,?)',
                                        (bankaccountoperationsitems.title, bankaccountoperationsitems.balance, bankaccountoperationsitems.in_out, bankaccountoperations.id)
                                )
                    except Exception as e:
                        print "item add error:", e
                        raise RepositoryException('error adding bankaccountoperationsitems item: %s, to bankaccountoperations: %s' %
                                                    (str(bankaccountoperationsitems), str(bankaccountoperations.id))
                                                )
        except Exception as e:
            #print "bankaccountoperations add error:", e
            raise RepositoryException('error adding bankaccountoperations %s' % str(bankaccountoperations))

    def delete(self, bankaccountoperations):
        try:
            c = self.conn.cursor()

            c.execute('DELETE FROM Bankaccountoperationsitems WHERE bankaccountoperations_id=?', (bankaccountoperations.id,))

            c.execute('DELETE FROM Bankaccountoperations WHERE id=?', (bankaccountoperations.id,))

        except Exception as e:
            #print "bankaccountoperations delete error:", e
            raise RepositoryException('error deleting bankaccountoperations %s' % str(bankaccountoperations))

    def getById(self, id):
        try:
            c = self.conn.cursor()
            c.execute("SELECT * FROM Bankaccountoperations WHERE id=?", (id,))
            bankaccountoperations_row = c.fetchone()
            bankaccountoperations= Bankaccountoperations(id=id)
            if bankaccountoperations_row == None:
                bankaccountoperations=None
            else:
                bankaccountoperations.op_date = bankaccountoperations_row[1]
                bankaccountoperations.balance = bankaccountoperations_row[2]
                c.execute("SELECT * FROM Bankaccountoperationsitems WHERE bankaccountoperations_id=? order by title", (id,))
                bankaccountoperations_items_rows = c.fetchall()
                items_list = []
                for item_row in bankaccountoperations_items_rows:
                    item = Bankaccountoperationsitems(title=item_row[0], balance=item_row[1], in_out=item_row[2])
                    items_list.append(item)
                bankaccountoperations.bankaccountoperationsitems=items_list
        except Exception as e:
            #print "bankaccountoperations getById error:", e
            raise RepositoryException('error getting by id bankaccountoperations_id: %s' % str(id))
        return bankaccountoperations

    def update(self, bankaccountoperations):
        try:
            bankaccountoperations_oryg = self.getById(bankaccountoperations.id)
            if bankaccountoperations_oryg != None:
                self.delete(bankaccountoperations)
            self.add(bankaccountoperations)
        except Exception as e:
            #print "bankaccountoperations update error:", e
            raise RepositoryException('error updating bankaccountoperations %s' % str(bankaccountoperations))



if __name__ == '__main__':
    try:
        with BankaccountoperationsRepository() as bankaccountoperations_repository:
            bankaccountoperations_repository.add(
                Bankaccountoperations(id = 1, op_date = datetime.now(),
                        bankaccountoperationsitems = [
                            Bankaccountoperationsitems(title = "wyplata",   balance = 1000, in_out = 50),
                            Bankaccountoperationsitems(title = "wplata",    balance = 1500, in_out = 500),
                            Bankaccountoperationsitems(title = "przelew",  balance = 750, in_out = 750),
                        ]
                    )
                )
            bankaccountoperations_repository.complete()
    except RepositoryException as e:
        print(e)

    print BankaccountoperationsRepository().getById(1)

    try:
        with BankaccountoperationsRepository() as bankaccountoperations_repository:
            bankaccountoperations_repository.update(
                Bankaccountoperations(id = 1, op_date = datetime.now(),
                        bankaccountoperationsitems = [
                            Bankaccountoperationsitems(title = "uznanie", balance = 1500, in_out = 750),
                            Bankaccountoperationsitems(title = "dociazenie", balance = 1400, in_out = 100),
                            Bankaccountoperationsitems(title = "przeksiegowanie",   balance = 1500, in_out = 100),
                        ]
                    )
                )
            bankaccountoperations_repository.complete()
    except RepositoryException as e:
        print(e)

    print BankaccountoperationsRepository().getById(1)

    try:
        with BankaccountoperationsRepository() as bankaccountoperations_repository:
            bankaccountoperations_repository.delete( Bankaccountoperations(id =1))
            bankaccountoperations_repository.complete()
    except RepositoryException as e:
         print(e)
