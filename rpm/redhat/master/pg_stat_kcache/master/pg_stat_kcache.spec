%global sname pg_stat_kcache

%global kcachemajver 2
%global kcachemidver 0
%global kcacheminver 3

%ifarch ppc64 ppc64le
# Define the AT version and path.
%global atstring	at10.0
%global atpath		/opt/%{atstring}
%endif

Summary:	A PostgreSQL extension gathering CPU and disk acess statistics
Name:		%{sname}%{pgmajorversion}
Version:	%{kcachemajver}.%{kcachemidver}.%{kcacheminver}
Release:	2%{?dist}
License:	PostgreSQL
Group:		Applications/Databases
URL:		https://github.com/powa-team/%{sname}
Source0:	https://github.com/powa-team/%{sname}/archive/REL%{kcachemajver}_%{kcachemidver}_%{kcacheminver}.tar.gz
Patch0:		%{sname}-pg%{pgmajorversion}-makefile-pgxs.patch
BuildRequires:	postgresql%{pgmajorversion}-devel
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
Gathers statistics about real reads and writes done by the filesystem layer.
It is provided in the form of an extension for PostgreSQL >= 9.4., and
requires pg_stat_statements extension to be installed. PostgreSQL 9.4 or more
is required as previous version of provided pg_stat_statements didn't expose
the queryid field.

%prep
%setup -q -n %{sname}-REL%{kcachemajver}_%{kcachemidver}_%{kcacheminver}
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

%{__make} USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}

# Avoid conflict with some other README files:
%{__mv} %{buildroot}%{pginstdir}/doc/extension/README.rst %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.rst


%clean
%{__rm} -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/README-%{sname}.rst
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}--*.sql
%{pginstdir}/share/extension/%{sname}.control

%changelog
* Sun Apr 15 2018 - Devrim Gündüz <devrim@gunduz.org> 2.0.3-2
- Update to new URL, and use macros for version numberto avoid issues.

* Wed Oct 12 2016 - Devrim Gündüz <devrim@gunduz.org> 2.0.3-1
- Update to 2.0.3

* Fri Mar 27 2015 - Devrim Gündüz <devrim@gunduz.org> 2.0.2-1
- Update to 2.0.2

* Tue Mar 17 2015 - Devrim Gündüz <devrim@gunduz.org> 2.0.1-1
- Initial RPM packaging for PostgreSQL RPM Repository
