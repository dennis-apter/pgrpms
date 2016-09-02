%global	name pgadmin4
%global	pgadmin4instdir /usr/pgadmin4-%{version}
%global	sname pgadmin4

%if 0%{?fedora}
%global with_python3 1
%else
%global with_python3 0
%endif

# Python major version.
%{expand: %%global pyver %(python -c 'import sys;print(sys.version[0:3])')}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%if 0%{?with_python3}
%{expand: %%global py3ver %(python3 -c 'import sys;print(sys.version[0:3])')}
%endif # with_python3

Name:		%{sname}
Version:	1.0
Release:	rc1_1%{?dist}
Summary:	Management tool for the PostgreSQL
Group:		Applications/Databases
License:	PostgreSQL
URL:		http://www.pgadmin.org
Source0:	https://ftp.postgresql.org/pub/pgadmin3/pgadmin4/v1.0-rc1/src/pgadmin4-%{version}-rc1.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	mesa-libGL-devel
BuildRequires:	gcc-c++
Requires:	pgadmin4-web
%if 0%{?with_python3}
BuildRequires:	qt5-qtbase-devel >= 5.1
BuildRequires:	qt5-qtwebkit-devel
%global QMAKE	/usr/bin/qmake-qt5
%else
BuildRequires:	qt-devel >= 4.6
BuildRequires:	qtwebkit-devel
%global QMAKE	/usr/lib64/qt4/bin/qmake
%endif

%if 0%{?with_python3}
BuildRequires:	python3-devel
Requires:	python3 >= 3.3
%else
BuildRequires:	python-devel
Requires:	python >= 2.6
%endif

%if 0%{?with_python3}
Requires:	qt >= 5.1
%else
Requires:	qt >= 4.6
%endif

%description
pgAdmin 4 is a rewrite of the popular pgAdmin3 management tool for the PostgreSQL (http://www.postgresql.org) database.
pgAdmin 4 is being written as a web application in Python, using jQuery and
Bootstrap for the client side processing and UI. On the server side, Flask is
being utilised.

Although developed using web technologies, we intend for pgAdmin 4 to be usable
either on a web server using a browser, or standalone on a workstation. The
runtime/ subdirectory contains a QT based runtime application intended to allow
this - it is essentially a browser and Python interpretor in one package which
will be capable of hosting the Python application and presenting it to the user
as a desktop application.

%package	-n pgadmin4-web
Summary:	pgAdmin4 web package
BuildArch:	noarch
%if 0%{?with_python3}
Requires:	python3-babel
Requires:	python3-flask
Requires:	python3-flask-sqlalchemy
Requires:	python3-flask-wtf >= 0.11
Requires:	python3-jinja2
Requires:	python3-markupsafe
Requires:	python3-sqlalchemy
Requires:	python3-wtforms
Requires:	python3-beautifulsoup4
Requires:	python3-blinker
Requires:	python3-html5lib
Requires:	python3-itsdangerous
Requires:	python3-psycopg2
Requires:	python3-six
Requires:	python3-crypto
Requires:	python3-simplejson
Requires:	python3-dateutil
Requires:	python3-werkzeug
Requires:	python3-sqlparse
Requires:	python3-flask-babel
#Requires:  python3-speaklater
Requires:	python3-passlib
#Requires:  python3-flask-gravatar
Requires:	Flask-mail
Requires:	python3-flask-security
Requires:	python3-flask-login
Requires:	python3-flask-principal
Requires:	python3-django-htmlmin
%else
Requires:	python-babel
Requires:	python-flask
Requires:	python-flask-sqlalchemy
Requires:	python-flask-wtf => 0.11
Requires:	python-jinja2
Requires:	python-markupsafe
Requires:	python-sqlalchemy
Requires:	python-wtforms
Requires:	python-beautifulsoup4
Requires:	python-blinker
Requires:	python-html5lib
Requires:	python-itsdangerous
Requires:	python-psycopg2
Requires:	python-six
Requires:	python-crypto
Requires:	python-simplejson
Requires:	python-dateutil
Requires:	python-werkzeug
Requires:	pytz
Requires:	python-sqlparse
Requires:	python-flask-babel
#Requires:  python-speaklater
Requires:	python-passlib
#Requires:  python-flask-gravatar
Requires:	Flask-mail
Requires:	python-flask-security
Requires: 	python-flask-login
Requires:	python-flask-principal
Requires:	python-django-htmlmin
#Requires:  python-argparse
#Requires:  python-importlib
#Requires:  python-wsgiref
%endif

%if 0%{?with_python3}
%global PYTHON_SITELIB %{python3_sitelib}
%else
%global PYTHON_SITELIB %{python2_sitelib}
%endif

%description    -n pgadmin4-web
This package contains the required files to run pgAdmin4 as a web application

%prep
%setup -q -n pgadmin4-1.0-rc1/runtime

%build
cd ../runtime
export PYTHON_CONFIG=/usr/bin/python3-config
%{QMAKE} -o Makefile pgAdmin4.pro
make
#chrpath -d pgAdmin4

%install
rm -rf %{buildroot}
install -d -m 755 %{buildroot}%{pgadmin4instdir}/runtime
cp pgAdmin4 %{buildroot}%{pgadmin4instdir}/runtime
install -d -m 755 %{buildroot}%{PYTHON_SITELIB}/pgadmin4-web
cp -pR ../web/* %{buildroot}%{PYTHON_SITELIB}/pgadmin4-web
cd %{buildroot}%{PYTHON_SITELIB}/pgadmin4-web
rm -f pgadmin4.db config_local.*
echo "SERVER_MODE = False" > config_local.py
#echo "HTML_HELP = '../../../docs/en_US/html/'" >> config_local.py
#echo "
#[General]
#ApplicationPath=%{PYTHON_SITELIB}/pgadmin4-web
#PythonPath=
#" > %{buildroot}%{pgadmin4instdir}/runtime/pgadmin4.ini

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{pgadmin4instdir}/runtime/pgAdmin4
#%{pgadmin4instdir}/runtime/pgadmin4.ini

%files -n pgadmin4-web
%defattr(-,root,root,-)
%{PYTHON_SITELIB}/pgadmin4-web
%doc

%doc

%changelog
