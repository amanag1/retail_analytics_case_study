import os
import csv
import pandas as pd
from flask import *
from sqlalchemy import *
from sqlalchemy.orm import *
from flask_sqlalchemy import SQLAlchemy

import constants
from utils.logger.applicationlogger import AppLogger
from utils.logger.exceptions import ApplicationError

logger = AppLogger()

app = Flask(__name__)

app.config[constants.SQLALCHEMY_DATABASE_URI] = constants.POSTGRES_URL
app.config[constants.MAX_CONTENT_LENGTH] = 1024 * 1024
app.config[constants.UPLOAD_FOLDER] = constants.FILE_UPLOAD_DIR
app.config[constants.SQLALCHEMY_TRACK_MODIFICATIONS] = False
app.config[constants.FILE_UPLOADS] = constants.FILE_UPLOAD_DIR

db = SQLAlchemy(app)
db.init_app(app)



class InsertData():

    @staticmethod
    def add_obj_to_session(obj, session):
        """
        insert data object in a table
        :param obj (Object): object of a table class having data to be inserted in table.
        :return: True/False on successful or unsuccessful db operation
        """
        flag = False
        try:
            flag = True
            db.session.add(obj)  # Adding data to sqlAlchemy orm for insertion
        except Exception as error:
            import traceback
            print(traceback.format_exc())
            flag = False
            logger.info(f'{constants.OBJECT_ADD_FAIL} {error}')
        else:
            logger.info(f'{constants.OBJECT_ADD_SUCCESS}')
        return flag



class Setter(InsertData):
    def set_object(self, session):
        result = InsertData.add_obj_to_session(self,session)
        return result


class Retail(db.Model,Setter):
    __tablename__ = constants.TABLE_NAME
    __table_args__ = constants.SCHEMA

    id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    store_id = db.Column(db.Integer())
    sku = db.Column(db.Integer())
    product_name = db.Column(db.String())
    price = db.Column(db.Integer())
    date = db.Column(db.DateTime)


    def __init__(self,store_id,sku,product_name,price,date):
        self.store_id = store_id
        self.sku = sku
        self.product_name = product_name
        self.price = price
        self.date = date

    def __repr__(self):
        return f"{self.store_id}:{self.sku} : {self.product_name}:{self.price}:{self.date}"

db.create_all()

@app.route('/home')
def upload_csvfile():
    try:
        print()
        return render_template(constants.RETAIL_HTML,flag=constants.FLAG_HOME)
    except Exception as error:
        import traceback
        print(traceback.format_exc())
        return  render_template(constants.RETAIL_HTML,msg=constants.FILE_ERROR_MSG,flag=constants.FLAG_ERROR)



@app.route('/show_retail_data', methods = ['POST'])
def save_display_csv_file_data():
    session = Session()
    try:
        status_list = []

        if request.method == 'POST':
            if request.files:
                uploaded_file = request.files['file']  # This line uses the same variable and worked fine
                filepath = os.path.join(constants.FILE_UPLOAD_DIR, uploaded_file.filename)
                
                uploaded_file.save(filepath)
                data = pd.read_csv(filepath)

                with open(filepath) as file:
                    csv_file_data = csv.reader(file)
                    headers = next(csv_file_data)
                    for row in csv_file_data:
                        if len(row)>2:
                            retail_obj = Retail(store_id=row[0], sku=row[1], product_name=row[2], price=row[3],date=row[4]).set_object(session=session)
                            status_list.append(retail_obj)
                if status_list:
                    db.session.commit()
                    logger.info(constants.DATA_ADD_SUCCESS)
                else:
                    db.session.close()

            final_result = Retail.query.all()

            display_result_list = [row.__dict__ for row in final_result]
            if len(display_result_list)>0:
                initial_df = pd.DataFrame(display_result_list)
                resultant_df = initial_df.drop([constants.INSTANCE_STATE, constants.ID], axis=1)
                resultant_df = resultant_df[[constants.STORE_ID, constants.SKU, constants.PRODUCT_NAME, constants.PRICE, constants.DATE]]
                resultant_df = resultant_df.rename(columns=str.title)
                resultant_df = resultant_df.sort_values(by=[constants.STORE_ID_TITLE])

                return render_template(constants.RETAIL_HTML, name=uploaded_file.filename,tables=[resultant_df.to_html(index=False)], titles=[''],flag=constants.ACTION,inner_flag=constants.INNER_FLAG)
            else:
                return render_template(constants.RETAIL_HTML,msg=constants.NO_RECORD_FOUND_MSG,flag=constants.NO_RECORD_FOUND)
    except Exception:
        import traceback
        print(traceback.format_exc())
        return  render_template(constants.RETAIL_HTML,msg=constants.ERROR_MSG,flag=constants.FLAG_ERROR)


