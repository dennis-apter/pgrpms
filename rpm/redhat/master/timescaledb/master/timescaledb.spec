%global sname	timescaledb

%global _varrundir %{_localstatedir}/run/%{name}

%ifarch ppc64 ppc64le
# Define the AT version and path.
%global atstring	at10.0
%global atpath		/opt/%{atstring}
%endif

Summary:	PostgreSQL based time-series database
Name:		%{sname}_%{pgmajorversion}
Version:	0.8.0
Release:	11%{?dist}
License:	Apache
Source0:	https://github.com/timescale/%{sname}/archive/%{version}.tar.gz
# Temp patch until the next release.
Patch0:		%{sname}-pg%{pgmajorversion}-pgconfig.patch
URL:		https://github.com/timescale/timescaledb00000000000
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	postgresql%{pgmajorversion}-devel cmake

%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%description
TimescaleDB is an open-source database designed to make SQL scalable for
time-series data. It is engineered up from PostgreSQL, providing automatic
partitioning across time and space (partitioning key), as well as full SQL
support.

%pre
if [ $1 -eq 1 ] ; then
groupadd -r pgagent >/dev/null 2>&1 || :
useradd -g pgagent -r -s /bin/false \
	-c "pgAgent Job Schedule" pgagent >/dev/null 2>&1 || :
touch /var/log/pgagent_%{pgmajorversion}.log
fi
%{__chown} pgagent:pgagent /var/log/pgagent_%{pgmajorversion}.log
%{__chmod} 0700 /var/log/pgagent_%{pgmajorversion}.log

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0
./bootstrap

%build
%ifarch ppc64 ppc64le
	CFLAGS="-O3 -mcpu=$PPC_MCPU -mtune=$PPC_MTUNE"
	CC=%{atpath}/bin/gcc; export CC
%else
	CFLAGS="$RPM_OPT_FLAGS -fPIC -pie"
	CXXFLAGS="$RPM_OPT_FLAGS -fPIC -pie"
	export CFLAGS
	export CXXFLAGS
%endif

cd build; %{__make}

%install
cd build; %{__make} DESTDIR=%{buildroot} install

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root)
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc README.md LICENSE
%else
%doc README.md
%license LICENSE
%endif
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}--*.sql
%{pginstdir}/share/extension/%{sname}.control

%changelog
* Tue Feb 6 2018 Devrim Gündüz <devrim@gunduz.org> 0.8.0-1
- Initial packaging for PostgreSQL RPM Repository
