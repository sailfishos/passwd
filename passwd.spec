#specfile originally created for Fedora, modified for Moblin Linux
%if %{?WITH_SELINUX:0}%{!?WITH_SELINUX:1}
%define WITH_SELINUX 0
%endif
%if %{?WITH_AUDIT:0}%{!?WITH_AUDIT:1}
%define WITH_AUDIT 0
%endif
Summary: The passwd utility for setting/changing passwords using PAM
Name: passwd
Version: 0.78
Release: 1
License: BSD or GPLv2+
Group: System/Base
URL: http://fedorahosted.org/passwd
Source: https://fedorahosted.org/releases/p/a/passwd/%{name}-%{version}.tar.bz2
Patch1: passwd-0.75-gnome-keyring.patch
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: pam >= 0.78, /etc/pam.d/system-auth
%if %{WITH_SELINUX}
BuildRequires: libselinux-devel
%endif
BuildRequires: glib2-devel, libuser-devel, pam-devel, libuser >= 0.53-1
BuildRequires: gettext, popt-devel
%if %{WITH_AUDIT}
BuildRequires: audit-libs-devel >= 1.0.14
Requires: audit-libs >= 1.0.14
%endif

%description
The passwd package contains a system utility (passwd) which sets
and/or changes passwords, using PAM (Pluggable Authentication
Modules).

To use passwd, you should have PAM installed on your system.

%prep
%setup -q -n %{name}-%{version}
#%patch1 -p1 -b .gnome-keyring

%build
%configure \
%if %{WITH_SELINUX}
        --with-selinux \
%else
        --without-selinux \
%endif
%if %{WITH_AUDIT}
        --with-audit
%else
        --without-audit
%endif
make DEBUG= RPM_OPT_FLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT bindir=%{_bindir} mandir=%{_mandir}
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/
install -m 644 passwd.pamd $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/passwd
%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/pam.d/passwd
%attr(4755,root,root) %{_bindir}/passwd
%{_mandir}/man1/passwd.1*

