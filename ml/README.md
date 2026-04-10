# Machine Learning Module

This folder contains the complete machine learning workflow for the **Sales Forecasting Platform** project.

The goal of this module is to prepare the sales data, build a forecasting model, evaluate its performance, and save the trained artifacts so they can later be used in the backend API and frontend dashboard.

## Overview

In this project, the machine learning pipeline is focused on predicting **store sales** using the **Rossmann Store Sales** dataset.

The workflow was built step by step using Jupyter notebooks so the entire process remains easy to understand, inspect, and improve.

The ML process includes:

- data exploration
- data cleaning
- feature engineering
- model training
- model evaluation
- prediction testing
- saving trained artifacts

## Folder Structure

text
ml/
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_preprocessing.ipynb
│   ├── 03_feature_engineering.ipynb
│   ├── 04_model_training.ipynb
│   ├── 05_model_evaluation.ipynb
│   └── 06_prediction_testing.ipynb
│
├── data/
│   ├── raw/
│   │   ├── train.csv
│   │   └── store.csv
│   └── processed/
│       ├── cleaned_train.csv
│       └── featured_train.csv
│
├── artifacts/
│   ├── model.pkl
│   ├── columns.pkl
│   └── metrics.json
│
└── README.md