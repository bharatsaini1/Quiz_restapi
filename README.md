# Django REST API Deployment on PythonAnywhere

## Overview
This README explains how to deploy your Django REST API to PythonAnywhere, a hosting platform for Python web applications.

---

## Prerequisites
- A PythonAnywhere account ([Sign up here](https://www.pythonanywhere.com/))
- A Django project ready for deployment
- Basic knowledge of Django and Python

---

## Deployment Steps

### Step 1: Prepare Your Django Project
1. Update `ALLOWED_HOSTS` in `settings.py`:
   ```python
   ALLOWED_HOSTS = ['yourusername.pythonanywhere.com']
   ```

2. Set `DEBUG = False`:
   ```python
   DEBUG = False
   ```

3. Collect static files:
   ```bash
   python manage.py collectstatic
   ```

4. Export dependencies:
   ```bash
   pip freeze > requirements.txt
   ```

5. Compress the project into a `.zip` file for easier upload.

---

### Step 2: Upload Your Project to PythonAnywhere
1. Log in to your PythonAnywhere account.
2. Go to the **Files** tab and navigate to `/home/yourusername/`.
3. Upload the `.zip` file containing your project.
4. Extract the uploaded file.

---

### Step 3: Set Up a Virtual Environment
1. Open a new Bash console in the **Consoles** tab.
2. Create a virtual environment:
   ```bash
   python3.9 -m venv myenv
   ```

3. Activate the virtual environment:
   ```bash
   source myenv/bin/activate
   ```

4. Install dependencies:
   ```bash
   pip install -r /home/yourusername/yourproject/requirements.txt
   ```

---

### Step 4: Configure the Web App
1. Go to the **Web** tab and add a new web app.
2. Choose **Manual Configuration** and select your Python version.
3. Configure the virtual environment in the **Virtualenv** section:
   ```
   /home/yourusername/myenv
   ```
4. Edit the WSGI file to point to your Django project:
   ```python
   import os
   import sys

   project_home = '/home/yourusername/yourproject'
   if project_home not in sys.path:
       sys.path.append(project_home)

   os.environ['DJANGO_SETTINGS_MODULE'] = 'yourproject.settings'

   from django.core.wsgi import get_wsgi_application
   application = get_wsgi_application()
   ```
5. Reload the web app.

---

### Step 5: Database Setup
1. If using a database other than SQLite, configure it in the **Databases** tab.
2. Update the database settings in `settings.py`:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'yourusername$databasename',
           'USER': 'yourusername',
           'PASSWORD': 'yourpassword',
           'HOST': 'yourusername.mysql.pythonanywhere-services.com',
       }
   }
   ```
3. Apply migrations:
   ```bash
   python manage.py migrate
   ```

---

### Step 6: Configure Static Files
1. Add a **Static files** mapping in the Web tab:
   - URL: `/static/`
   - Path: `/home/yourusername/yourproject/static/`
2. Ensure static files are collected:
   ```bash
   python manage.py collectstatic
   ```

---

### Step 7: Test and Debug
1. Visit your API at `yourusername.pythonanywhere.com`.
2. Check error logs in the Web tab if any issues arise.

---

### Optional: Secure Your API
PythonAnywhere automatically provides HTTPS for its subdomains.

---

## Notes
- Ensure your API endpoints are working locally before deploying.
- Use PythonAnywhere's **Log Files** for troubleshooting.
- For large-scale apps, consider upgrading your plan for better resources.

---
