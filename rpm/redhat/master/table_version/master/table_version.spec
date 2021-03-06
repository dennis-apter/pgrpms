%global debug_package %{nil}
%global sname table_version
%ifarch ppc64 ppc64le
# Define the AT version and path.
%global atstring	at10.0
%global atpath		/opt/%{atstring}
%endif

Summary:	PostgreSQL table versioning extension
Name:		%{sname}%{pgmajorversion}
Version:	1.4.2
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	https://github.com/linz/postgresql-tableversion/archive/%{version}.tar.gz
Patch0:		%{sname}-pg%{pgmajorversion}-makefile-pgxs.patch
URL:		https://github.com/linz/postgresql-tableversion/
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
PostgreSQL table versioning extension, recording row modifications and its
history. The extension provides APIs for accessing snapshots of a table at
certain revisions and the difference generated between any two given revisions.
The extension uses a PL/PgSQL trigger based system to record and provide
access to the row revisions

%prep
%setup -q -n postgresql-tableversion-%{version}
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
%{__make} DESTDIR=%{buildroot} USE_PGXS=1 %{?_smp_mflags} install
# Install README and howto file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/share/extension

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/*%{sname}.md
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc LICENSE
%else
%license LICENSE
%endif
%{pginstdir}/bin/table_version-loader
%{pginstdir}/share/extension/table_version*.sql*
%{pginstdir}/share/extension/table_version.control
%{pginstdir}/doc/extension/how_to_release.md

%changelog
* Mon Apr 9 2018 - Devrim Gündüz <devrim@gunduz.org> 1.4.2-1
- Update to 1.4.2

* Thu Feb 22 2018 - Devrim Gündüz <devrim@gunduz.org> 1.4.1-1
- Update to 1.4.1

* Sat Oct 14 2017 - Devrim Gündüz <devrim@gunduz.org> 1.3.1-1
- Update to 1.3.1

* Wed Sep 13 2017 - Devrim Gündüz <devrim@gunduz.org> 1.3.0-1
- Update to 1.3.0

* Thu May 25 2017 - Devrim Gündüz <devrim@gunduz.org> 1.1.1-1
- Update to 1.1.1

* Sun Mar 20 2016 - Devrim Gündüz <devrim@gunduz.org> 1.0.1-1
- Initial packaging for PostgreSQL RPM Repository
