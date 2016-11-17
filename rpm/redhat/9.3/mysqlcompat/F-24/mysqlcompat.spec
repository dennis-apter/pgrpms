%global pgmajorversion 93
%global pginstdir /usr/pgsql-9.3
%global sname mysqlcompat

Summary:	MySQL compatibility functions for PostgreSQL
Name:		%{sname}%{pgmajorversion}
Version:	0.0.7
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	http://api.pgxn.org/dist/%{sname}/%{version}/%{sname}-%{version}.zip
Patch0:		%{sname}-makefile-pgxs.patch
URL:		http://pgxn.org/dist/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch

%description
This project is a collection of functions, aggregates, operators and
casts that make PostgreSQL mimic MySQL as closely as possible.

To use the project, you can either find and install the few functions
that you need, or run all the .sql files to install the complete
compatibility environment.

This can be an immense time-saver when porting large applications that
rely heavily on certain MySQL functions.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0

%build
make USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
make  DESTDIR=%{buildroot} USE_PGXS=1 %{?_smp_mflags} install

# Install README and howto file under PostgreSQL installation directory:
install -d %{buildroot}%{pginstdir}/doc/extension
install -m 644 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%clean
%{__rm} -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/share/extension/%{sname}--%{version}.sql
%{pginstdir}/share/extension/%{sname}.control

%changelog
* Thu Oct 27 2016 - Devrim GUNDUZ <devrim@gunduz.org> 0.0.7-1
- Initial packaging for PostgreSQL RPM Repository