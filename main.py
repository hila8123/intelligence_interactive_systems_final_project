import pandas as pd 
import algorithm1 as al1
import algorithm2 as al2
from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from flask_table import Table, Col
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials
json_key = json.load(open('creds.json')) # json credentials you downloaded earlier
sheet_id = '1xe2n0HlL3Lqphav5NLdm0bz2XncqoKUxu-w0o7lQP1c'
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('creds.json',scope) 
gc = gspread.authorize(credentials) 
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1xe2n0HlL3Lqphav5NLdm0bz2XncqoKUxu-w0o7lQP1c/edit#gid=1602661685')
def create_worksheet(number):
    if number == 0:
        wks_social = sh.get_worksheet(0)
        main_data = wks_social.get_all_values()
        headers_social = main_data.pop(0)
        songs = [x for x in range(1,31)]
        main_df = pd.DataFrame(main_data, columns=headers_social)
        # main_df.index = main_df['song_id']
        return main_df
    else:
        wks_users = sh.get_worksheet(1)
        users_data = wks_users.get_all_values()
        headers_users = users_data.pop(0)
        users_df = pd.DataFrame(users_data, columns=headers_users)
        users_df.to_csv(f'playlist.csv', index=False)
        return users_df


app = Flask(__name__)

@app.route('/', methods=['POST','GET'])
def index():
    main_df = create_worksheet(0)
    if request.method == 'POST':
        if request.form["action"] ==  "watch":
            id_content = request.form['content']
            result = search_id(id_content)
            if result:
                main_df = main_df.drop(['grade1', 'grade2'], axis=1)
                main_df['grade'] = result
                data_i = 'ID number '+id_content+' found'
                return render_template('index.html', table=main_df.to_html(index=False), data=data_i)
            else:
                data_i = 'ID number '+id_content+' not found'
                main_df = create_worksheet(0)
                return render_template('index.html', table=main_df.to_html(index=False), data=data_i)  
        elif request.form["action"] ==  "update":
            id_content = request.form.get('content')
            return redirect(url_for('update', content=id_content))
        elif request.form["action"] ==  "insert new":
            id_content = request.form.get('content')
            return redirect(url_for('insert', content=id_content))
    else:
        main_df = create_worksheet(0)
        return render_template('index.html',table=main_df.to_html(index=False))

@app.route('/update',methods=['GET','POST'])
def update():
    id_content = request.args.get('content', None)
    result = search_id(id_content)
    main_df = create_worksheet(0)
    if result:
        n = main_df.columns[1]
        main_df['grade'] = result
        data_i = 'ID number '+id_content+' found'
        return render_template('update.html', table=main_df, data=data_i,id_c=id_content)
    else:
        data_i = 'ID number '+id_content+' not found'
        main_df = create_worksheet(0)
        return render_template('index.html', table=main_df.to_html(index=False), data=data_i)


@app.route('/insert')
def insert():
    id_content = request.args.get('content', None)
    result = search_id(id_content)
    main_df = create_worksheet(0)
    if result:
        data_i = 'ID number '+id_content+' already exsist, you can update your grades by choosing UPDATE button'
        main_df = create_worksheet(0)
        return render_template('index.html', table=main_df.to_html(index=False), data=data_i)
    else:
        return render_template('insert.html', table=main_df,id_c=id_content)

@app.route('/update/submit',methods=['GET','POST'])
def update_submit():
    grades_dict = {}
    if request.method == 'POST':
        id_content = request.form.getlist('content')[0]
        for idx in range(0,30):
            grades_dict[idx+1] = int(request.form.getlist(str(idx))[0])
        insert_to_files(grades_dict,id_content,new=False)
        message = 'Update was recorded Successfuly!'
        return render_template('submit.html',message= message)
        # except:
        #     message = 'There was an issue updating your grades'
        #     return render_template('submit.html',message= message)

@app.route('/insert/submit',methods=['GET','POST'])
def insert_submit():
    grades_dict = {}
    if request.method == 'POST':
        id_content = request.form.getlist('content')[0]
        for idx in range(0,30):
            grades_dict[idx+1] = int(request.form.getlist(str(idx))[0])
        insert_to_files(grades_dict,id_content,new=True)
        message = 'new Grading was added Successfuly!'
        return render_template('submit.html',message= message)
        # except:
        #     message = 'There was an issue updating your grades'
        #     return render_template('submit.html',message= message)


def search_id(id_content):
    users_df = create_worksheet(1)
    row_id = users_df.loc[users_df['id']==id_content]
    if row_id.empty:
        return ''
    row_dict = row_id.to_dict('list')
    new_dict = {}
    for item in row_dict.items():
        if item[0] == 'id':
            continue
        else:
            new_dict[item[0]] = item[1][0]
    # new_dict = {k: v for k, v in sorted(new_dict.items(), key=lambda item: item[1])}
    return [*new_dict.values()]

def insert_to_files(grades_dict, id_content, new):
    users_df = create_worksheet(1)
    dc = {'id':id_content}
    dc.update(grades_dict)
    if not (new):
        for key in list(dc.keys())[1:]:
            users_df.loc[users_df['id'] == dc['id'], str(key)] = dc[key]
    else:
        dc = {str(x):y for x,y in dc.items()}
        users_df = users_df.append(dc,ignore_index=True)
    wks_users = sh.get_worksheet(1)
    wks_users.update([users_df.columns.values.tolist()] + users_df.values.tolist())
    update_algorithms()

def update_algorithms():
    users_df = create_worksheet(1)
    main_df = create_worksheet(0)
    first_alg_dict = al1.main()
    main_df['grade1'] = [*first_alg_dict.values()]
    second_alg_dict = al2.main()
    main_df['grade2'] = [*second_alg_dict.values()]
    wks_main = sh.get_worksheet(0)
    wks_main.update([main_df.columns.values.tolist()] + main_df.values.tolist())



if __name__ == "__main__":
    app.run(debug=True)
