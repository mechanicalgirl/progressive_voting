There's a brief description of the project in the repo wiki:

https://github.com/mechanicalgirl/progressive_voting/wiki


Create a virtual environment:
-----------------------------

```python3
cd ~/path/to/progressive_voting/
virtualenv venv
source venv/bin/activate
```

To run locally:
---------------

```python3
cd ~/path/to/progressive_voting/
source venv/bin/activate
pip install -r requirements.txt
cd voting
python3 manage.py migrate
python3 manage.py runserver
```

To create a superuser (for admin access):
-----------------------------------------

```python3
cd ~/path/to/progressive_voting/voting
python3 manage.py createsuperuser
```

To view:
------------------

    Admin:           http://127.0.0.1:8000/admin/
    Main:            http://127.0.0.1:8000/
