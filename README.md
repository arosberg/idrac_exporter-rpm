# idrac_exporter-rpm

This repository provides an RPM packaging setup for the [`idrac_exporter`](https://github.com/mrlhansen/idrac_exporter) Prometheus exporter.
Included are:

- **RPM spec file** (`idrac_exporter.spec`)
- **Systemd service unit** (`idrac_exporter.service`)

## Build Instructions

To build the RPM locally using `rpmbuild`, run:

```bash
rpmbuild -ba \
  --define "_topdir $(pwd)/rpmbuild" \
  rpmbuild/SPECS/idrac_exporter.spec
