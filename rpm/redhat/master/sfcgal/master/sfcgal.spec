%ifarch ppc64 ppc64le
# Define the AT version and path.
%global atstring	at10.0
%global atpath		/opt/%{atstring}
%endif

Summary:	C++ wrapper library around CGAL for PostGIS
Name:		SFCGAL
Version:	1.3.2
Release:	1%{?dist}
License:	GLPLv2
Group:		System Environment/Libraries
Source:		https://github.com/Oslandia/%{name}/archive/v%{version}.tar.gz
URL:		http://sfcgal.org/
BuildRequires:	cmake, CGAL-devel
%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
BuildRequires:	libboost_date_time1_54_0 libboost_thread1_54_0
BuildRequires:	libboost_system1_54_0 libboost_serialization1_54_0
%endif
%else
BuildRequires:	boost-thread, boost-system, boost-date-time, boost-serialization
%endif
BuildRequires:	mpfr-devel, gmp-devel, gcc-c++
Requires:	%{name}-libs%{?_isa} = %{version}-%{release} CGAL

%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%ifarch ppc64 ppc64le
BuildRequires:	advance-toolchain-%{atstring}-devel
%endif

%description
SFCGAL is a C++ wrapper library around CGAL with the aim of supporting
ISO 19107:2013 and OGC Simple Features Access 1.2 for 3D operations.

SFCGAL provides standard compliant geometry types and operations, that
can be accessed from its C or C++ APIs. PostGIS uses the C API, to
expose some SFCGAL's functions in spatial databases (cf. PostGIS
manual).

Geometry coordinates have an exact rational number representation and
can be either 2D or 3D.

%package libs
Summary:	The shared libraries required for SFCGAL
Group:		Applications/Databases
%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%description libs
The sfcgal-libs package provides the essential shared libraries for SFCGAL.

%package devel
Summary:	The development files for SFCGAL
Group:		Development/Libraries
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

%description devel
Development headers and libraries for SFCGAL.

%prep
%setup -q

%build
%ifarch ppc64 ppc64le
	CFLAGS="${CFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	CXXFLAGS="${CXXFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	LDFLAGS="-L%{atpath}/%{_lib}"
	CC=%{atpath}/bin/gcc; export CC
%endif
%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr \
%endif
%else
%cmake \
%endif
	-D LIB_INSTALL_DIR=%{_lib} -DBoost_NO_BOOST_CMAKE=BOOL:ON .

make %{?_smp_mflags}

%install
make %{?_smp_mflags} install/fast DESTDIR=%{buildroot}

%post
%ifarch ppc64 ppc64le
%{atpath}/sbin/ldconfig
%else
/sbin/ldconfig
%endif
%post libs
%ifarch ppc64 ppc64le
%{atpath}/sbin/ldconfig
%else
/sbin/ldconfig
%endif
%postun
%ifarch ppc64 ppc64le
%{atpath}/sbin/ldconfig
%else
/sbin/ldconfig
%endif
%postun libs
%ifarch ppc64 ppc64le
%{atpath}/sbin/ldconfig
%else
/sbin/ldconfig
%endif

%files
%doc AUTHORS README.md NEWS
%license LICENSE
%{_bindir}/sfcgal-config

%files devel
%{_includedir}/%{name}/

%files libs
%{_libdir}/libSFCGAL.so*
/usr/lib/libSFCGAL.la

%changelog
* Wed Sep 13 2017 Devrim Gündüz <devrim@gunduz.org> 1.3.2-1
- Update to 1.3.2 to support CGAL >= 4.10.1 on Fedora 26+

* Wed Jul 19 2017 Devrim Gündüz <devrim@gunduz.org> 1.2.2-2
- Also Requires CGAL, per Fahar Abbas (EDB QA)

* Thu Nov 19 2015 Oskari Saarenmaa <os@ohmu.fi> 1.2.2-1
- Update to 1.2.2 to support newer CGAL versions

* Fri Oct 30 2015 Devrim Gündüz <devrim@gunduz.org> 1.2.0-1
- Initial build for PostgreSQL YUM Repository.
