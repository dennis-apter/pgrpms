%global pgpoolinstdir /usr/pgpool-%{pgpackageversion}
%global sname pgpool-II

%if 0%{?rhel} && 0%{?rhel} <= 6
%global systemd_enabled 0
%else
%global systemd_enabled 1
%endif

# Use this macro for update-alternatives, because implementations are different
# between RHEL and SLES:
%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
%global __update_alternatives %{_sbindir}/update-alternatives --quiet
%endif
%else
%global __update_alternatives %{_sbindir}/update-alternatives
%endif

%ifarch ppc64 ppc64le
# Define the AT version and path.
%global atstring	at10.0
%global atpath		/opt/%{atstring}
%endif

%global _varrundir %{_localstatedir}/run/%{name}

Summary:		Pgpool is a connection pooling/replication server for PostgreSQL
Name:			%{sname}-%{pgmajorversion}
Version:		3.5.15
Release:		1%{?dist}
License:		BSD
Group:			Applications/Databases
URL:			http://pgpool.net
Source0:		http://www.pgpool.net/mediawiki/images/%{sname}-%{version}.tar.gz
Source1:		%{sname}-pg%{pgmajorversion}.service
Source2:		%{sname}.sysconfig
Source3:		%{sname}-pg%{pgmajorversion}.init
Source9:		%{sname}-pg%{pgmajorversion}-libs.conf
Patch1:			%{sname}-pg%{pgmajorversion}-conf.sample.patch
Patch2:			%{sname}-pg%{pgmajorversion}-makefiles-pgxs.patch
BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:		postgresql%{pgmajorversion}-devel pam-devel
BuildRequires:		libmemcached-devel openssl-devel

%if %{systemd_enabled}
BuildRequires:		systemd
# We require this to be present for %%{_prefix}/lib/tmpfiles.d
Requires:		systemd
Requires(post):		systemd-sysv
Requires(post):		systemd
Requires(preun):	systemd
Requires(postun):	systemd
%else
Requires(post):		chkconfig
Requires(preun):	chkconfig
# This is for /sbin/service
Requires(preun):	initscripts
Requires(postun):	initscripts
%endif
Obsoletes:		postgresql-pgpool > 1.0.0

%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%ifarch ppc64 ppc64le
BuildRequires:	advance-toolchain-%{atstring}-devel
%endif

%description
pgpool-II is a inherited project of pgpool (to classify from
pgpool-II, it is sometimes called as pgpool-I). For those of
you not familiar with pgpool-I, it is a multi-functional
middle ware for PostgreSQL that features connection pooling,
replication and load balancing functions. pgpool-I allows a
user to connect at most two PostgreSQL servers for higher
availability or for higher search performance compared to a
single PostgreSQL server.

pgpool-II, on the other hand, allows multiple PostgreSQL
servers (DB nodes) to be connected, which enables queries
to be executed simultaneously on all servers. In other words,
it enables "parallel query" processing. Also, pgpool-II can
be started as pgpool-I by changing configuration parameters.
pgpool-II that is executed in pgpool-I mode enables multiple
DB nodes to be connected, which was not possible in pgpool-I.

%package devel
Summary:	The development files for pgpool-II
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Development headers and libraries for pgpool-II.

%package extensions
Summary:	Postgersql extensions for pgpool-II
Group:		Applications/Databases
Obsoletes:	postgresql-pgpool-II-recovery <= 1:3.3.4-1
Provides:	postgresql-pgpool-II-recovery = %{version}-%{release}
Requires:	postgresql%{pgmajorversion}-server
%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%description extensions
Postgresql extensions libraries and sql files for pgpool-II.

%prep
%setup -q -n %{sname}-%{version}
%patch1 -p0
%patch2 -p0

