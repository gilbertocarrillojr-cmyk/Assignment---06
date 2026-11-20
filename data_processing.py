import pandas as pd
import requests

DEMOGRAPHICS_URL = "https://ruby.ils.unc.edu/~kibria/chip705_2026_fall/patient_demographics.csv"
CMP_URL = "https://ruby.ils.unc.edu/~kibria/chip705_2026_fall/cmp.json"


def fetch_demographics(url: str = DEMOGRAPHICS_URL) -> pd.DataFrame:
    """Fetch patient demographics CSV from the web."""
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    from io import StringIO
    return pd.read_csv(StringIO(response.text))


def fetch_cmp(url: str = CMP_URL) -> dict:
    """Fetch comprehensive metabolic panel (CMP) JSON from the web."""
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.json()


def calculate_egfr(sex: str, age: float, creatinine: float) -> float:
    """Calculate eGFR using the 2021 CKD-EPI creatinine equation."""
    c = 142
    k = 0.7 if sex == "F" else 0.9
    a = -0.241 if sex == "F" else -0.302

    scr_over_k = creatinine / k
    low = min(scr_over_k, 1.0)
    high = max(scr_over_k, 1.0)

    egfr = c * (low ** a) * (high ** -1.200) * (0.9938 ** age)
    if sex == "F":
        egfr *= 1.012
    return egfr


def calculate_bmi(weight_lbs: float, height_inches: float) -> float:
    """Calculate BMI using weight (lbs) and height (inches)."""
    return (weight_lbs * 703) / (height_inches ** 2)


def extract_creatinine(panels: list) -> float | None:
    """Extract serum Creatinine value from a patient's CMP panel list."""
    for panel in panels:
        if panel.get("measure") == "Creatinine":
            return float(panel["patient_measure"])
    return None


def build_patient_dataframe(
    demo_url: str = DEMOGRAPHICS_URL,
    cmp_url: str = CMP_URL,
) -> pd.DataFrame:
    """Harmonize web demographics and CMP data into the required DataFrame."""
    df_demo = fetch_demographics(demo_url)
    cmp_data = fetch_cmp(cmp_url)

    records = []
    for _, row in df_demo.iterrows():
        patient_id = str(row["patient_id"])
        if patient_id not in cmp_data:
            continue

        creatinine = extract_creatinine(cmp_data[patient_id])
        if creatinine is None:
            continue

        sex = row["sex"]
        age = float(row["age"])
        height = float(row["height_inches"])
        weight = float(row["weight_lbs"])

        records.append({
            "Patient Age": age,
            "Patient Height": height,
            "Patient Weight": weight,
            "Patient BMI": calculate_bmi(weight, height),
            "Patient Sex": sex,
            "Patient eGFR": calculate_egfr(sex, age, creatinine),
        })

    return pd.DataFrame(
        records,
        columns=[
            "Patient Age",
            "Patient Height",
            "Patient Weight",
            "Patient BMI",
            "Patient Sex",
            "Patient eGFR",
        ],
    )