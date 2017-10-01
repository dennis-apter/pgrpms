%global		sname geos
%global		geosinstdir /usr/%{sname}-36

Name:		%{sname}36
Version:	3.6.2
Release:	1%{?dist}
Summary:	GEOS is a C++ port of the Java Topology Suite

Group:		Applications/Engineering
License:	LGPLv2
URL:		http://trac.osgeo.org/geos/
Source0:	http://download.osgeo.org/%{sname}/%{sname}-%{version}.tar.bz2
Patch0:		%{name}-gcc43.patch

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	doxygen libtool
BuildRequires:	python-devel
BuildRequires:	gcc-c++

%global __ospython %{_bindir}/python2
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python2_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python2_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")


%description
GEOS (Geometry Engine - Open Source) is a C++ port of the Java Topology
Suite (JTS). As such, it aims to contain the complete functionality of
JTS in C++. This includes all the OpenGIS "Simple Features for SQL" spatial
predicate functions and spatial operators, as well as specific JTS topology
functions such as IsValid()

%package devel
Summary:	Development files for GEOS
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
GEOS (Geometry Engine - Open Source) is a C++ port of the Java Topology
Suite (JTS). As such, it aims to contain the complete functionality of
JTS in C++. This includes all the OpenGIS "Simple Features for SQL" spatial
predicate functions and spatial operators, as well as specific JTS topology
functions such as IsValid()

This package contains the development files to build applications that
use GEOS

%package python
Summary:	Python modules for GEOS
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
BuildRequires:	swig

%description python
Python module to build applications using GEOS and python

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0

%build

# fix python path on 64bit
sed -i -e 's|\/lib\/python|$libdir\/python|g' configure
sed -i -e 's|.get_python_lib(0|.get_python_lib(1|g' configure

# disable internal libtool to avoid hardcoded r-path
for makefile in `find . -type f -name 'Makefile.in'`; do
sed -i 's|@LIBTOOL@|%{_bindir}/libtool|g' $makefile
done

./configure --prefix=/usr/%{sname}-36 --disable-static --disable-dependency-tracking --enable-python
# Touch the file, since we are not using ruby bindings anymore:
# Per http://lists.osgeo.org/pipermail/geos-devel/2009-May/004149.html
touch swig/python/geos_wrap.cxx

%{__make} %{?_smp_mflags}

# Make doxygen documentation files
cd doc
%{__make} doxygen-html

%install
%{__rm} -rf %{buildroot}
%{__make} DESTDIR=%{buildroot} install

%check

# test module
%{__make} %{?_smp_mflags} check || exit 0

%clean
%{__rm} -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS README TODO
%{geosinstdir}/lib/libgeos-%{version}.so
#%{geosinstdir}/lib64/libgeos_c.so.*
#%exclude %{geosinstdir}/lib64/*.a

%files devel
%defattr(-,root,root,-)
%doc doc/doxygen_docs
%{geosinstdir}/bin/geos-config
%{geosinstdir}/include/*
%{geosinstdir}/lib/libgeos.so*
%{geosinstdir}/lib/libgeos_c.so*
%exclude %{geosinstdir}/lib/*.a
%exclude %{geosinstdir}/lib/*.la

%files python
%defattr(-,root,root,-)
%defattr(-,root,root,-)
%dir %exclude %{geosinstdir}/
%dir %{geosinstdir}/lib64/python%{pyver}/site-packages/%{sname}/
%exclude %{geosinstdir}/lib64/python%{pyver}/site-packages/%{sname}/_%{sname}.la
%exclude %{geosinstdir}/lib64/python%{pyver}/site-packages/%{sname}/_%{sname}.a
%{geosinstdir}/lib64/python%{pyver}/site-packages/%{sname}/_%{sname}.so
%{geosinstdir}/lib64/python%{pyver}/site-packages/%{sname}.pth
%{geosinstdir}/lib64/python%{pyver}/site-packages/%{sname}/%{sname}.py
%{geosinstdir}/lib64/python%{pyver}/site-packages/%{sname}/%{sname}.py?


%changelog
* Sun Oct 1 2017 Devrim Gündüz <devrim@gunduz.org> - 3.6.2-1
- Initial packaging of 3.6.X for PostgreSQL RPM Repository,
  which is to satisfy PostGIS on older platforms, so that
  users can benefit from all PostGIS features.