@app.route('/record_data_template')
def record_data_template():
    try:
        action_val = str(request.url).split('?')[1].split('=')[1].lower()
        return render_template(constants.RETAIL_HTML,act=action_val,flag=constants.RECORD_DATA_TEMPLATE)
    except Exception as error:
        import traceback
        print(traceback.format_exc())
        return  render_template(constants.RETAIL_HTML,msg=constants.ERROR_MSG,flag=constants.FLAG_ERROR)


@app.route('/search',methods = ['POST'])
def search_record():
    try:
        if request.method == 'POST':
            sid = request.form[constants.STORE_ID]
            pname = request.form[constants.PRODUCT_NAME]
            sku = request.form[constants.SKU]
            price = request.form[constants.PRICE]

            #----------------------Search Criteria 1 : On basis of Store ID to display all records with matching store id
            #final_result = Retail.query.filter_by(store_id=sid)

            #----------------------Search Criteria 2 : On basis of Store ID to display firsy with matching store id
            #final_result = Retail.query.filter_by(store_id=sid).first()

            #----------------------Search Criteria 3 : On basis of Store ID and Product Name to display all records with with given store id and product name but using filter
            '''
            filter_by is used for simple queries on the column names using regular kwargs, like -- db.users.filter_by(name='Joe')
            filter does same without using kwargs, but instead using the '==' equality operator, which has been overloaded on the db.users.name object -- db.users.filter(db.users.name=='Joe')
            '''
            final_result = Retail.query.filter(Retail.store_id==sid,Retail.product_name==pname)

            #----------------------Search Criteria 4 : On basis of Store ID and Product Name to display all records with given store id or product name
            #final_result = Retail.query.filter(or_(Retail.store_id == sid, Retail.product_name == pname))

            #----------------------Search Criteria 5 : On basis of Store ID and Product Name to display all records with given store id and product name
            #final_result = Retail.query.filter(and_(Retail.store_id == sid, Retail.product_name == pname))

            #----------------------Search Criteria 6 : On basis of Store ID and Product Name to display all records with given store id and product name
            #final_result = Retail.query.filter(Retail.store_id == sid,Retail.price<price)

            display_result_list = [row.__dict__ for row in final_result]
            if len(display_result_list)>0:
                initial_df = pd.DataFrame(display_result_list)
                resultant_df = initial_df.drop([constants.INSTANCE_STATE, constants.ID], axis=1)
                resultant_df = resultant_df[[constants.STORE_ID,constants.SKU,constants.PRODUCT_NAME,constants.PRICE,constants.DATE]]
                resultant_df = resultant_df.rename(columns=str.title)
                resultant_df = resultant_df.sort_values(by=[constants.STORE_ID_TITLE])
                return render_template(constants.RETAIL_HTML,tables=[resultant_df.to_html(index=False)], titles=[''],flag=constants.ACTION)
            else:
                return render_template(constants.RETAIL_HTML, msg=constants.NO_RECORD_FOUND_MSG,
                                       flag=constants.NO_RECORD_FOUND)

    except Exception as error:
        import traceback
        print(traceback.format_exc())
        return  render_template(constants.RETAIL_HTML,msg=constants.ERROR_MSG,flag=constants.FLAG_ERROR)



