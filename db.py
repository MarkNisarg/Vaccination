import sqlite3


class Database:
    def __init__(self, path):
        self.conn = sqlite3.connect(path)

    def select(self, sql, parameters=[]):
        c = self.conn.cursor()
        c.execute(sql, parameters)
        return c.fetchall()

    def execute(self, sql, parameters=[]):
        c = self.conn.cursor()
        c.execute(sql, parameters)
        self.conn.commit()

    def update_contact(self, name, email, message):
        self.execute("insert into contact_tbl(name,email,message) values(?,?,?)", [name, email, message])
        self.conn.commit()

    def update_signup(self, name, email, password, contact, birthdate):
        c = self.conn.cursor()
        account = c.fetchone()
        self.execute(
            "insert into registration_tbl(name,email,password,contact,birthdate,gender,otp) values(?,?,?,?,?,?,?)",
            [name, email, password, contact, birthdate, 'F', '000000'])
        self.conn.commit()
        print("You have successfully registered")

    def update_otp(self, otp, email):
        self.execute('UPDATE registration_tbl SET otp=? WHERE email=?', [otp, email])
        self.conn.commit()

    def update_password(self, email, password):
        self.execute('UPDATE registration_tbl SET password=? WHERE email=?', [password, email])
        self.conn.commit()

    def update_verify(self, email):
        self.execute('UPDATE registration_tbl SET isverify=? WHERE email=?', [1, email])
        self.conn.commit()

    def get_otp(self, email):
        data = self.select('SELECT otp FROM registration_tbl where email=? ', [email])
        return data[0][0]

    def get_user(self, email):
        data = self.select(
            'SELECT * FROM registration_tbl WHERE email=?', [email])
        if data:
            d = data[0]
            return {
                'username': d[1],
                'encrypted_password': d[2],
            }
        else:
            return None

    def close(self):
        self.conn.close()
