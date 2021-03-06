%global sname postgresql-unit
%ifarch ppc64 ppc64le
# Define the AT version and path.
%global atstring	at10.0
%global atpath		/opt/%{atstring}
%endif

Summary:	SI Units for PostgreSQL
Name:		%{sname}%{pgmajorversion}
Version:	6.0
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	https://github.com/ChristophBerg/%{sname}/archive/%{version}.tar.gz
Patch0:		%{sname}-pg%{pgmajorversion}-makefile-pgxs.patch
URL:		https://github.com/ChristophBerg/%{sname}
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
postgresql-unit implements a PostgreSQL datatype for SI units, plus byte.
The base units can be combined to named and unnamed derived units using
operators defined in the PostgreSQL type system. SI prefixes are used for
input and output, and quantities can be converted to arbitrary scale.

Requires PostgreSQL 9.5 or later (uses psprintf()), flex, and bison 3 (the
pre-built grammar files are used if only bison 2 is available).

%prep
%setup -q -n %{sname}-%{version}
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
# Install README and howto file under PostgreSQL installation directory:
install -d %{buildroot}%{pginstdir}/doc/extension
install -m 644 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/unit.so
%{pginstdir}/share/extension/unit*.sql
%{pginstdir}/share/extension/unit.control
%{pginstdir}/share/extension/unit_prefixes.data
%{pginstdir}/share/extension/unit_units.data

%changelog
* Thu Mar 22 2018 - Devrim Gündüz <devrim@gunduz.org> 6.0-1
- Update to 6.0

* Sun May 28 2017 - Devrim Gündüz <devrim@gunduz.org> 3.1-1
- Update to 3.1

* Thu Apr 27 2017 - Devrim Gündüz <devrim@gunduz.org> 3.0-1
- Update to 3.0
- Add support for Power RPMs.

* Tue Jan 10 2017 - Devrim Gündüz <devrim@gunduz.org> 2.0-1
- Update to 2.0

* Thu Sep 22 2016 - Devrim Gündüz <devrim@gunduz.org> 1.0-1
- Initial RPM packaging for PostgreSQL YUM Repository
