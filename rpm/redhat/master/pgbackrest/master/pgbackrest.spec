%global debug_package %{nil}

Summary:	Reliable PostgreSQL Backup & Restore
Name:		pgbackrest
Version:	2.03
Release:	4%{?dist}
License:	MIT
Group:		Applications/Databases
Url:		http://www.pgbackrest.org/
Source0:	https://github.com/pgbackrest/pgbackrest/archive/release/%{version}.tar.gz
Source1:	pgbackrest-conf.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:	perl-XML-LibXML perl-IO-Socket-SSL
%if 0%{?rhel} && 0%{?rhel} <= 6
Requires:	perl-parent perl-JSON
%else
Requires:	perl-JSON-PP
%endif
Requires:	perl-Digest-SHA perl-DBD-Pg perl-Time-HiRes
Requires:	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
pgBackRest aims to be a simple, reliable backup and restore system that can
seamlessly scale up to the largest databases and workloads.

Instead of relying on traditional backup tools like tar and rsync, pgBackRest
implements all backup features internally and uses a custom protocol for
communicating with remote systems. Removing reliance on tar and rsync allows
for better solutions to database-specific backup challenges. The custom remote
protocol allows for more flexibility and limits the types of connections that
are required to perform a backup which increases security.

%prep
%setup -q -n %{name}-release-%{version}

%build
pushd src
%{__make}
popd

%install
%{__install} -D -d -m 0755 %{buildroot}%{perl_vendorlib} %{buildroot}%{_bindir}
%{__install} -D -d -m 0700 %{buildroot}/%{_sharedstatedir}/%{name}
%{__install} -D -d -m 0700 %{buildroot}/var/log/%{name}
%{__install} -D -d -m 0700 %{buildroot}/var/spool/%{name}
%{__install} -D -d -m 0755 %{buildroot}%{_sysconfdir}
%{__install} %{SOURCE1} %{buildroot}/%{_sysconfdir}/%{name}.conf
%{__cp} -a src/%{name} %{buildroot}%{_bindir}/%{name}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc LICENSE
%else
%license LICENSE
%endif
%{_bindir}/%{name}
%config(noreplace) %attr (644,root,root) %{_sysconfdir}/%{name}.conf
%attr(-,postgres,postgres) /var/log/%{name}
%attr(-,postgres,postgres) %{_sharedstatedir}/%{name}
%attr(-,postgres,postgres) /var/spool/%{name}

%changelog
* Wed Jun 13 2018 - Devrim Gündüz <devrim@gunduz.org> 2.03-4
- Move perl-Time-HiRes dependency to global list, per
  https://github.com/pgbackrest/pgbackrest/issues/544

* Wed Jun 6 2018 - Devrim Gündüz <devrim@gunduz.org> 2.03-3
- Fix dependencies for RHEL 6, per #3387.

* Mon May 28 2018 - Devrim Gündüz <devrim@gunduz.org> 2.03-2
- Add new dependencies

* Thu May 24 2018 - Devrim Gündüz <devrim@gunduz.org> 2.03-1
- Update to 2.03, per #3366

* Mon May 7 2018 - Devrim Gündüz <devrim@gunduz.org> 2.02-1
- Update to 2.02, per #3335.

* Thu Mar 22 2018 - Devrim Gündüz <devrim@gunduz.org> 2.01-1
- Update to 2.01, per #3223

* Mon Feb 26 2018 - David Steele <david@pgbackrest.org> 2.00-1
- Update to 2.00, per #3152
- Build C pgbackrest bin, remove Perl bin

* Sun Feb 4 2018 - Devrim Gündüz <devrim@gunduz.org> 1.28-1
- Update to 1.28, per #3078

* Wed Dec 27 2017 - Devrim Gündüz <devrim@gunduz.org> 1.27-1
- Update to 1.27, per #2968

* Thu Dec 7 2017 - David Steele <david@pgbackrest.org> 1.26-3
- Cleanly build/install LibC. Fixes #2914

* Sun Dec 3 2017 - Devrim Gündüz <devrim@gunduz.org> 1.26-2
- Dirty hack to install libc related files manually. Fixes #2914

* Sun Nov 26 2017 - Devrim Gündüz <devrim@gunduz.org> 1.26-1
- Update to 1.26, per #2889
- Add perl-libc related files.

* Thu Oct 26 2017 - Devrim Gündüz <devrim@gunduz.org> 1.25-1
- Update to 1.25, per #2823

* Sun Oct 1 2017 - Devrim Gündüz <devrim@gunduz.org> 1.24-1
- Update to 1.24, per #2743

* Wed Sep 13 2017 - Devrim Gündüz <devrim@gunduz.org> 1.23-1
- Update to 1.23, per #2675.

* Thu Aug 10 2017 - Devrim Gündüz <devrim@gunduz.org> 1.22-1
- Update to 1.22, per #2643.

* Thu Jun 29 2017 - Devrim Gündüz <devrim@gunduz.org> 1.20-1
- Update to 1.20, per #2517.

* Tue Jun 13 2017 - Devrim Gündüz <devrim@gunduz.org> 1.19-1
- Update to 1.19, per #2483.

* Wed May 10 2017 - Devrim Gündüz <devrim@gunduz.org> 1.18-1
- Update to 1.18

* Tue Mar 14 2017 - Devrim Gündüz <devrim@gunduz.org> 1.17-1
- Update to 1.17

* Fri Mar 3 2017 - Devrim Gündüz <devrim@gunduz.org> 1.16-1
- Update to 1.16

* Wed Feb 8 2017 - Devrim Gündüz <devrim@gunduz.org> 1.13-1
- Update to 1.13

* Thu Dec 22 2016 - Devrim Gündüz <devrim@gunduz.org> 1.12-1
- Update to 1.12

* Thu Nov 17 2016 - Devrim Gündüz <devrim@gunduz.org> 1.11-1
- Update to 1.11

* Tue Nov 8 2016 - Devrim Gündüz <devrim@gunduz.org> 1.10-1
- Update to 1.10

* Thu Nov 3 2016 - Devrim Gündüz <devrim@gunduz.org> 1.09-1
- Update to 1.09
- Install default conf file, per David Steele.
- Install default directories, per David Steele.

* Sun Sep 18 2016 - Devrim Gündüz <devrim@gunduz.org> 1.08-1
- Update to 1.08

* Fri Aug 12 2016 - Devrim Gündüz <devrim@gunduz.org> 1.05-1
- Update to 1.05

* Fri May 27 2016 - Devrim Gündüz <devrim@gunduz.org> 1.01-1
- Initial packaging for PostgreSQL RPM Repository
