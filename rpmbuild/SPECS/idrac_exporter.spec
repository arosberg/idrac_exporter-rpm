Name:           idrac_exporter
Version:        2.3.1
Release:        1%{?dist}
Summary:        Prometheus exporter for Dell iDRAC via Redfish

License:        MIT
URL:            https://github.com/mrlhansen/idrac_exporter
Source0:        idrac_exporter-v2.3.1-linux-amd64
Source1:        idrac_exporter.service
Source2:        idrac.yml

BuildArch:      x86_64

# We’re packaging a prebuilt binary, so no BuildRequires/Build steps needed

Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd

%description
Prometheus exporter for Redfish-based hardware metrics.

%prep
# No sources to unpack, prebuilt binary
# Just a no-op section
%define _unitdir /usr/lib/systemd/system

%build
# No build step, we already built the binary outside of RPM

%install
rm -rf %{buildroot}

# Install binary
install -D -m 0755 %{SOURCE0} %{buildroot}%{_bindir}/idrac_exporter

# Install systemd unit
install -D -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/idrac_exporter.service

# Install default config
install -D -m 0640 %{SOURCE2} %{buildroot}%{_sysconfdir}/prometheus/idrac.yml

%post
systemctl daemon-reload > /dev/null 2>&1 || :
systemctl enable --now idrac_exporter.service > /dev/null 2>&1 || :

%preun
if [ $1 -eq 0 ]; then
  systemctl disable --now idrac_exporter.service > /dev/null 2>&1 || :
fi

%postun
systemctl daemon-reload > /dev/null 2>&1 || :

%files
%license
%doc
%{_bindir}/%{name}
%config(noreplace) %{_sysconfdir}/prometheus/idrac.yml
%{_unitdir}/idrac_exporter.service

%changelog
* Mon Dec 01 2025 Aidan Rosberg <arosberg@iu.edu> - 2.3.1-1
- Initial package
