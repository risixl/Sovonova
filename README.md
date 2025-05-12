
---

### 📌 Notes

* Run `db_setup.py` once to initialize the database and create necessary tables.
* The database is stored locally in `cases.db` — no external database setup needed.
* You can run either `main.py` (CLI interface) or `gui.py` (Tkinter GUI).
* To ignore `.db` and Python cache files, use a `.gitignore`:

  ```gitignore
  *.db
  __pycache__/
  *.pyc
  ```
* Future enhancements you can add:

  * User authentication (login/signup)
  * Role-based access (admin, consultant, user)
  * Case history or audit log
  * Export data to CSV
  * Attachments or document uploads for cases

---
