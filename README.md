# Assignment 06: Descriptive Statistics

## Analysis Plan

1. **Web Data Retrieval & Harmonization (`data_processing.py`):**
   - Fetches `patient_demographics.csv` and `cmp.json` directly from the course web endpoints.
   - Matches patient records and extracts serum creatinine values from CMP lab panels.
   - Computes **eGFR** and **BMI** using:
     $$\text{BMI} = \frac{\text{weight in lbs} \times 703}{(\text{height in inches})^2}$$
   - Builds a Pandas DataFrame containing **Patient Age**, **Patient Height**, **Patient Weight**, **Patient BMI**, **Patient Sex**, and **Patient eGFR**.

2. **Cohort Filtering & Descriptive Analysis (`main.ipynb`):**
   - Filters the patient DataFrame to individuals with **Patient eGFR <= 65**.
   - Generates a descriptive statistics summary table for **Patient Age**, **Patient Height**, and **Patient Weight**.
   - Categorizes patients by BMI into **Underweight** (`< 18.5`), **Normal Weight** (`18.5 - 24.9`), **Overweight** (`25 - 29.9`), and **Obese** (`>= 30`).
   - Produces three visualizations for the `eGFR <= 65` population:
     - A **bar chart** of average eGFR by BMI category.
     - A **scatter plot** of **Patient Age** (X-axis) vs. **Patient eGFR** (Y-axis).
     - A **pie chart** of **Patient Sex**.

## Setup & Execution

1. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   # Windows PowerShell:
   .venv\Scripts\Activate.ps1
   # macOS/Linux:
   source .venv/bin/activate

2. **Install Dependencies**
    pip install -r requirements.txt

3. **Run Notebook**
