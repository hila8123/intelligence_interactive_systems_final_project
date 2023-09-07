from flask import Flask, request, render_template
import pandas as pd 
import csv 

app=Flask(__name__)

@app.route("/",methods=['GET','POST'])
def index():
    return render_template('index.html')

@app.route('/data', methods=['GET','POST'])
def data():
    if request.method == 'POST':
        f = request.form['csvfile']
        data = []
        with open(f) as file:
            csvfile = csv.reader(file)
            for row in csvfile:
                data.append(row)
        return render_template('data.html',data=data)

if __name__ == "__main__":
    app.run(debug=True)




# def upload_file():
#     if request.method == 'POST':
#         return jsonify({"result": request.get_array(field_name='file')})
#     return '''
#     <!doctype html>
#     <title>Upload an excel file</title>
#     <h1>Excel file upload (csv, tsv, csvz, tsvz only)</h1>
#     <form action="" method=post enctype=multipart/form-data><p>
#     <input type=file name=file><input type=submit value=Upload>
#     </form>
#     '''

# @app.route("/download", methods=['GET'])
# def download_file():
#     return excel.make_response_from_array([[1,2], [3, 4]], "csv")

# # insert database related code here

