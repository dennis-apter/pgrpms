Summary:	a unix pager optimized for psql
Name:		pspg
Version:	0.1
Release:	1%{?dist}
License:	BSD
Group:		Development/Tools
URL:		https://github.com/okbob/%{name}
Source:		https://github.com/okbob/%{name}/archive/v%{version}.tar.gz
BuildRequires:	ncurses-devel
Requires:	ncurses

%description
pspg is a unix pager optimized for psql. It can freeze rows, freeze
columns, and lot of color themes are included.

%prep
%setup -q

%build
%configure
CFLAGS="%{optflags}"
%{__make} %{_smp_mflags} \
	prefix=%{_prefix} \
	all

%install
%{__rm} -rf %{buildroot}

CFLAGS="%{optflags}"
%{__make} %{_smp_mflags} DESTDIR=%{buildroot} \
	prefix=%{_prefix} bindir=%{_bindir} mandir=%{_mandir} \
	install

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc README.md LICENSE
%else
%license LICENSE
%doc README.md
%endif
%{_bindir}/*

%changelog
* Fri Sep 15 2017 Devrim Gündüz <devrim@gunduz.org> 0.1-1
- Initial packaging for PostgreSQL RPM repository, based on the spec
  file written by Pavel. Fixes #2704
