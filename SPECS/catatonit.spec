Name: catatonit
Epoch: 3
Version: 0.1.7
Release: 10%{?dist}
Summary: A signal-forwarding process manager for containers
License: GPLv3+
URL: https://github.com/openSUSE/catatonit
Source0: https://github.com/openSUSE/catatonit/archive/v%{version}.tar.gz
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: file
BuildRequires: gcc
BuildRequires: git
BuildRequires: glibc-static
BuildRequires: libtool

%description
Catatonit is a /sbin/init program for use within containers. It
forwards (almost) all signals to the spawned child, tears down
the container when the spawned child exits, and otherwise
cleans up other exited processes (zombies).

This is a reimplementation of other container init programs (such as
"tini" or "dumb-init"), but uses modern Linux facilities (such as
signalfd(2)) and has no additional features.

%prep
%autosetup -Sgit -n %{name}-%{version}
sed -i '/^AM_INIT_AUTOMAKE$/d' configure.ac

%build
autoreconf -fi
%configure
%{__make} %{?_smp_mflags}

# Make sure we *always* build a static binary. Otherwise we'll break containers
# that don't have the necessary shared libs.
file ./%{name} | grep 'statically linked'
if [ $? != 0 ]; then
   echo "ERROR: %{name} binary must be statically linked!"
   exit 1
fi

%install
install -dp %{buildroot}%{_libexecdir}/%{name}
install -p %{name} %{buildroot}%{_libexecdir}/%{name}

%files
%license COPYING
%doc README.md
%dir %{_libexecdir}/%{name}
%{_libexecdir}/%{name}/%{name}

%changelog
* Wed Jun 21 2023 Jindrich Novy <jnovy@redhat.com> - 3:0.1.7-10
- bump release to preserve upgrade path from 9.2
- Resolves: #2209677

* Mon May 29 2023 Jindrich Novy <jnovy@redhat.com> - 3:0.1.7-9
- rebuild for 9.3
- Resolves: #2209677

* Wed Jan 11 2023 Jindrich Novy <jnovy@redhat.com> - 3:0.1.7-8
- remove any relation to podman-catatonit
- Related: #2151322

* Tue Jul 26 2022 Jindrich Novy <jnovy@redhat.com> - 3:0.1.7-7
- make sure podman-catatonit is always obsoleted
- Related: #2061316

* Fri Jul 22 2022 Lokesh Mandvekar <lsm5@redhat.com> - 3:0.1.7-6
- Rebuild for combined gating with podman
- Related: #2061316

* Fri Jul 22 2022 Lokesh Mandvekar <lsm5@redhat.com> - 3:0.1.7-5
- Empty ruleset in gating.yaml
- Related: #2061316

* Wed Jul 20 2022 Lokesh Mandvekar <lsm5@redhat.com> - 3:0.1.7-4
- Remove osci.brew-build.tier0.functional from gating.yaml
- Related: #2061316

* Tue Jul 19 2022 Lokesh Mandvekar <lsm5@redhat.com> - 3:0.1.7-3
- Add gating.yaml to dist-git
- Related: #2061316

* Tue Jul 19 2022 Lokesh Mandvekar <lsm5@redhat.com> - 3:0.1.7-2
- Obsolete and provides podman-catatonit
- Related: #2061316

* Tue Jun 28 2022 Jindrich Novy <jnovy@redhat.com> - 0.1.7-1
- update to 0.1.7
- Related: #2061316

* Wed Apr 29 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.1.5-2
- complain if not statically linked, patch from Jindrich Novy <jnovy@redhat.com>

* Wed Apr 29 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.1.5-1
- bump to v0.1.5
- static binary to not break containers that don't have necessary shared libs

* Wed Feb 19 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.1.4-1
- first build for review
- source copied from openSUSE @ https://build.opensuse.org/package/show/openSUSE:Factory/catatonit
