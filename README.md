# apteka_bonus
Bonus system for Apteka

$pip install -r requirements.txt

$python manage.py makemigrations

$python manage.py migrate

#Для синхронизацие forms с SQL если ошибка у вас "NO SUCH TABLE <<accounts_user>> "
$python manage.py migrate --run-syncdb
