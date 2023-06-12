import pymysql
import os
import shutil
import json
class uploadFiles(object):
    def __init__(self):
        # self.host = os.environ['DB_HOST']
        self.host = 'localhost'
        # self.username = os.environ['DB_USER']
        self.username = 'root'
        # self.password = os.environ['DB_PASSWORD']
        self.password = ''
        # self.db = os.environ['DB']
        self.db = 'eautopacific'
        # self.port = int(os.environ['DB_PORT'])
        self.port = int(3306)

        self.cursor = self.connect_db()


    def connect_db(self):
        cnx = {'host': self.host,
               'username': self.username,
               'password': self.password,
               'db': self.db,
               'port': int(self.port)
               }
        self.conn = pymysql.connect(db=cnx['db'], host=cnx['host'], port=cnx['port'], user=cnx['username'],
                                    password=cnx['password'])
        self.cursor = self.conn.cursor()
        return self.cursor

    def upload_image(self):
        names = []
        img_directory = 'E:\Image\image'
        upload_directory_1 = 'E:\\RYJ\\img\\upload_photo'
        upload_directory_2 = 'E:\\RYJ\\img\\upload_photos'

        out_directory = 'E:\\RYJ\\new_image'
        for s_path, s_dirs, s_files in os.walk(upload_directory_1):
            try:
                if s_dirs:
                    for name in s_dirs:
                        if '_' in name:
                            manu_name = name.replace('_', ' ')
                            self.cursor.execute("SELECT makeid FROM make WHERE name={}".format(self.add_quote(manu_name)))
                            manu_id = self.cursor.fetchall()
                            if not manu_id:
                                manu_name = name.replace('_', '-')
                            self.cursor.execute("SELECT makeid FROM make WHERE name={}".format(self.add_quote(manu_name)))
                            manu_id = self.cursor.fetchall()
                            if not manu_id:
                                manu_name = name.replace('_', '/')
                                self.cursor.execute("SELECT makeid FROM make WHERE name={}".format(self.add_quote(manu_name)))
                                manu_id = self.cursor.fetchall()
                            if not manu_id:
                                manu_name = name.replace('_', ' & ')
                                self.cursor.execute("SELECT makeid FROM make WHERE name={}".format(self.add_quote(manu_name)))
                                manu_id = self.cursor.fetchall()

                        else:
                            self.cursor.execute(
                                "SELECT makeid FROM make WHERE name={}".format(self.add_quote(name)))
                            manu_id = self.cursor.fetchall()
                        manu_id = manu_id[0][0] if manu_id else None

                        if manu_id:
                            new_directory = os.path.join(out_directory, str(manu_id))
                            if not os.path.isdir(new_directory):
                                os.mkdir(new_directory)
                            directory_path = os.path.join(s_path, name)
                            for ss_path, ss_dirs, ss_files in os.walk(directory_path):
                                for ss_file in ss_files:
                                    self.cursor.execute("SELECT VehicleID FROM vehiclephoto WHERE LargeFileName={}".format(self.add_quote(ss_file)))
                                    vehicleid = self.cursor.fetchall()
                                    vehicleid = vehicleid[0][0] if vehicleid else None
                                    if vehicleid:
                                        image_directory = os.path.join(new_directory, str(vehicleid))
                                        if not os.path.isdir(image_directory):
                                            os.mkdir(image_directory)
                                        img_source_path = os.path.join(ss_path, ss_file)
                                        if not os.path.isfile(os.path.join(image_directory, ss_file)):
                                            shutil.copy(img_source_path, image_directory)
                                    else:
                                        ss_file
                                for ss_dir in ss_dirs:
                                    another_directory = os.path.join(ss_path, ss_dir)
                                    for thumb_path, thumb_dirs, thumb_files in os.walk(another_directory):
                                        for thumb_file in thumb_files:
                                            self.cursor.execute("SELECT VehicleID FROM vehiclephoto WHERE LargeFileName={}".format(
                                                self.add_quote(thumb_file)))
                                            vehicleid = self.cursor.fetchall()
                                            vehicleid = vehicleid[0][0] if vehicleid else None
                                            if vehicleid:
                                                image_directory = os.path.join(new_directory, str(vehicleid), 'thumb')
                                                if not os.path.isdir(image_directory):
                                                    os.mkdir(image_directory)
                                                img_source_path = os.path.join(thumb_path, thumb_file)
                                                if not os.path.isfile(os.path.join(image_directory, thumb_file)):
                                                    shutil.copy(img_source_path, image_directory)
                                                shutil.copy(img_source_path, image_directory)
                                            else:
                                                thumb_file
                        else:
                            name
            except Exception as e:
                print(e)
        for s_path, s_dirs, s_files in os.walk(upload_directory_2):
            try:
                if s_files:
                    for s_file in s_files:
                        self.cursor.execute(
                            "SELECT VehicleID FROM vehiclephoto WHERE LargeFileName={}".format(self.add_quote(s_file)))
                        vehicleid = self.cursor.fetchall()
                        vehicleid = vehicleid[0][0] if vehicleid else None
                        if vehicleid:
                            self.cursor.execute("SELECT makeid FROM vehicles WHERE VehicleID={}".format(self.add_quote(vehicleid)))
                            manu_id = self.cursor.fetchall()
                            manu_id = manu_id[0][0] if manu_id else None
                            if manu_id:
                                new_directory = os.path.join(out_directory, str(manu_id))
                                if not os.path.isdir(new_directory):
                                    os.mkdir(new_directory)
                                sub_new_directory = os.path.join(new_directory, str(vehicleid))
                                if not os.path.isdir(sub_new_directory):
                                    os.mkdir(sub_new_directory)
                                img_source_path = os.path.join(s_path, s_file)
                                if not os.path.isfile(os.path.join(sub_new_directory, s_file)):
                                    shutil.copy(img_source_path, sub_new_directory)
                                thumb_directory = os.path.join(sub_new_directory, 'thumb')
                                if not os.path.isdir(thumb_directory):
                                    os.mkdir(thumb_directory)
                                if not os.path.isfile(os.path.join(thumb_directory, s_file)):
                                    shutil.copy(img_source_path, thumb_directory)
                            else:
                                vehicleid

            except Exception as e:
                print(e)

    def upload_pdf(self):
        upload_directory = 'E:\\Image\\img\\files'
        out_directory = 'E:\\Image\\new_pdf'
        files = []
        non_files = []
        db_files = []
        try:
            for s_path, s_dirs, s_files in os.walk(upload_directory):
                if s_files:
                    for s_file in s_files:
                        self.cursor.execute(
                            "SELECT VehicleID FROM vehicleinsightfile WHERE insightFile={}".format(self.add_quote(s_file)))
                        vehicleID = self.cursor.fetchall()
                        vehicleID = vehicleID[0][0] if vehicleID else None
                        if vehicleID:
                            files.append(s_file)
                            o_directory = os.path.join(out_directory, str(vehicleID))
                            if not os.path.isdir(o_directory):
                                os.mkdir(o_directory)
                            pdf_source_path = os.path.join(s_path, s_file)
                            if not os.path.isfile(os.path.join(o_directory, s_file)):
                                shutil.copy(pdf_source_path, o_directory)
                        else:
                            non_files.append(s_file)

        except Exception as e:
            print(e)

        res = [i for i in db_files if i not in files]
        return files, json.dumps(res, indent=4)

    def add_quote(self, w):
        return '"{}"'.format(w)

def main(event, context):
    cf = uploadFiles()
    cf.upload_image()
    # cf.upload_pdf()
if __name__ == "__main__":
    main(0, 0)