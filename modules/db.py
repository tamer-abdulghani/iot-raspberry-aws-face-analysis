import mysql.connector as mariadb


class Database:
    def __init__(self):
        host = "localhost"
        user = "root"
        password = ""
        db_name = "smile"
        self.con = mariadb.connect(host=host, user=user, password=password, db=db_name)
        self.cur = self.con.cursor()
        print(self.con)

    def insert_train_info(self, train_time, label, collection, aws_face_id, aws_image_id):
        sql = "INSERT INTO train (train_time, label, collection, aws_face_id, aws_image_id) VALUES (%s,%s,%s,%s,%s)"
        values = (train_time, label, collection, aws_face_id, aws_image_id)
        self.cur.execute(sql, values)
        self.con.commit()
        result = self.cur.lastrowid
        return result

    def insert_access_info(self, screen_time, label, is_access_allowed, face_attributes):
        sql = "INSERT INTO access (screen_time, label,	is_access_allowed,	face_attributes) VALUES (%s,%s,%s,%s)"
        values = (screen_time, label, is_access_allowed, face_attributes)
        self.cur.execute(sql, values)
        self.con.commit()
        result = self.cur.lastrowid
        return result

    def get_access_log(self):
        self.cur.execute("SELECT screen_time, label, is_access_allowed, face_attributes FROM access")
        access_info = []
        for screen_time, label, is_access_allowed, face_attributes in self.cur:
            log = {'screen_time': screen_time, 'label': label, 'is_access_allowed': is_access_allowed,
                   'face_attributes': face_attributes}
            access_info.append(log)
        return access_info
