# Expense-and-Budget-Analytics-Dashboard-Using-Python
 monitor budget utilization, detect overspending, and make informed cost-control decisions.
# Budget & Expense Analytics Project

## Important data note
The included `data/budget.csv` and `data/expenses.csv` are **synthetic demonstration data** created solely to make the notebook and dashboard runnable. They are not actual company records. The assignment says not to fabricate findings; therefore, do not present any demo numbers or patterns as real business findings. Replace both CSV files with authorized, verified company records and rerun the analysis before final submission.

## Project files
- `data/budget.csv` — approved budget by month, department, and expense category.
- `data/expenses.csv` — actual expense by the same keys.
- `budget_expense_analysis.ipynb` — data cleaning, merge, KPIs, analysis, charts, alerts, and exports.
- `app.py` — interactive Streamlit dashboard with filters, KPIs, charts, alerts, and CSV export.
- `final_report.pdf` — report structure, methodology, demo-only observations, and recommendations.
- `README.md` — setup and run instructions.

## Setup
Use Python 3.10 or newer. Open a terminal in the project folder.

Windows:
```powershell
py -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If `py` is not recognized but `python` is installed, use `python -m venv .venv`.

## Run dashboard
```powershell
streamlit run app.py
```
Streamlit will show a local URL, usually `http://localhost:8501`. Open it in your browser.

## Run notebook
```powershell
jupyter notebook budget_expense_analysis.ipynb
```
Run all cells from top to bottom. The notebook writes `analysis_output.csv`, `department_summary.csv`, and `category_summary.csv` to the project folder.

## Expected CSV schemas
`budget.csv`: `Month`, `Department`, `Expense_Category`, `Approved_Budget`, `Currency`
`expenses.csv`: `Month`, `Department`, `Expense_Category`, `Actual_Expense`, `Currency`

- `Month` should use `YYYY-MM` format.
- Use the same currency and consistent department/category labels in both files.
- Remove employee names, account numbers, or other confidential personal information.
- The join keys are Month + Department + Expense_Category.
- Duplicate rows are aggregated before joining.
- Missing budget or expense combinations are retained as zero on the absent side. Review unmatched combinations before drawing conclusions.

## KPI definitions
- Variance = Approved Budget − Actual Expense. Positive means under budget; negative means over budget.
- Utilization (%) = Actual Expense / Approved Budget × 100, where approved budget is greater than zero.
- Over budget = Actual Expense > Approved Budget.

## Dataset/source statement
No real company dataset was supplied with the assignment image. For this reason, this package includes synthetic demo data and makes no claim that it represents a real company. For the submitted, evidence-based version, cite the source of the actual budget and expense records supplied by the organization, including extraction date and any cleaning/aggregation steps. Do not cite this demo data as an external source.

## Before final submission
1. Replace the synthetic CSVs with approved, real data.
2. Confirm that totals and currency match the source system.
3. Inspect unmatched merge keys and missing values.
4. Rerun the notebook and dashboard.
5. Update the report with at least five findings and three recommendations supported by the real output.
6. Test `streamlit run app.py` and notebook execution without errors.
