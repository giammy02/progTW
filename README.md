# ProgTecWeb
Progetto d'esame di Tecnologie Web 2024
# PlayPadel
Applicazione web sviluppata con Django per la prenotazione 
in vari impianti di campi da padel e tracciamento delle partite
dei vari utenti registrati.
## Eseguire il progetto in locale
Clonare la repository in locale:

```bash
git clone https://github.com/giammy02/progTW.git
```

Installare i requisiti necessari (possibilmente su ambiente virtuale):

```bash
pipenv install -r requirements.txt
```

Creare il database:

```bash
python manage.py migrate
```

Infine, eseguire il server:

```bash
python manage.py runserver
```

L'applicazione web sarà disponibile all'indirizzo **127.0.0.1:8000**.
