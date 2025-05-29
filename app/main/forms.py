# from flask import render_template, current_app, redirect, url_for
# from werkzeug.utils import secure_filename
# import os
# from app.main import main
# from flask_wtf import FlaskForm
# from wtforms import FileField, SubmitField
# from wtforms.validators import InputRequired
# import pandas as pd
# from app.main.cluster_order import cluster_data
# from app.main.cluster_rayu import cluster_data_rayu
# # from app.main.model import process_data_with_pipeline, process_data_with_pipeline2
# from flask import flash, session
# import traceback

# # Define the upload form
# class UploadFileForm(FlaskForm):
#     file = FileField("File", validators=[InputRequired()])
#     submit = SubmitField("Upload File")

# @main.route('/', methods=['GET', 'POST'])
# @main.route('/upload', methods=['GET', 'POST'])
# def upload():
#     form = UploadFileForm()
#     if form.validate_on_submit():
#         file = form.file.data
#         upload_folder = current_app.config['UPLOAD_FOLDER']
#         file_path = os.path.join(upload_folder, secure_filename(file.filename))
#         file.save(file_path)
        
#         try:
#             df=pd.read_excel(file_path, sheet_name=['Order'])
#             df['Order']
#             df=pd.read_excel(file_path, sheet_name='Order')
#             cluster_data(df)
#             df_rayu_manis=pd.read_excel(file_path, sheet_name=['Rayu Manis'])
#             df_rayu_manis['Rayu Manis']
#             df_rayu_manis=pd.read_excel(file_path, sheet_name='Rayu Manis')
#             cluster_data_rayu(df_rayu_manis)
#             return redirect(url_for('main.dashboard'))

#         except Exception as e:
#             return f"Error: {e}"
#             traceback.print_exc()
#     else:
#         # Store results in session for simplicity
#         # session['result1'] = processed_data1.head().to_html()
#         # session['result2'] = processed_data2.head().to_html()

#         # Set a success message
#         flash('error!', 'error')
#         return render_template('main/upload.html', form=form)

    