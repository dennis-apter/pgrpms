%global debug_package %{nil}

Summary:	PostgreSQL backup daemon and restore tooling for cloud object storage
Name:		pghoard
Version:	1.4.0
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	https://github.com/ohmu/%{name}/archive/%{version}.tar.gz
URL:		https://github.com/ohmu/%{name}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch
BuildRequires:	python3-devel
Requires:	python3-snappy python3-cryptography python3-boto

%description
pghoard is a PostgreSQL backup daemon and restore tooling for cloud
object storage.

Features:

 * Automatic periodic basebackups
 * Automatic transaction log (WAL/xlog) backups (using either
   pg_receivexlog, archive_command or experimental PG native
   replication protocol support with walreceiver)
 * Cloud object storage support (AWS S3, Google Cloud, OpenStack Swift,
   Azure, Ceph)
 * Backup restoration directly from object storage, compressed and
   encrypted
 * Point-in-time-recovery (PITR)
 * Initialize a new standby from object storage backups, automatically
   configured as a replicating hot-standby

%prep
%setup -q

%build

%install
%{__rm} -rf %{buildroot}
%__python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
sed -e "s@#!/bin/python@#!%{_bindir}/python@" -i %{buildroot}%{_bindir}/*
%{__install} -Dm0644 pghoard.unit %{buildroot}%{_unitdir}/pghoard.service
%{__mkdir_p} %{buildroot}%{_localstatedir}/lib/pghoard

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README.rst pghoard.json
%attr (755,root,root)  %{_bindir}/pghoard*
%attr(0755, postgres, postgres) %{_localstatedir}/lib/pghoard
%{_unitdir}/pghoard.service
%{python3_sitelib}/*
%license LICENSE

%changelog
* Mon Nov 7 2016 - Devrim Gündüz <devrim@gunduz.org> 1.4.0-1
- Initial RPM packaging for PostgreSQL RPM Repository
