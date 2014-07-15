pinax-project-pto-membership
============================

a starter project the incorporates account features from django-user-accounts and
adds features for a simple parent teacher organization membership site


Usage:

    django-admin.py startproject --template=https://github.com/paltman/pinax-project-pto-membership/zipball/master --extension=py,rst,in,sh,rc,yml,ini,coveragerc,json <project_name>

Getting Started:

    pip install virtualenv
    virtualenv mysiteenv
    source mysiteenv/bin/activate
    pip install Django==1.6.2
    django-admin.py startproject --template=https://github.com/pinax/pinax-project-pto-membership/zipball/master --extension=py,rst,in,sh,rc,yml,ini,coveragerc,json mysite
    cd mysite
    pip install -r requirements.txt
    python manage.py syncdb
    python manage.py runserver
