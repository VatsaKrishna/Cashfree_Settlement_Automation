# Cashfree Settlement Automation System

## Overview

The Cashfree Settlement Automation System is a Python-based automation project developed during my Business Development internship at Vision Printt Technologies (MIMO).

The purpose of this project is to eliminate the repetitive manual process of downloading settlement reports from Cashfree and maintaining them in spreadsheets.

The system automatically fetches settlement data from the Cashfree Payment Gateway every day, processes it, removes duplicate records, and updates a Google Spreadsheet without any manual intervention.

This project was built as the foundation for a complete business intelligence pipeline that will later integrate SQL, Power BI, KPI generation and automated reporting.

---

# Business Problem

Every day the operations team had to:

* Login to Cashfree
* Open the Settlement Dashboard
* Download settlement information
* Copy the data into spreadsheets
* Keep historical records manually

This process was repetitive, time-consuming and prone to human error.

---

# Solution

This automation system performs the complete process automatically.

The workflow is:

Cashfree API

↓

Python Automation

↓

Google Sheets

↓

Business Analysis

No manual downloading or data entry is required.

---

# Features

### Current Version (Version 1)

* Automatic Cashfree API integration
* Secure authentication using Environment Variables (.env)
* Automatic "Yesterday" date detection
* Fetches daily settlement records
* Duplicate settlement detection
* Automatic Google Sheets update
* Google Service Account authentication
* Windows Task Scheduler automation
* Historical settlement storage

---

# Technologies Used

* Python
* Cashfree Payment Gateway API
* Google Sheets API
* Requests
* gspread
* python-dotenv
* Google OAuth2 Credentials
* Windows Task Scheduler

---

# Folder Structure

```
Cashfree_Settlement_Automation/

│
├── cashfree_settlement_automation.py
├── README.md
├── requirements.txt
├── .gitignore
├── .env.example
```

---

# Future Roadmap

## Version 2

Business Logic & KPI Engine

* Refund Detection
* Refund Amount
* Settlement Difference
* Difference Reason
* Weekly KPI Report
* Daily Summary Metrics
* Data Cleaning

---

## Version 3

Power BI Automation

* Automatic dashboard refresh
* Executive Dashboard
* Operational Dashboard
* Weekly Visual Reports

---

## Version 4

SQL Integration

* Store settlement history inside SQL
* Query optimisation
* Historical analysis
* Multi-table database

---

## Version 5

Business Intelligence System

* Automated KPIs
* Trend Analysis
* Revenue Insights
* Refund Analysis
* Settlement Performance

---

## Version 6

Complete Analytics Pipeline

Cashfree API

↓

Python

↓

SQL Database

↓

Data Cleaning

↓

Power BI Dashboard

↓

Automatic Email Reports

This version will function as a complete business reporting system.

---

# Skills Demonstrated

This project demonstrates practical experience with:

* Python Programming
* REST API Integration
* Google Sheets Automation
* Data Processing
* Automation
* Business Analytics
* Secure Credential Management
* Version Control (Git & GitHub)
* Problem Solving

---

# Business Impact

The automation significantly reduces manual effort by eliminating repetitive settlement downloads and spreadsheet updates.

Benefits include:

* Faster reporting
* Reduced human error
* Historical settlement tracking
* Automated daily updates
* Better decision-making through centralized data

---

# Future Improvements

* Refund Intelligence
* Settlement Prediction
* Email Notifications
* Power BI Integration
* SQL Database Migration
* Advanced Business KPI Dashboard

---

# Author

**Vatsa Krishna Raj**

Business Analytics | Automation | Python | Power BI | SQL

Developed as part of my internship at Vision Printt Technologies (MIMO).
