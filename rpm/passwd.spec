Summary: The passwd utility for setting/changing passwords using PAM
Name: passwd
Version: 0.79
Release: 1
License: BSD or GPLv2+
Group: System/Base
URL: https://pagure.io/passwd
Source: %{name}-%{version}.tar.bz2
Patch1: passwd-0.79-stdin-length.patch
Requires: pam >= 1.0.90, /etc/pam.d/system-auth
BuildRequires: automake
BuildRequires: glib2-devel, libuser-devel, pam-devel, libuser >= 0.53-1
BuildRequires: gettext, popt-devel

%description
The passwd package contains a system utility (passwd) which sets
and/or changes passwords, using PAM (Pluggable Authentication
Modules).

To use passwd, you should have PAM installed on your system.

%package doc
Summary:   Documentation for %{name}
Group:     Documentation
Requires:  %{name} = %{version}-%{release}

%description doc
Man page for %{name}.

%prep
%setup -q -n %{name}-%{version}/%{name}
%patch1 -p1

%build
autoreconf -vfi
%configure \
        --without-selinux \
        --without-audit

make DEBUG= RPM_OPT_FLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT bindir=%{_bindir} mandir=%{_mandir}
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/
install -m 644 passwd.pamd $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/passwd
%find_lang %{name}

%files -f %{name}.lang
%defattr(-,root,root,-)
%license COPYING
%config(noreplace) %{_sysconfdir}/pam.d/passwd
%attr(4755,root,root) %{_bindir}/passwd

%files doc
%defattr(-,root,root,-)
%{_mandir}/man1/%{name}.*
