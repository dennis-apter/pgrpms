%global	pgadmin4instdir /usr/pgadmin4-%{version}

%if 0%{?rhel} && 0%{?rhel} <= 6
%{!?systemd_enabled:%global systemd_enabled 0}
%else
%{!?systemd_enabled:%global systemd_enabled 1}
%endif

%if 0%{?fedora} > 23
%{!?with_python3:%global with_python3 1}
%global __ospython %{_bindir}/python3
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%else
%{!?with_python3:%global with_python3 0}
%global __ospython %{_bindir}/python2
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python2_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%endif

%if 0%{?with_python3}
%global PYTHON_SITELIB %{python3_sitelib}
%else
%global PYTHON_SITELIB %{python2_sitelib}
%endif

Name:		pgadmin4
Version:	1.0
Release:	rc1_3%{?dist}
Summary:	Management tool for the PostgreSQL
Group:		Applications/Databases
License:	PostgreSQL
URL:		http://www.pgadmin.org
Source0:	https://ftp.postgresql.org/pub/pgadmin3/pgadmin4/v1.0-rc1/src/pgadmin4-%{version}-rc1.tar.gz
Source1:	%{name}.conf
Source2:	%{name}.service
Source3:	%{name}.tmpfiles.d
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
%global QMAKE	/usr/bin/qmake-qt4
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
pgAdmin 4 is a rewrite of the popular pgAdmin3 management tool for the PostgreSQL
(http://www.postgresql.org) database.
pgAdmin 4 is written as a web application in Python, using jQuery and Bootstrap
for the client side processing and UI. On the server side, Flask is being utilised.

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
Requires:	python3-passlib
Requires:	python3-flask-gravatar
Requires:	python3-flask-mail
Requires:	python3-flask-security
Requires:	python3-flask-login
Requires:	python3-flask-principal
Requires:	django-htmlmin
Requires:	python3-wsgiref
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
Requires:	python-passlib
Requires:	python-flask-gravatar
Requires:	python-flask-mail
Requires:	python-flask-security
Requires: 	python-flask-login
Requires:	python-flask-principal
Requires:	django-htmlmin
Requires:	python-wsgiref
%endif

%description    -n pgadmin4-web
This package contains the required files to run pgAdmin4 as a web application

%package	-n pgadmin4-docs
Summary:	pgAdmin4 documentation
BuildArch:	noarch

%description -n pgadmin4-docs
Documentation of pgadmin4.

%prep
%setup -q -n pgadmin4-1.0-rc1/runtime

%build
cd ../runtime
%if 0%{?with_python3}
export PYTHON_CONFIG=/usr/bin/python3-config
%else
export PYTHON_CONFIG=/usr/bin/python-config
%endif
%{QMAKE} -o Makefile pgAdmin4.pro
make

%install
%{__rm} -rf %{buildroot}
install -d -m 755 %{buildroot}%{_docdir}/%{name}-docs/
%{__cp} -pr ../docs/* %{buildroot}%{_docdir}/%{name}-docs
install -d -m 755 %{buildroot}%{pgadmin4instdir}/runtime
%{__cp} pgAdmin4 %{buildroot}%{pgadmin4instdir}/runtime
install -d -m 755 %{buildroot}%{PYTHON_SITELIB}/pgadmin4-web
%{__cp} -pR ../web/* %{buildroot}%{PYTHON_SITELIB}/pgadmin4-web
install -d %{buildroot}%{_sysconfdir}/httpd/conf.d/
install -m 755 -p %{SOURCE1} %{buildroot}%{_sysconfdir}/httpd/conf.d/%{name}.conf
# Install unit file/init script
%if %{systemd_enabled}
# This is only for systemd supported distros:
install -d %{buildroot}%{_unitdir}
install -m 644 %{SOURCE2} %{buildroot}%{_unitdir}/%{name}.service
%else
# Reserved for init script
:
%endif
%if %{systemd_enabled}
# ... and make a tmpfiles script to recreate it at reboot.
mkdir -p %{buildroot}/%{_tmpfilesdir}
install -m 0644 %{SOURCE3} %{buildroot}/%{_tmpfilesdir}/pgadmin4.conf
%endif
cd %{buildroot}%{PYTHON_SITELIB}/pgadmin4-web
%{__rm} -f pgadmin4.db config_local.*
echo "SERVER_MODE = False" > config_local.py
echo "HTML_HELP = '/usr/share/doc/pgadmin4-docs/en_US/html/'" >> config_local.py
echo "
[General]
ApplicationPath=%{PYTHON_SITELIB}/pgadmin4-web
PythonPath=
" > %{buildroot}%{pgadmin4instdir}/runtime/pgadmin4.ini

%clean
%{__rm} -rf %{buildroot}

%post
if [ $1 -eq 1 ] ; then
 %if %{systemd_enabled}
   /bin/systemctl daemon-reload >/dev/null 2>&1 || :
   %systemd_post %{name}.service
   %tmpfiles_create
  %else
   :
   #chkconfig --add pgadmin4
  %endif
fi

%preun
if [ $1 -eq 0 ] ; then
%if %{systemd_enabled}
        # Package removal, not upgrade
        /bin/systemctl --no-reload disable %{name}.service >/dev/null 2>&1 || :
        /bin/systemctl stop %{name}.service >/dev/null 2>&1 || :
%else
	:
	#/sbin/service pgadmin4 condstop >/dev/null 2>&1
	#chkconfig --del pgadmin4
%endif
fi

%postun
%if %{systemd_enabled}
 /bin/systemctl daemon-reload >/dev/null 2>&1 || :
%else
 :
 #sbin/service pgadmin4 >/dev/null 2>&1
%endif
if [ $1 -ge 1 ] ; then
 %if %{systemd_enabled}
        # Package upgrade, not uninstall
        /bin/systemctl try-restart %{name}.service >/dev/null 2>&1 || :
 %else
    :
   #/sbin/service pgadmin4 condrestart >/dev/null 2>&1
 %endif
fi

%files
%defattr(-,root,root,-)
%{pgadmin4instdir}/runtime/pgAdmin4
%{pgadmin4instdir}/runtime/pgadmin4.ini

%files -n pgadmin4-web
%defattr(-,root,root,-)
%{PYTHON_SITELIB}/pgadmin4-web
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%if %{systemd_enabled}
%{_unitdir}/%{name}.service
%{_tmpfilesdir}/%{name}.conf
%endif

%files -n pgadmin4-docs
%defattr(-,root,root,-)
%doc	%{_docdir}/%{name}-docs/*

%changelog
* Sun Sep 11 2016 - Devrim Gündüz <devrim@gunduz.org> 1.0rc1-3
- Properly detect python sitelib

* Sat Sep 10 2016 - Devrim Gündüz <devrim@gunduz.org> 1.0rc1-2
- Add httpd config file, per Dave.
- Add unit file support for systemd distros.

* Fri Sep 2 2016 - Devrim Gündüz <devrim@gunduz.org> 1.0rc1-1
- Initial spec file, based on Sandeep Thakkar's spec.
