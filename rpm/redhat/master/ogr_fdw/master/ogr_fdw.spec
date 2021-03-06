%global sname ogr_fdw

%ifarch ppc64 ppc64le
# Define the AT version and path.
%global atstring	at10.0
%global atpath		/opt/%{atstring}
%endif

Summary:	PostgreSQL foreign data wrapper for OGR
Name:		%{sname}%{pgmajorversion}
Version:	1.0.4
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	https://github.com/pramsey/pgsql-ogr-fdw/archive/v%{version}.tar.gz
Patch0:		%{sname}-pg%{pgmajorversion}-makefile-pgxs.patch
URL:		https://github.com/pramsey/pgsql-ogr-fdw
BuildRequires:	postgresql%{pgmajorversion}-devel gdal-devel
Requires:	postgresql%{pgmajorversion}-server
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%ifarch ppc64 ppc64le
BuildRequires:	advance-toolchain-%{atstring}-devel
%endif

%description
This library contains a PostgreSQL extension, a Foreign Data Wrapper (FDW)
handler of PostgreSQL which provides easy way for interacting with OGR.

%prep
%setup -q -n pgsql-ogr-fdw-%{version}
%patch0 -p0

%build
%ifarch ppc64 ppc64le
	CFLAGS="${CFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	CXXFLAGS="${CXXFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	LDFLAGS="-L%{atpath}/%{_lib}"
	CC=%{atpath}/bin/gcc; export CC
%endif
%{__make} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

%{__install} -d %{buildroot}%{pginstdir}/
%{__install} -d %{buildroot}%{pginstdir}/bin/
%{__install} -d %{buildroot}%{pginstdir}/share/extension
%{__make} USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}

# Install README file under PostgreSQL installation directory:
%{__install} -m 755 README.md %{buildroot}%{pginstdir}/share/extension/README-%{sname}.md
%{__rm} -f %{buildroot}%{_docdir}/pgsql/extension/README.md

%clean
%{__rm} -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/share/extension/README-%{sname}.md
%attr (755,root,root) %{pginstdir}/bin/ogr_fdw_info
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}--1.0.sql
%{pginstdir}/share/extension/%{sname}.control

%changelog
* Sat Oct 14 2017 Devrim Gündüz <devrim@gunduz.org> 1.0.4-1
- Update to 1.0.4

* Sat Aug 13 2016 Devrim Gündüz <devrim@gunduz.org> 1.0.2-1
- Update to 1.0.2

* Wed Jan 06 2016 Devrim Gündüz <devrim@gunduz.org> 1.0.1-1
- Update to 1.0.1

* Mon Sep 21 2015 - Devrim Gündüz <devrim@gunduz.org> 1.0-1
- Initial RPM packaging for PostgreSQL RPM Repository
