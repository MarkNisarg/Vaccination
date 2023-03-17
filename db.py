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
            [name, email, password, contact, birthdate, 'N/A', '000000'])
        self.conn.commit()
        print("You have successfully registered")

    def create_vaccine_schedule(self, email, contact):
        self.execute('insert into vaccine_schedule_tbl (email,contact) values (?,?)', [email, contact])
        self.conn.commit()

    def update_vaccine_status(self, vaccine, status, email):
        self.execute('update vaccine_schedule_tbl set ' + vaccine + '=? where email=?', [status, email])
        self.conn.commit()

    def get_users(self):
        users = self.select('SELECT * FROM registration_tbl where isverify=1')
        return [
          {
            'name': user[0],
            'email':user[1],
            'birthdate': user[4]
          }
          for user in users
        ]

    def get_vaccines_status(self, email):
        data = self.select(
            'SELECT * FROM vaccine_schedule_tbl WHERE email=?', [email])
        if data:
            vaccines = data[0]
            return {
                'bcg_1': vaccines[2],
                'hep_b_1': vaccines[3],
                'hep_b_2': vaccines[4],
                'hep_b_3': vaccines[5],
                'opv_1': vaccines[6],
                'opv_2': vaccines[7],
                'opv_3': vaccines[8],
                'opv_4': vaccines[9],
                'opv_5': vaccines[10],
                'opv_booster_dose_1': vaccines[11],
                'opv_booster_dose_2': vaccines[12],
                'dpt_1': vaccines[13],
                'dpt_2': vaccines[14],
                'dpt_3': vaccines[15],
                'dpt_booster_dose_1': vaccines[16],
                'dpt_booster_dose_2': vaccines[17],
                'hep_a_1': vaccines[18],
                'hep_a_2': vaccines[19],
                'hep_a_3': vaccines[20],
                'ipv_1': vaccines[21],
                'ipv_2': vaccines[22],
                'ipv_3': vaccines[23],
                'pneumococcal_1': vaccines[24],
                'pneumococcal_2': vaccines[25],
                'pneumococcal_3': vaccines[26],
                'hib_1': vaccines[27],
                'hib_2': vaccines[28],
                'hib_3': vaccines[29],
                'rotavirus_1': vaccines[30],
                'rotavirus_2': vaccines[31],
                'measles_1': vaccines[32],
                'chickenpox_1': vaccines[33],
                'mmr_1': vaccines[34],
                'typhoid_1': vaccines[35],
                'td_vac_1': vaccines[36],
            }
        else:
            return None

    def update_otp(self, otp, email):
        self.execute('UPDATE registration_tbl SET otp=? WHERE email=?', [otp, email])
        self.conn.commit()

    def update_ask_tbl(self, email, contact,question):
        self.execute('insert into ask_question_tbl (email,contact,message) values (?,?,?)', [email, contact, question])
        self.conn.commit()

    def update_name(self, name, email):
        self.execute('UPDATE registration_tbl SET name=? WHERE email=?', [name, email])
        self.conn.commit()

    def update_dob(self, dob, email):
        self.execute('UPDATE registration_tbl SET birthdate=? WHERE email=?', [dob, email])
        self.conn.commit()

    def update_phone(self, phone, email):
        self.execute('UPDATE registration_tbl SET birthdate=? WHERE email=?', [phone, email])
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
                'name': d[0],
                'email': d[1],
                'encrypted_password': d[2],
                'contact': d[3],
                'birthdate': d[4],
            }
        else:
            return None

    def close(self):
        self.conn.close()
