%global postgismajorversion 2.4
%global pgroutingmajorversion 2.5
%global sname	pgrouting

%ifarch ppc64 ppc64le
# Define the AT version and path.
%global atstring	at10.0
%global atpath		/opt/%{atstring}
%endif

Summary:	Routing functionality for PostGIS
Name:		%{sname}_%{pgmajorversion}
Version:	%{pgroutingmajorversion}.3
Release:	1%{dist}
License:	GPLv2
Group:		Applications/Databases
Source0:	https://github.com/pgRouting/%{sname}/archive/v%{version}.tar.gz
URL:		http://pgrouting.org/
BuildRequires:	gcc-c++
%if 0%{?rhel} && 0%{?rhel} == 7
BuildRequires:  cmake3
%else
BuildRequires:  cmake => 2.8.8
%endif
BuildRequires:	postgresql%{pgmajorversion}-devel
BuildRequires:	boost-devel >= 1.53, CGAL-devel => 4.4, gmp-devel
Requires:	postgis2_%{pgmajorversion} >= %{postgismajorversion}
Requires:	postgresql%{pgmajorversion}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%ifarch ppc64 ppc64le
BuildRequires:	advance-toolchain-%{atstring}-devel
%endif

%description
pgRouting extends the PostGIS / PostgreSQL geospatial database to
provide geospatial routing functionality.

Advantages of the database routing approach are:

- Data and attributes can be modified by many clients, like QGIS and
uDig through JDBC, ODBC, or directly using Pl/pgSQL. The clients can
either be PCs or mobile devices)
- Data changes can be reflected instantaneously through the routing
engine. There is no need for precalculation.
- The “cost” parameter can be dynamically calculated through SQL and its
value can come from multiple fields or tables.

%prep
%setup -q -n %{sname}-%{version}

%build
%ifarch ppc64 ppc64le
	CFLAGS="${CFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	CXXFLAGS="${CXXFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	LDFLAGS="-L%{atpath}/%{_lib}"
	CC=%{atpath}/bin/gcc; export CC
%endif
install -d build
cd build
%if 0%{?rhel} && 0%{?rhel} == 7
cmake3 .. \
%else
%cmake .. \
%endif
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DPOSTGRESQL_BIN=%{pginstdir}/bin \
	-DCMAKE_BUILD_TYPE=Release \
%if "%{_lib}" == "lib64"
	-DLIB_SUFFIX=64
%endif

%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

%{__make} -C build install \
	DESTDIR=%{buildroot}

%clean
%{__rm} -rf %{buildroot}

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md BOOST_LICENSE_1_0.txt
%attr(755,root,root) %{pginstdir}/lib/libpgrouting-%{pgroutingmajorversion}.so
%{pginstdir}/share/extension/%{sname}*

%changelog
* Wed Mar 21 2018 Devrim Gündüz <devrim@gunduz.org> 2.5.3-1
- Update to 2.5.3, per 3224.

* Wed Nov 29 2017 Devrim Gündüz <devrim@gunduz.org> 2.5.2-1
- Update to 2.5.2
- Remove proj and geos dependencies, they are not needed.

* Fri Oct 13 2017 Devrim Gündüz <devrim@gunduz.org> 2.5.1-1
- Update to 2.5.1 (no release needed)

* Sun Oct 1 2017 Devrim Gündüz <devrim@gunduz.org> 2.5.0-1
- Update to 2.5.0

* Wed Aug 16 2017 Devrim Gündüz <devrim@gunduz.org> 2.4.2-1
- Update to 2.4.2

* Mon Jul 3 2017 Devrim Gündüz <devrim@gunduz.org> 2.4.1-1
- Update to 2.4.1

* Wed Jan 11 2017 Devrim Gündüz <devrim@gunduz.org> 2.3.2-1
- Update to 2.3.2

* Sat Nov 26 2016 Devrim Gündüz <devrim@gunduz.org> 2.3.1-1
- Update to 2.3.1
- Update Source0 URL for this version.

* Mon Sep 26 2016 Devrim Gündüz <devrim@gunduz.org> 2.3.0-1
- Update to 2.3.0
- Update postgis dependency to 2.3

* Sat Aug 13 2016 Devrim Gündüz <devrim@gunduz.org> 2.2.4-1
- Update to 2.2.4

* Fri May 20 2016 Devrim Gündüz <devrim@gunduz.org> 2.2.3-1
- Update to 2.2.3

* Wed Apr 20 2016 Devrim Gündüz <devrim@gunduz.org> 2.2.1-1
- Update to 2.2.1
- Decrease boost dependency version to 1.53, per report from Regina.

* Tue Sep 8 2015 Devrim Gündüz <devrim@gunduz.org> 2.1.0-1
- Update to 2.1.0
- Update dependency versions
- Remove patch0, and pass PostgreSQL directory to cmake.

* Wed Oct 23 2013 Devrim Gündüz <devrim@gunduz.org> 2.0.0-1
- Update to 2.0.0

* Mon Sep 2 2013 Devrim Gündüz <devrim@gunduz.org> 2.0.0-rc1-1
- Update to 2.0.0 rc1
- Remove patch1 -- already in upstream.

* Mon Nov 12 2012 Devrim Gündüz <devrim@gunduz.org> 1.0.5-2
- Add the following features, sponsored by "Norsk institutt for skog og landskap":
 -- Add Traveling Salesperson functionality
 -- Add Driving Distance functionality
- Fix packaging issues, sponsored again by "Norsk institutt for skog og landskap".
- Update URL
- Add a new patch so that pgrouting can find PostgreSQL libs.
- Remove obsoleted patch (pgrouting-pg84.patch) -- already in upstream.
- Add a patch for 9.2, that removes quotes around LANGUAGE 'C'.

* Sat Sep 15 2012 Devrim Gündüz <devrim@gunduz.org> 1.0.5-1
- Update to 1.05

* Wed Jan 20 2010 Devrim Gündüz <devrim@gunduz.org> 1.0.3-5
- Initial import to PostgreSQL RPM repository, with very little cosmetic
  changes Thanks Peter	for sending spec to me.

* Wed Dec 09 2009 Peter HOPFGARTNER <peter.hopfgartner@r3-gis.com> - 1.0.3-4
- New build for PostGIS 1.4.

* Tue May 05 2009 Peter HOPFGARTNER <peter.hopfgartner@r3-gis.com> - 1.0.3-3
- Adapted to CentOS 5.