@app.route('/update',methods = ['POST','PUT'])
def update_record():
    try:

        if request.method == 'POST':
            sid = request.form[constants.STORE_ID]
            pname  =request.form[constants.PRODUCT_NAME]
            sku = request.form[constants.SKU]
            price = request.form[constants.PRICE]

            #<---------------Updating Price for Record on the basis of given conditions--------------->
            initial_result_count = Retail.query.filter_by(store_id=sid,product_name=pname).count()
            if initial_result_count > 0:
                initial_result = Retail.query.filter_by(store_id=sid, product_name=pname).update({Retail.price: price},
                                                                                                 synchronize_session=False)
                db.session.commit()
                final_result = Retail.query.all()
                display_result_list = [row.__dict__ for row in final_result]
                if len(display_result_list) > 0:

                    initial_df = pd.DataFrame(display_result_list)
                    resultant_df = initial_df.drop([constants.INSTANCE_STATE, constants.ID], axis=1)
                    resultant_df = resultant_df[
                        [constants.STORE_ID, constants.SKU, constants.PRODUCT_NAME, constants.PRICE, constants.DATE]]
                    resultant_df = resultant_df.rename(columns=str.title)
                    resultant_df = resultant_df.sort_values(by=[constants.STORE_ID_TITLE])

                    return render_template(constants.RETAIL_HTML, tables=[resultant_df.to_html(index=False)],
                                           titles=[''], flag=constants.ACTION)
                else:
                    return render_template(constants.RETAIL_HTML, msg=constants.NO_RECORD_FOUND_MSG,
                                           flag=constants.NO_RECORD_FOUND)

            else:
                return render_template(constants.RETAIL_HTML, msg=constants.NO_RECORD_FOUND_FOR_UPDATE,
                                       flag=constants.NO_RECORD_FOUND)

    except Exception as error:
        import traceback
        print(traceback.format_exc())
        return  render_template(constants.RETAIL_HTML,msg=constants.ERROR_MSG,flag=constants.FLAG_ERROR)


@app.route('/delete',methods = ['POST'])
def delete_record():
    try:
        if request.method == 'POST':
            sid = request.form[constants.STORE_ID]
            pname  =request.form[constants.PRODUCT_NAME]
            sku = request.form[constants.SKU]
            price = request.form[constants.PRICE]

            # <-------------Delete multiple record------------>
            initial_result_count = Retail.query.filter_by(store_id=sid).count()
            if initial_result_count > 0:
                initial_result = Retail.query.filter_by(store_id=sid).delete(synchronize_session=False)

                #<--------------Delete single record-------------->
                # result = Retail.query.filter_by(store_id=sid).first()
                # if result:
                #     db.session.delete(result)

                db.session.commit()

                final_result = Retail.query.all()
                display_result_list = [row.__dict__ for row in final_result]
                if len(display_result_list)>0:
                    initial_df = pd.DataFrame(display_result_list)
                    resultant_df = initial_df.drop([constants.INSTANCE_STATE, constants.ID], axis=1)
                    resultant_df = resultant_df[[constants.STORE_ID,constants.SKU,constants.PRODUCT_NAME,constants.PRICE,constants.DATE]]
                    resultant_df = resultant_df.rename(columns=str.title)
                    resultant_df = resultant_df.sort_values(by=[constants.STORE_ID_TITLE])

                    return render_template(constants.RETAIL_HTML,tables=[resultant_df.to_html(index=False)], titles=[''],flag=constants.ACTION)
                else:
                    return render_template(constants.RETAIL_HTML,msg=constants.NO_RECORD_FOUND_MSG,flag=constants.NO_RECORD_FOUND)
            else:
                return render_template(constants.RETAIL_HTML, msg=constants.NO_RECORD_FOUND_FOR_DELETE,
                                       flag=constants.NO_RECORD_FOUND)

    except Exception as error:
        import traceback
        print(traceback.format_exc())
        return  render_template(constants.RETAIL_HTML,msg=constants.ERROR_MSG,flag=constants.FLAG_ERROR)


if __name__ == '__main__':
    app.run(host=constants.HOST, debug=True,port=5000)
