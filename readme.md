
# eWallet Django project
### Functionality
- It allows the user to register and login accordingly
- password reset
- Email reset
- Admin and user panel
- Tranfer funds
- See and add pals
- See account statement
- load funds into user account(specific to admin)

### Installation
- create a virtual environment
```bash
python -m venv venv
```
- Activate Virtual environment
```bash
.\venv\Scripts\Activate
```
- Django Installation
```bash
pip install django==3.2
```
- Go to project root directory
```bash
cd eWallet
```
- Make migrations
```bash
python manage.py makemigrations
```
- Migrate the migrations
```bash
python manage.py migrate
```
- Run the project
```bash
python manage.py runserver --insecure
```


