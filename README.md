# AI-Powered Credit Risk Platform

An end-to-end AI-powered Credit Risk Platform for credit risk modelling, ECL, loan decisioning, Basel capital analytics, portfolio risk, stress testing, RAG-based AI assistance, and web-based risk visualization.

## Project Objective

The objective is to build an end-to-end Credit Risk Management Platform covering:

- Probability of Default (PD)
- Credit Scorecard
- Loss Given Default (LGD)
- Exposure at Default (EAD)
- Credit Conversion Factor (CCF)
- Expected Credit Loss (ECL)
- Loan Decision Engine
- Basel / RWA / Capital Analytics
- Portfolio Risk Analytics
- Vintage Analysis
- Roll Rate Analysis
- Stress Testing
- Model Validation & Explainability
- RAG-based AI Assistant
- Web Dashboard

## End-to-End Workflow

Loan Application
        ↓
Data Collection
        ↓
Data Validation & Storage
        ↓
Data Preprocessing
        ↓
Feature Engineering
        ↓
PD Model
        ↓
Credit Scorecard
        ↓
LGD Model
        ↓
EAD / CCF Model
        ↓
ECL Engine
        ↓
Risk Classification
        ↓
Decision Engine
        ↓
Basel / RWA / Capital
        ↓
Portfolio Risk Analysis
        ↓
Vintage Analysis
        ↓
Roll Rate Analysis
        ↓
Stress Testing
        ↓
Model Validation & Explainability
        ↓
Dashboard + RAG AI Assistant
        ↓
Final Integrated Platform

## Core Credit Risk Modules

### Probability of Default (PD)

Estimate the probability that a borrower will default.

Main activities:

- Default target definition
- Logistic Regression
- Model development
- Model validation
- PD calibration
- Benchmark comparison

### Credit Scorecard

Convert borrower risk characteristics into a credit score.

Main activities:

- Variable binning
- Weight of Evidence (WoE)
- Information Value (IV)
- Variable selection
- Score scaling
- Risk bands

### Loss Given Default (LGD)

Estimate the percentage of exposure expected to be lost after default.

LGD = 1 - Recovery Rate

### Exposure at Default (EAD) / CCF

Estimate exposure outstanding at the time of default.

EAD = Outstanding Exposure + CCF × Undrawn Commitment

### Expected Credit Loss (ECL)

Calculate expected credit loss using:

ECL = PD × LGD × EAD

The ECL engine will also include IFRS 9 staging logic.

### Loan Decision Engine

Convert model outputs into lending decisions:

- Approve
- Reject
- Manual Review

Decisioning can use PD, score, ECL, risk category and configurable business rules.

### Basel / Capital Analytics

The Basel component will cover:

- Asset correlation
- Risk Weight
- Risk Weighted Assets (RWA)
- Capital Requirement
- Capital impact under stress

### Portfolio Risk Analytics

Portfolio-level analysis will include:

- Total Exposure
- Total ECL
- Average PD
- Default Rate
- Risk Distribution
- Segment Risk
- Geography Risk
- Concentration Risk

### Vintage Analysis

Analyse portfolio performance by loan origination cohorts.

### Roll Rate Analysis

Track movement between delinquency buckets.

Current
   ↓
30 DPD
   ↓
60 DPD
   ↓
90+ DPD

### Stress Testing

Scenario-based analysis:

Base Scenario
      ↓
Moderate Stress
      ↓
Severe Stress

Evaluate impact on:

- PD
- LGD
- EAD
- ECL
- RWA
- Capital Requirement

### Model Validation & Explainability

Validation will cover appropriate model performance, calibration, stability and explainability checks.

Examples:

- AUC
- Gini
- KS
- Calibration
- MAE
- RMSE
- R²
- PSI
- Feature / population drift
- Reason Codes
- SHAP / Feature Importance

## System Architecture

USER
  ↓
WEB APPLICATION
  ↓
FASTAPI
  ↓
POSTGRESQL
  ↓
┌─────────────────────┬─────────────────────┐
↓                     ↓
CREDIT RISK CORE      RAG AI
↓                     ↓
PD                    Retrieval
LGD                   ↓
EAD                   LLM
ECL                   ↓
Decision              AI Answer
Basel
Portfolio
Stress Testing
↓
Final Risk Outputs
↓
Dashboard / UI

## Technology Stack

### Data & Machine Learning

- Python
- Pandas
- NumPy
- SciPy
- Scikit-learn
- Matplotlib
- Seaborn
- Jupyter

### Backend

- FastAPI

### Database

- PostgreSQL

### Frontend

- React

### RAG / AI

- LangChain
- Embeddings
- ChromaDB
- LLM

### Deployment

- Docker

## Project Structure

AI_CREDIT_RISK_PLATFORM/
│
├── data/
├── notebooks/
├── preprocessing/
├── feature_engineering/
├── models/
│
├── credit_risk/
│   ├── pd/
│   ├── scorecard/
│   ├── lgd/
│   ├── ead/
│   ├── ecl/
│   └── basel/
│
├── decision_engine/
├── portfolio/
├── vintage/
├── roll_rate/
├── stress_testing/
│
├── database/
├── api/
├── tests/
├── config/
│
├── rag/
├── frontend/
│
├── .gitignore
├── requirements.txt
└── README.md

## Team Responsibilities

### Asmit Singh — Credit Risk Core

Responsible for:

