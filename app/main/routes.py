from flask import render_template, request, current_app, send_from_directory
from flask import redirect, url_for, session
from werkzeug.utils import secure_filename
import json 
import os
import pandas as pd
from app.main import main
# from app.main.forms import UploadFileForm
# from app.main.model import process_data_with_pipeline, process_data_with_pipeline2
from flask import flash

# @main.route('/', methods=['GET', 'POST'])
# def upload_and_process():   
#     form = UploadFileForm()
#     if form.validate_on_submit():
#         file = form.file.data
#         upload_folder = current_app.config['UPLOAD_FOLDER']
#         file_path = os.path.join(upload_folder, secure_filename(file.filename))
#         file.save(file_path)

#         # Load the file and apply pipelines
#         # try:
#         #     df = pd.read_excel(file_path)
#         #     processed_data1 = process_data_with_pipeline(df)
#         #     processed_data2 = process_data_with_pipeline2(df)
#         # except Exception as e:
#         #     return f"Error: {e}"

#         # Store results in session for simplicity
#         # session['result1'] = processed_data1.head().to_html()
#         # session['result2'] = processed_data2.head().to_html()

#         # Set a success message
#         flash('File uploaded successfully!', 'success')

#         # # Redirect to the results page
#         # return redirect(url_for('show_results'))

#     return render_template('main/upload.html', form=form)


# @main.route('/table1')
# def table1():
#     result1 = session.get('result1')
#     result2 = session.get('result2')

#     if not result1 or not result2:
#         return "No results available. Please upload a file first.", 400

#     return render_template('main/table_order.html', result1=result1, result2=result2)

# @main.route('/download/<filename>')
# def download_file(filename):
#     return send_from_directory('static/files', filename, as_attachment=True)


import os

@main.route('/')
@main.route('/excel')
def excel():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, '..', '..', 'app', 'static', 'files', 'Teras Rayu (cleaned_2).xlsx')
    file_path = os.path.abspath(file_path)

    sheet_order = pd.read_excel(file_path, sheet_name="Order")
    sheet_rayu = pd.read_excel(file_path, sheet_name="Rayu Manis")  

    table_order = sheet_order.to_html(classes='table-custom', index=False, border=0)
    table_rayu = sheet_rayu.to_html(classes='table-custom', index=False, border=0)

    return render_template("main/excel.html", table_order=table_order, table_rayu=table_rayu)


# @main.route('/')
# @main.route('/excel')
# def excel():
#     file_path = os.path.join(os.getcwd(), 'app', 'static', 'files', 'Teras Rayu (cleaned_2).xlsx')
#     df = pd.read_excel(file_path, sheet_name="Order")
#     table_html = df.to_html(classes='table-custom', index=False, border=0)
#     return render_template("main/excel.html", table=table_html)


# @main.route("/excel")
# def excel():
#     # Baca file Excel (pastikan sesuai nama dan sheet-nya)
#     df = pd.read_excel("app/static/files/Teras Rayu (cleaned 2).xlsx", sheet_name="Order")  # kamu bisa tambahkan sheet_name="Sheet1" jika perlu
#     # Convert DataFrame ke HTML
#     table_html = df.to_html(classes='table table-striped', index=False, border=0)
#     return render_template("main/excel.html", table=table_html)

# @main.route('/')
# def home():
#     return excel()

# @main.route('/excel1')
# def excel1():
#     file_path = os.path.join(current_app.root_path, "static/files/Teras Rayu (cleaned 2).xlsx")
#     if not os.path.exists(file_path):
#         return "File Excel tidak ditemukan di path: " + file_path

#     try:
#         df = pd.read_excel(file_path, sheet_name="Order")
#         print(df.head())  # Lihat di terminal/log
#         table_html = df.to_html(classes='table table-striped', index=False, border=0)
#         return render_template("main/excel1.html", table=table_html)
#     except Exception as e:
#         return f"Terjadi error saat membaca file Excel: {e}"


@main.route('/dashboard')
def dashboard():
    with open(os.path.join(os.getcwd(), 'app', 'static', 'data', 'present.json'), 'r') as json_file:
        data = json.load(json_file) 
    with open(os.path.join(os.getcwd(), 'app', 'static', 'data', 'present_rm.json'), 'r') as json_file1:
        data1 = json.load(json_file1) 
    with open(os.path.join(os.getcwd(), 'app', 'static', 'data', 'cluster.json'), 'r') as json_file2:
        data2 = json.load(json_file2) 
    with open(os.path.join(os.getcwd(), 'app', 'static', 'data', 'cluster_rm.json'), 'r') as json_file3:
        data3 = json.load(json_file3) 
    return render_template('main/dashboard.html', data=data, data1=data1, data2=data2, data3=data3)

@main.route('/dashboard1')
def dashboard1():
    with open(os.path.join(os.getcwd(), 'app', 'static', 'data', 'present.json'), 'r') as json_file:
        data = json.load(json_file) 
    with open(os.path.join(os.getcwd(), 'app', 'static', 'data', 'cluster.json'), 'r') as json_file2:
        data2 = json.load(json_file2) 
    return render_template('main/cluster_order.html', data=data, data2=data2)

@main.route('/dashboard2')
def dashboard2():
    with open(os.path.join(os.getcwd(), 'app', 'static', 'data', 'present_rm.json'), 'r') as json_file1:
        data1 = json.load(json_file1) 
    with open(os.path.join(os.getcwd(), 'app', 'static', 'data', 'cluster_rm.json'), 'r') as json_file3:
        data3 = json.load(json_file3) 
    return render_template('main/cluster_rm.html', data1=data1, data3=data3)

@main.route('/table1')
def table1():
    with open(os.path.join(os.getcwd(), 'app', 'static', 'data', 'merged.json'), 'r') as json_file4:
        merged_data1 = json.load(json_file4) 
    return render_template('main/table_order.html', merged_data1=merged_data1)

@main.route('/table2')
def table2():
    with open(os.path.join(os.getcwd(), 'app', 'static', 'data', 'merged_rm.json'), 'r') as json_file5:
        merged_data2 = json.load(json_file5) 
    return render_template('main/table_rm.html', merged_data2=merged_data2)