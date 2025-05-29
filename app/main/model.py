import os
import joblib
from flask import Flask, request, jsonify, render_template

# Base directory of the project
BASE_DIR = r"C:\Users\zaky rizqullah\OneDrive\文档\skripsi kakak\skripsi2"

# pipeline_path1 = os.path.join(BASE_DIR, "app", "models", "pipeline1.pkl")
# pipeline_path2 = os.path.join(BASE_DIR, "app", "models", "combined_data_pipeline2.pkl")

# Load the pipelines
# try:
#     transform = DataTransformer()
#     print(f"Loading pipeline from: {pipeline_path1}")
#     combined_data_pipeline = joblib.load(pipeline_path1)

#     transform2 = DataTransformer()
#     print(f"Loading pipeline from: {pipeline_path2}")
#     combined_data_pipeline2 = joblib.dump(transform2,pipeline_path2)
# except FileNotFoundError as e:
#     raise FileNotFoundError(f"Pipeline file not found: {e.filename}") from e
# except Exception as e:
#     raise RuntimeError(f"Error loading pipelines: {e}")

# Example functions to process data using the pipelines
# def process_data_with_pipeline(data):
#     return combined_data_pipeline.transform(data)

# def process_data_with_pipeline2(data):
#     return combined_data_pipeline2.transform(data)