- Data Foundation
- Data Validation
- Data Preprocessing
- Feature Engineering
- PD Model
- Credit Scorecard
- LGD Model
- EAD / CCF Model
- ECL Engine
- Decision Engine
- Basel / RWA / Capital
- Portfolio Risk Analysis
- Vintage Analysis
- Roll Rate Analysis
- Stress Testing
- Model Validation
- Model Explainability
- Integration-ready model outputs

### Ankit Manjhi — Dashboard / Web Application

Responsible for:

- React Frontend
- Dashboard
- Customer Risk View
- Portfolio Risk View
- Basel View
- Stress Testing View
- Web Interface

### Kashif Iqubal — Major Supporting / Integration Work

Responsible for:

- Major supporting work
- Integration-related responsibilities
- Assigned platform components

### Salik Ubair — RAG AI Assistant

Responsible for:

- Document ingestion
- Document processing
- Chunking
- Embeddings
- Vector storage
- Retrieval
- LLM integration
- Source-grounded AI responses

### Spandan Behera

Supporting project work as assigned.

### Amardeep Kumar

Supporting project work as assigned.

## Development Principle

Each module should remain modular and integration-ready.

Input
  ↓
Processing / Model
  ↓
Output

Credit Risk modules should remain independent from the frontend.

The outputs should be structured so they can later be consumed through:

Python Credit Risk Modules
          ↓
       FastAPI
          ↓
    React Dashboard

and stored or retrieved through SQL.

## Credit Risk Development Flow

DATA
  ↓
DATA VALIDATION
  ↓
PREPROCESSING
  ↓
FEATURE ENGINEERING
  ↓
PD
  ↓
SCORECARD
  ↓
LGD
  ↓
EAD / CCF
  ↓
ECL
  ↓
DECISION ENGINE
  ↓
BASEL
  ↓
PORTFOLIO
  ↓
VINTAGE
  ↓
ROLL RATE
  ↓
STRESS TESTING
  ↓
MODEL VALIDATION
  ↓
EXPLAINABILITY
  ↓
API-READY OUTPUT

## Dashboard & RAG Integration

CREDIT RISK MODULES
        ↓
CLEAN RISK OUTPUTS
        ↓
API / DATABASE
        ↓
┌───────────────────┬───────────────────┐
↓                   ↓
REACT DASHBOARD     RAG AI
↓                   ↓
VISUAL RISK VIEW    AI RISK ASSISTANT
        └───────────┬───────────┘
                    ↓
             FINAL PLATFORM

## Git / Collaboration Workflow

GITHUB REPOSITORY
        ↓
┌──────────────────┬──────────────────┐
↓                  ↓                  ↓
CREDIT RISK        RAG        FRONTEND
                           
        └──────────┬──────────┘
                   ↓
            FINAL INTEGRATION

Each team member can develop their assigned module independently.

The project will use modular code, clean interfaces and defined inputs/outputs so independently developed modules can be integrated later.

## Development Phases

### Phase 1 — Project Foundation

- [x] Project folder structure
- [x] Python virtual environment
- [x] Basic data/ML libraries
- [x] Git repository
- [x] .gitignore
- [x] README

### Phase 2 — Data Foundation

- [ ] Dataset Selection
- [ ] Data Understanding
- [ ] Data Dictionary
- [ ] Database Schema
- [ ] Data Validation
- [ ] Data Storage

### Phase 3 — Data Preparation

- [ ] Data Cleaning
- [ ] Missing Value Treatment
- [ ] Outlier Treatment
- [ ] Encoding
- [ ] Feature Engineering
- [ ] Model-Ready Dataset

### Phase 4 — Credit Risk Modelling

- [ ] PD Model
- [ ] PD Validation
- [ ] PD Calibration
- [ ] Credit Scorecard
- [ ] WoE
- [ ] IV
- [ ] Risk Bands
- [ ] LGD Model
- [ ] EAD / CCF Model
- [ ] ECL Engine

### Phase 5 — Risk & Regulatory Analytics

- [ ] Decision Engine
- [ ] Basel Risk Weight
- [ ] RWA
- [ ] Capital Requirement
- [ ] Portfolio Risk
- [ ] Vintage Analysis
- [ ] Roll Rate Analysis
- [ ] Concentration Analysis

### Phase 6 — Stress Testing & Validation

- [ ] Base Scenario
- [ ] Moderate Stress
- [ ] Severe Stress
- [ ] PD Stress
- [ ] LGD Stress
- [ ] EAD Stress
- [ ] ECL Stress
- [ ] Capital Impact
- [ ] Model Validation
- [ ] Explainability

### Phase 7 — Final Integration

- [ ] FastAPI Integration
- [ ] React Dashboard Integration
- [ ] RAG Integration
- [ ] End-to-End Testing
- [ ] Docker Deployment
- [ ] Final Documentation

## Current Project Status

Project Structure        ✅
Python Environment       ✅
Virtual Environment      ✅
Basic ML Libraries       ✅
Git Repository           ✅
.gitignore               ✅
README                   ✅

NEXT:

Dataset Selection
      ↓
Data Understanding
      ↓
Data Dictionary
      ↓
Database Design
      ↓
Preprocessing

## Final Project Goal

Customer / Loan Data
        ↓
Credit Risk Models
        ↓
PD + Scorecard + LGD + EAD
        ↓
ECL
        ↓
Decision
        ↓
Basel / Capital
        ↓
Portfolio Risk
        ↓
Stress Testing
        ↓
Dashboard + RAG
        ↓
Complete Credit Risk Platform

## Project Status

Current Stage: Project Foundation Completed

Next Stage: Dataset Selection & Data Understanding