%global sname	informix_fdw
%global ifxfdwmajver 0
%global ifxfdwmidver 3
%global ifxfdwminver 1

Summary:	A PostgreSQL Foreign Data Wrapper for Informix
Name:		%{sname}%{pgmajorversion}
Version:	%{ifxfdwmajver}.%{ifxfdwmidver}.%{ifxfdwminver}
Release:	1%{?dist}
Group:		Applications/Databases
License:	PostgreSQL
URL:		https://github.com/credativ/%{sname}
Source0:	https://github.com/credativ/%{sname}/archive/REL%{ifxfdwmajver}_%{ifxfdwmidver}_%{ifxfdwminver}.tar.gz
Patch0:		%{sname}-pg%{pgmajorversion}-makefile-pgxs.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:	postgresql%{pgmajorversion}-devel
BuildRequires:	postgresql%{pgmajorversion}-server
#BuildRequires:	some-informix-dependency maybe?
Requires:	postgresql%{pgmajorversion}-server

%description
The PostgreSQL Informix Foreign Datawrapper (FDW) module is a driver
for accessing remote Informix table from within PostgreSQL databases.
Foreign Tables are transparently accessed as normal PostgreSQL tables,
they can be used to join remote data against real PostgreSQL tables,
import remote data and more.

%prep
%setup -q -n %{sname}-REL%{ifxfdwmajver}_%{ifxfdwmidver}_%{ifxfdwminver}
%patch0 -p0

%build
PATH=/opt/IBM/informix/bin:$PATH INFORMIXDIR=/opt/IBM/informix USE_PGXS=1 %{__make} %{?_smp_mflags}

%install
%{__rm} -rf  %{buildroot}
USE_PGXS=1 %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%clean
%{__rm} -rf  %{buildroot}

%files
%defattr(-,root,root,-)
%doc README
%{pginstdir}/lib/*.so
%{pginstdir}/share/extension/*.sql
%{pginstdir}/share/extension/*.control

%changelog
* Thu Aug 25 2016 Devrim Gündüz <devrim@gunduz.org> 0.3.1-1
- Initial packaging for PostgreSQL RPM repository.
