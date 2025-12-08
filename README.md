## Build
```bash
rpmbuild -ba \
  --define "_topdir $(pwd)/rpmbuild" \
  rpmbuild/SPECS/idrac_exporter.spec
```