## Expense Tracker
Track expenses, auto-categorize, budget alerts, multi-currency, PDF reports.

**Stack:** PostgreSQL | R2 | pandas, scikit-learn, forex-python, ReportLab

**Steps:**
1. FastAPI + SQLAlchemy + alembic
2. Expense CRUD, bulk CSV import
3. Upload receipts to R2, thumbnails with Pillow
4. Rule-based + ML categorization, feedback loop
5. Budget tracking, email alerts at 80%/100%
6. Daily forex rate updates, multi-currency
7. Generate PDF reports with charts
8. Tests (mock forex) + coverage
9. black/isort/flake8/mypy + pre-commit
10. Dockerfile + docker-compose + localstack
11. GitHub Actions → deploy Render

---