%build
%ifarch ppc64 ppc64le
	CFLAGS="${CFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	CXXFLAGS="${CXXFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	LDFLAGS="-L%{atpath}/%{_lib}"
	CC=%{atpath}/bin/gcc; export CC
%endif
# We need this flag on SLES so that pgpool can find libmemched.
# Otherwise, we get "libmemcached.so: undefined reference to `pthread_once'" error.
%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
	export LDFLAGS='-lpthread'
%endif
%endif
%ifarch ppc64 ppc64le
%configure --build=ppc64le \
%else
./configure \
%endif
	--datadir=%{pgpoolinstdir}/share \
	--disable-static \
        --bindir=%{pgpoolinstdir}/bin \
	--exec-prefix=%{pgpoolinstdir} \
	--includedir=%{pgpoolinstdir}/include \
	--libdir=%{pgpoolinstdir}/lib \
	--mandir=%{pgpoolinstdir}/man \
	--sysconfdir=%{_sysconfdir}/%{name}/ \
	--with-memcached=%{_includedir}/libmemcached \
	--with-openssl \
	--with-pam \
	--with-pgsql=%{pginstdir}

# https://fedoraproject.org/wiki/Packaging:Guidelines#Removing_Rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

USE_PGXS=1 %{__make} %{?_smp_mflags}
USE_PGXS=1 %{__make} %{?_smp_mflags} -C src/sql/pgpool_adm
USE_PGXS=1 %{__make} %{?_smp_mflags} -C src/sql/pgpool-recovery
USE_PGXS=1 %{__make} %{?_smp_mflags} -C src/sql/pgpool-regclass

%install
%{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install
%{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install -C src/sql/pgpool_adm
%{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install -C src/sql/pgpool-recovery
%{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install -C src/sql/pgpool-regclass

%if %{systemd_enabled}
%{__install} -d %{buildroot}%{_unitdir}
%{__install} -m 755 %{SOURCE1} %{buildroot}%{_unitdir}/%{sname}-%{pgmajorversion}.service

# ... and make a tmpfiles script to recreate it at reboot.
%{__mkdir} -p %{buildroot}%{_tmpfilesdir}
cat > %{buildroot}%{_tmpfilesdir}/%{name}.conf <<EOF
d %{_varrundir} 0755 root root -
EOF

%else
%{__install} -d %{buildroot}%{_sysconfdir}/init.d
%{__install} -m 755 %{SOURCE3} %{buildroot}%{_sysconfdir}/init.d/%{name}
%endif

%{__install} -d %{buildroot}%{_sysconfdir}/sysconfig
%{__install} -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/%{name}

# nuke libtool archive and static lib
%{__rm} -f %{buildroot}%{pgpoolinstdir}/lib/libpcp.{a,la}

# Install linker conf file under postgresql installation directory.
# We will install the latest version via alternatives.
%{__install} -d -m 755 %{buildroot}%{pgpoolinstdir}/share/
%{__install} -m 700 %{SOURCE9} %{buildroot}%{pgpoolinstdir}/share/

%post
# Create alternatives entries for common binaries and man files
%{__update_alternatives} --install /usr/bin/pgpool pgpool-pgpool %{pgpoolinstdir}/bin/pgpool %{pgmajorversion}0
%{__update_alternatives} --install /usr/bin/pcp_attach_node pgpool-pcp_attach_node %{pgpoolinstdir}/bin/pcp_attach_node %{pgmajorversion}0
%{__update_alternatives} --install /usr/bin/pcp_detach_node pgpool-pcp_detach_node %{pgpoolinstdir}/bin/pcp_detach_node %{pgmajorversion}0
%{__update_alternatives} --install /usr/bin/pcp_node_count pgpool-pcp_node_count %{pgpoolinstdir}/bin/pcp_node_count %{pgmajorversion}0
%{__update_alternatives} --install /usr/bin/pcp_node_info pgpool-pcp_node_info %{pgpoolinstdir}/bin/pcp_node_info %{pgmajorversion}0
%{__update_alternatives} --install /usr/bin/pcp_pool_status pgpool-pcp_pool_status %{pgpoolinstdir}/bin/pcp_pool_status %{pgmajorversion}0
%{__update_alternatives} --install /usr/bin/pcp_promote_node pgpool-pcp_promote_node %{pgpoolinstdir}/bin/pcp_promote_node %{pgmajorversion}0
%{__update_alternatives} --install /usr/bin/pcp_proc_count pgpool-pcp_proc_count %{pgpoolinstdir}/bin/pcp_proc_count %{pgmajorversion}0
%{__update_alternatives} --install /usr/bin/pcp_proc_info pgpool-pcp_proc_info %{pgpoolinstdir}/bin/pcp_proc_info %{pgmajorversion}0
%{__update_alternatives} --install /usr/bin/pcp_stop_pgpool pgpool-pcp_stop_pgpool %{pgpoolinstdir}/bin/pcp_stop_pgpool %{pgmajorversion}0
%{__update_alternatives} --install /usr/bin/pcp_recovery_node pgpool-pcp_recovery_node %{pgpoolinstdir}/bin/pcp_recovery_node %{pgmajorversion}0
%{__update_alternatives} --install /usr/bin/pcp_watchdog pgpool-pcp_watchdog_info %{pgpoolinstdir}/bin/pcp_watchdog_info %{pgmajorversion}0
%{__update_alternatives} --install /usr/bin/pg_md5 pgpool-pg_md5 %{pgpoolinstdir}/bin/pg_md5 %{pgmajorversion}0
%{__update_alternatives} --install /etc/ld.so.conf.d/pgpool-libs.conf pgpool-ld-conf %{pgpoolinstdir}/share/pgpool-%{pgmajorversion}-libs.conf %{pgmajorversion}0
/sbin/ldconfig
%if %{systemd_enabled}
%systemd_post %{sname}-%{pgmajorversion}.service
%tmpfiles_create
%else
# This adds the proper /etc/rc*.d links for the script
/sbin/chkconfig --add %{name}
%endif

%preun
%if %{systemd_enabled}
%systemd_preun %{sname}-%{pgmajorversion}.service
%else
if [ $1 -eq 0 ] ; then
	/sbin/service %{sname}-%{pgmajorversion} condstop >/dev/null 2>&1
	/sbin/chkconfig --del %{sname}-%{pgmajorversion}
fi
%endif

%postun
if [ "$1" -eq 0 ]
  then
	%{__update_alternatives} --remove pgpool-ld-conf	%{pgpoolinstdir}/share/pgpool-%{pgmajorversion}-libs.conf
	/sbin/ldconfig
fi
/sbin/ldconfig
%if %{systemd_enabled}
%systemd_postun_with_restart %{sname}-%{pgmajorversion}.service
%else
if [ $1 -ge 1 ] ; then
    /sbin/service pgpool-II-%{pgmajorversion} condrestart >/dev/null 2>&1 || :
fi
%endif
# Drop alternatives entries for common binaries and man files
if [ "$1" -eq 0 ]
  then
	# Only remove these links if the package is completely removed from the system (vs.just being upgraded)
	%{__update_alternatives} --remove pgpool-pgpool %{pgpoolinstdir}/bin/pgpool
	%{__update_alternatives} --remove pgpool-pcp_attach_node %{pgpoolinstdir}/bin/pcp_attach_node
	%{__update_alternatives} --remove pgpool-pcp_detach_node %{pgpoolinstdir}/bin/pcp_detach_node
	%{__update_alternatives} --remove pgpool-pcp_node_count %{pgpoolinstdir}/bin/pcp_node_count
	%{__update_alternatives} --remove pgpool-pcp_node_info %{pgpoolinstdir}/bin/pcp_node_info
	%{__update_alternatives} --remove pgpool-pcp_pool_status %{pgpoolinstdir}/bin/pcp_pool_status
	%{__update_alternatives} --remove pgpool-pcp_promote_node %{pgpoolinstdir}/bin/pcp_promote_node
	%{__update_alternatives} --remove pgpool-pcp_proc_count %{pgpoolinstdir}/bin/pcp_proc_count
	%{__update_alternatives} --remove pgpool-pcp_proc_info %{pgpoolinstdir}/bin/pcp_proc_info
	%{__update_alternatives} --remove pgpool-pcp_stop_pgpool %{pgpoolinstdir}/bin/pcp_stop_pgpool
	%{__update_alternatives} --remove pgpool-pcp_recovery_node %{pgpoolinstdir}/bin/pcp_recovery_node
	%{__update_alternatives} --remove pgpool-pcp_watchdog_info %{pgpoolinstdir}/bin/pcp_watchdog_info
	%{__update_alternatives} --remove pgpool-pg_md5 %{pgpoolinstdir}/bin/pg_md5
fi

%if %{systemd_enabled}
%triggerun -- %{sname}-%{pgmajorversion} < 3.1-1
# Save the current service runlevel info
# User must manually run systemd-sysv-convert --apply pgpool
# to migrate them to systemd targets
/usr/bin/systemd-sysv-convert --save %{sname}-%{pgmajorversion} >/dev/null 2>&1 ||:

# Run these because the SysV package being removed won't do them
/sbin/chkconfig --del %{sname}-%{pgmajorversion} >/dev/null 2>&1 || :
/bin/systemctl try-restart %{sname}-%{pgmajorversion}.service >/dev/null 2>&1 || :
%endif

%files
%doc README TODO INSTALL AUTHORS ChangeLog NEWS doc/pgpool-en.html doc/pgpool-ja.html doc/pgpool.css doc/tutorial-en.html doc/tutorial-ja.html
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc COPYING
%else
%license COPYING
%endif
%dir %{pgpoolinstdir}
%{pgpoolinstdir}/bin/pgpool
%{pgpoolinstdir}/bin/pcp_attach_node
%{pgpoolinstdir}/bin/pcp_detach_node
%{pgpoolinstdir}/bin/pcp_node_count
%{pgpoolinstdir}/bin/pcp_node_info
%{pgpoolinstdir}/bin/pcp_pool_status
%{pgpoolinstdir}/bin/pcp_proc_count
%{pgpoolinstdir}/bin/pcp_proc_info
%{pgpoolinstdir}/bin/pcp_promote_node
%{pgpoolinstdir}/bin/pcp_recovery_node
%{pgpoolinstdir}/bin/pcp_stop_pgpool
%{pgpoolinstdir}/bin/pcp_watchdog_info
%{pgpoolinstdir}/bin/pg_md5
%{pgpoolinstdir}/man/man8/pgpool.8
%{pgpoolinstdir}/share/pgpool-II/insert_lock.sql
%{pgpoolinstdir}/share/pgpool-II/pgpool.pam
%{_sysconfdir}/%{name}/*.sample*
%{pgpoolinstdir}/lib/libpcp.so.*
%config(noreplace) %attr (644,root,root) %{pgpoolinstdir}/share/pgpool-II-pg%{pgmajorversion}-libs.conf

%if %{systemd_enabled}
%ghost %{_varrundir}
%{_tmpfilesdir}/%{name}.conf
%{_unitdir}/%{sname}-%{pgmajorversion}.service
%else
%{_sysconfdir}/init.d/%{name}
%endif
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}

%files devel
%{pgpoolinstdir}/include/libpcp_ext.h
%{pgpoolinstdir}/include/pcp.h
%{pgpoolinstdir}/include/pool_process_reporting.h
%{pgpoolinstdir}/include/pool_type.h
%{pgpoolinstdir}/lib/libpcp.so

%files extensions
%{pginstdir}/lib/pgpool_adm.so
%{pginstdir}/lib/pgpool-recovery.so
%{pginstdir}/share/extension/pgpool_adm--1.0.sql
%{pginstdir}/share/extension/pgpool_adm.control
%{pginstdir}/share/extension/pgpool-recovery.sql
%{pginstdir}/share/extension/pgpool-regclass.sql
%{pginstdir}/share/extension/pgpool_recovery--1.1.sql
%{pginstdir}/share/extension/pgpool_recovery.control
%{pginstdir}/share/extension/pgpool_regclass--1.0.sql
%{pginstdir}/share/extension/pgpool_regclass.control
# From PostgreSQL 9.4 pgpool-regclass.so is not needed anymore
# because 9.4 or later has to_regclass.
%{pginstdir}/lib/pgpool-regclass.so

%changelog
* Thu Jun 14 2018 Devrim Gündüz <devrim@gunduz.org> - 3.5.15-1
- Update to 3.5.15

* Tue Apr 17 2018 Devrim Gündüz <devrim@gunduz.org> - 3.5.14-1
- Update to 3.5.14

* Sat Feb 17 2018 Devrim Gündüz <devrim@gunduz.org> - 3.5.13-1
- Update to 3.5.13

* Wed Jan 10 2018 Devrim Gündüz <devrim@gunduz.org> - 3.5.12-1
- Update to 3.5.12

* Wed Nov 8 2017 Devrim Gündüz <devrim@gunduz.org> - 3.5.11-1
- Update to 3.5.11

* Tue Sep 5 2017 Devrim Gündüz <devrim@gunduz.org> - 3.5.10-1
- Update to 3.5.10
- Use a new macro for update-alternatives, so that it does not
  produce verbose output in SLES.

* Thu Jul 13 2017 Devrim Gündüz <devrim@gunduz.org> - 3.5.9-1
- Update to 3.5.9

* Sat May 6 2017 Devrim Gündüz <devrim@gunduz.org> - 3.5.7-1
- Update to 3.5.7

* Fri Mar 17 2017 Devrim Gündüz <devrim@gunduz.org> - 3.5.6-1
- Update to 3.5.6

* Mon Dec 26 2016 Devrim Gündüz <devrim@gunduz.org> - 3.5.5-1
- Update to 3.5.5

* Fri Sep 2 2016 Devrim Gündüz <devrim@gunduz.org> - 3.5.4-1
- Update to 3.5.4

* Mon Jul 4 2016 Devrim Gündüz <devrim@gunduz.org> - 3.5.3-1
- Update to 3.5.3

* Thu Apr 28 2016 Devrim Gündüz <devrim@gunduz.org> - 3.5.2-1
- Update to 3.5.2

* Tue Apr 5 2016 Devrim Gündüz <devrim@gunduz.org> - 3.5.1-1
- Update to 3.5.1

* Tue Feb 9 2016 Devrim Gündüz <devrim@gunduz.org> - 3.5.0-1
- Update to 3.5.0
- Add pgpool_adm to extensions subpackage.

* Mon Jan 11 2016 Devrim Gündüz <devrim@gunduz.org> - 3.4.3-4
- Second time in a row: Fix typo in init script. Per report
  from Ryan Shoemaker.

* Wed Dec 9 2015 Devrim Gündüz <devrim@gunduz.org> - 3.4.3-3
- Fix typo in init script. Per report from Ryan Shoemaker.

* Thu Sep 17 2015 Jeff Frost <jeff@pgexperts.com> - 3.4.3-2
- Bring init script in line with pgpool community init script

* Wed Aug 5 2015 Devrim Gündüz <devrim@gunduz.org> - 3.4.3-1
- Update to 3.4.3, per changes described at:
  http://www.pgpool.net/docs/pgpool-II-3.4.3/NEWS.txt

* Wed Apr 8 2015 Devrim Gündüz <devrim@gunduz.org> - 3.4.2-1
- Update to 3.4.2, per changes described at:
  http://www.pgpool.net/docs/pgpool-II-3.4.2/NEWS.txt

* Fri Feb 6 2015 Devrim Gündüz <devrim@gunduz.org> - 3.4.1-2
- Add missing BuildRoot macro.
- Fix rpmlint warnings/errors.

* Thu Feb 5 2015 Devrim Gündüz <devrim@gunduz.org> - 3.4.1-1
- Update to 3.4.1
- Remove patch3, now in upstream.

* Mon Jan 12 2015 Devrim Gündüz <devrim@gunduz.org> - 3.4.0-4
- Create /etc/ld.so.conf.d config file, for pcp and other libraries.
  Per #12597 in pgsql-bugs mailing list.

* Mon Jan 12 2015 Devrim Gündüz <devrim@gunduz.org> - 3.4.0-3
- Fix builds for non-systemd environments. Patch by Bernd Helmle.

* Thu Dec 11 2014 Devrim Gündüz <devrim@gunduz.org> - 3.4.0-2
- Sync with Fedora spec and apply our multiversion changes.
  Fedora spec is recently reworked by Pavel Raiskup. This spec
  file adds -extensions subpackage.

- Trim changelog

* Fri Nov 7 2014 Devrim Gündüz <devrim@gunduz.org> - 3.4.0-1
- Update to 3.4.0
- Add patch3 to fix compilation with memcache support. This
  patch will be removed when 3.4.1 comes out.
- Fix config file path in unit file.

