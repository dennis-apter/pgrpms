%if 0%{?rhel} && 0%{?rhel} < 6
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%endif

%if 0%{?fedora} > 23
%{!?with_python3:%global with_python3 1}
%global __ospython3 %{_bindir}/python3
%{expand: %%global py3ver %(echo `%{__ospython3} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global __ospython2 %{_bindir}/python2
%{expand: %%global py2ver %(echo `%{__ospython2} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python2_sitelib %(%{__ospython2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%else
%{!?with_python3:%global with_python3 0}
%global __ospython2 %{_bindir}/python2
%{expand: %%global py2ver %(echo `%{__ospython2} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python2_sitelib %(%{__ospython2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%endif

%global sname pyrseas
%global cname Pyrseas

Summary:	Compare and synchronize PostgreSQL database schemas
Name:		python2-%{sname}
Version:	0.7.3
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	https://github.com/perseas/%{cname}/archive/v%{version}.tar.gz
URL:		https://github.com/perseas/%{cname}/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch

%description
Pyrseas provides a framework and utilities to upgrade and maintain a relational
database. Its purpose is to enhance and follow through on the concepts of the
Andromeda Project.

%if 0%{?with_python3}
%package -n python3-%{sname}
Summary:	Compare and synchronize PostgreSQL database schemas

%description -n python3-%{sname}
Pyrseas provides a framework and utilities to upgrade and maintain a relational
database. Its purpose is to enhance and follow through on the concepts of the
Andromeda Project. This is Python 3 version.
%endif

%prep
%setup -q -n %{cname}-%{version}

%build
%{__ospython2} setup.py build

%if 0%{?with_python3}
%{__ospython3} setup.py build
%endif

%install
%{__rm} -rf %{buildroot}
%{__ospython2} setup.py install --root %{buildroot}

%if 0%{?with_python3}
%{__ospython3} setup.py install --root %{buildroot}
%endif

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,755)
%doc docs/ README.rst
%{_bindir}/dbaugment
%{_bindir}/dbtoyaml
%{_bindir}/yamltodb
%{python2_sitelib}/%{cname}-%{version}-py%{py2ver}*.egg-info/*
%{python2_sitelib}/%{sname}

%if 0%{?with_python3}
%files -n python3-pyrseas
%doc docs/ README.rst
%{python3_sitelib}/%{cname}-%{version}-py%{py3ver}*.egg-info/*
%{python3_sitelib}/%{sname}
%{python3_sitelib}/%{sname}/yamltodb.py
%endif

%changelog
* Tue Nov 29 2016 - Devrim Gündüz <devrim@gunduz.org> 0.7.3-1
- Initial RPM packaging for PostgreSQL RPM Repository
