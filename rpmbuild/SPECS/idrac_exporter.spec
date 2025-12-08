Name:           idrac_exporter
Version:        2.3.1
Release:        1%{?dist}
Summary:        Prometheus exporter for Dell iDRAC via Redfish

License:        MIT
URL:            https://github.com/mrlhansen/idrac_exporter
Source0:        https://github.com/mrlhansen/idrac_exporter/archive/refs/tags/v%{version}.tar.gz
Source1:        idrac_exporter.service
Source2:        idrac.yml

%define _unitdir /usr/lib/systemd/system

BuildArch:      x86_64

BuildRequires:  golang
BuildRequires:  make

Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd

%description
Prometheus exporter for Redfish-based hardware metrics.

%pre
getent group idrac_exporter >/dev/null || groupadd -r idrac_exporter
getent passwd idrac_exporter >/dev/null || \
    useradd -r -g idrac_exporter -d /var/lib/idrac_exporter -s /sbin/nologin idrac_exporter

%prep
%autosetup -n idrac_exporter-%{version}

%build
make

%install
rm -rf %{buildroot}

# Install binary
install -D -m 0755 idrac_exporter %{buildroot}%{_bindir}/idrac_exporter

# Install systemd unit
install -D -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/idrac_exporter.service

# Install default config
install -D -m 0640 %{SOURCE2} %{buildroot}%{_sysconfdir}/prometheus/idrac.yml

%post
# Ensure config is owned by the service user on the target system
chown idrac_exporter:idrac_exporter %{_sysconfdir}/prometheus/idrac.yml >/dev/null 2>&1 || :

systemctl daemon-reload > /dev/null 2>&1 || :
# systemctl enable --now idrac_exporter.service > /dev/null 2>&1 || :

%preun
if [ $1 -eq 0 ]; then
  systemctl disable --now idrac_exporter.service > /dev/null 2>&1 || :
fi

%postun
systemctl daemon-reload > /dev/null 2>&1 || :

# Delete idrac_exporter user
if [ "$1" -eq 0 ]; then
    getent passwd idrac_exporter >/dev/null && userdel idrac_exporter || :
    getent group idrac_exporter >/dev/null && groupdel idrac_exporter || :
fi

%files
%license
%doc
%{_bindir}/%{name}
%config(noreplace) %{_sysconfdir}/prometheus/idrac.yml
%{_unitdir}/idrac_exporter.service

%changelog
* Mon Dec 01 2025 Aidan Rosberg <arosberg@iu.edu> - 2.3.1-1
- Initial package
