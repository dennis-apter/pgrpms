%global debug_package %{nil}

%global pginstdir /usr/pgsql-%{pgpackageversion}
%global sname luapgsql

%ifarch ppc64 ppc64le
# Define the AT version and path.
%global atstring	at10.0
%global atpath		/opt/%{atstring}
%endif

%{!?luaver: %global luaver %(lua -e "print(string.sub(_VERSION, 5))")}
# for compiled modules
%global lualibdir %{_libdir}/lua/%{luaver}
# for arch-independent modules
%global luapkgdir %{_datadir}/lua/%{luaver}

Summary:	Lua binding for PostgreSQL
Name:		%{sname}
Version:	1.6.1
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	https://github.com/arcapos/%{name}/archive/%{version}.tar.gz
Patch0:		%{sname}-pg%{pgmajorversion}-makefile-pgxs.patch
URL:		https://github.com/arcapos/%{name}/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	lua-devel
BuildRequires: 	postgresql%{pgmajorversion}-devel lua-devel
Requires:	postgresql%{pgmajorversion}-server
%if 0%{?fedora} || 0%{?rhel} >= 7
Requires:	lua(abi) = %{luaver}
%else
%global luanext 5.2
Requires:	lua >= %{luaver}
Requires:	lua <  %{luanext}
%endif

%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%ifarch ppc64 ppc64le
BuildRequires:	advance-toolchain-%{atstring}-devel
%endif

%description
A Lua Binding for PostgreSQL.

%prep
%setup -q
%patch0 -p0

%build
%ifarch ppc64 ppc64le
	CFLAGS="${CFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	CXXFLAGS="${CXXFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	LDFLAGS="-L%{atpath}/%{_lib}"
	CC=%{atpath}/bin/gcc; export CC
%endif
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%clean
%{__rm} -rf %{buildroot}

%files
%doc README.md
%{lualibdir}/pgsql.so

%changelog
* Wed Nov 9 2016 - Devrim Gündüz <devrim@gunduz.org> 1.6.1-1
- Update to 1.6.1

* Sat Aug 27 2016 - Devrim Gündüz <devrim@gunduz.org> 1.6.0-1
- Initial RPM packaging for PostgreSQL RPM Repository
