%global mod_name WTForms
%global sname wtforms

%global pgadmin4py2instdir %{python2_sitelib}/pgadmin4-web/
%global pgadmin4py3instdir %{python3_sitelib}/pgadmin4-web/

%if 0%{?fedora} > 25
%{!?with_python3:%global with_python3 1}
%global __ospython %{_bindir}/python3
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python3_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%endif

%if 0%{?rhel} == 6
%{!?with_python3:%global with_python3 1}
%global __ospython %{_bindir}/python3
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python3_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%endif

%if 0%{?rhel} == 7
%{!?with_python3:%global with_python3 0}
%global __ospython %{_bindir}/python2
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python2_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python2_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%endif

%if 0%{?with_python3}
Name:		pgadmin4-python3-%{sname}
%else
Name:		pgadmin4-python-%{sname}
%endif
Version:	2.1
Release:	3%{?dist}
Summary:	Forms validation and rendering library for python

Group:		Development/Libraries
License:	BSD
URL:		http://wtforms.simplecodes.com/
Source0:	https://pypi.python.org/packages/source/W/%{mod_name}/%{mod_name}-%{version}.zip

BuildArch:	noarch

%if 0%{?fedora} > 25
BuildRequires:	python3-devel python3-setuptools
%endif

%if 0%{?rhel} == 6
Obsoletes:	pgadmin4-python-%{sname}
BuildRequires:	python34-devel python34-setuptools
%endif

%if 0%{?rhel} == 7
BuildRequires:	python2-devel python-setuptools
%endif

%description
With wtforms, your form field HTML can be generated for you.
This allows you to maintain separation of code and presentation,
and keep those messy parameters out of your python code.

%prep
%setup -q -n %{mod_name}-%{version}
sed -i "s|\r||g" docs/html/_sources/index.txt
sed -i "s|\r||g" docs/conf.py
sed -i "s|\r||g" docs/Makefile
sed -i "s|\r||g" docs/index.rst
sed -i "s|\r||g" docs/html/_static/jquery.js
%{__rm} -f docs/html/.buildinfo

%build
%{__ospython} setup.py build

%install
%{__ospython} setup.py install -O1 --skip-build --root %{buildroot}

# Move everything under pgadmin4 web/ directory.
%if 0%{?with_python3}
%{__mkdir} -p %{buildroot}/%{pgadmin4py3instdir}
%{__mv} %{buildroot}%{python3_sitelib}/%{sname} %{buildroot}%{python3_sitelib}/%{mod_name}-%{version}-py%{pyver}.egg-info %{buildroot}/%{pgadmin4py3instdir}
%else
%{__mkdir} -p %{buildroot}/%{pgadmin4py2instdir}
%{__mv} %{buildroot}%{python2_sitelib}/%{sname} %{buildroot}%{python2_sitelib}/%{mod_name}-%{version}-py%{pyver}.egg-info %{buildroot}/%{pgadmin4py2instdir}
%endif

%files
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc docs/ LICENSE.txt PKG-INFO
%else
%license LICENSE.txt
%doc docs/ PKG-INFO
%endif
%if 0%{?with_python3}
%{pgadmin4py3instdir}/*%{mod_name}*.egg-info
%{pgadmin4py3instdir}/%{sname}
%else
%{pgadmin4py2instdir}/*%{mod_name}*.egg-info
%{pgadmin4py2instdir}/%{sname}
%endif

%changelog
* Sun Apr 8 2018 Devrim Gündüz <devrim@gunduz.org> - 2.1-3
- pgadmin4-v3 will only support Python 3.4 in EPEL on RHEL 6,
  so adjust the spec file for that.

* Mon Apr 10 2017 Devrim Gündüz <devrim@gunduz.org> - 2.1-2
- Move the components under pgadmin web directory, per #2332.
- Do a spring cleanup in the spec file.

* Tue Sep 13 2016 Devrim Gündüz <devrim@gunduz.org> - 2.1-1
- Initial packaging for PostgreSQL YUM repository, to satisfy pgadmin4 dependency.
