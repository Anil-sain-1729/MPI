# Employee Churn Intelligence — Full-stack ML project

Student project: frontend dashboard + FastAPI backend + Random Forest + CSV data.

## Responsible-use note
The included 1,800-row CSV is **synthetic demo data**, not actual employee records. Scores are uncertain estimates, not facts that an employee will resign. Never use this demo for firing, hiring, promotion, compensation or other adverse employment decisions. Real HR use needs lawful governance, privacy controls, fairness evaluation and human review; focus on supportive, voluntary retention programs.

## Run on Windows (Python 3.10+)
Open PowerShell in this folder:
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
uvicorn backend.main:app --reload
```
Keep that terminal open. In a second terminal, from this folder run:
```powershell
py -m http.server 5500 --directory frontend
```
Open `http://127.0.0.1:5500` in Chrome/Edge.

API docs: `http://127.0.0.1:8000/docs`
API overview: `http://127.0.0.1:8000/api/overview`

On first startup the backend trains and saves the model in `backend/artifacts/`.
## Included
- `frontend/index.html`: responsive dark dashboard, charts, model metrics and risk-estimate form
- `backend/main.py`: FastAPI endpoints, preprocessing, Random Forest training/evaluation, prediction
- `data/employee_churn_sample.csv`: 1,800 synthetic sample records
## Not yet included
SHAP integration, login/authentication, production database, tests, fairness audit and cloud deployment. The displayed indicators are simple transparent heuristics, not SHAP explanations or causal factors. Only claim what you actually run and verify in your resume.
