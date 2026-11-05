# AEGIS Dependency Analysis

- **Project:** `C:\Users\Aayush(work)\aegis-demo`
- **Generated:** 2026-10-23T11:55:45.610074+00:00
- **Analysis complete:** yes
- **Manifests:** 1
- **Dependency declarations:** 2

## Advisory Summary

- **Raw OSV records:** 14
- **Unique advisory groups:** 7

- **requests — CVE-2018-18074:** 2 OSV record(s)
  - **Identifiers:** CVE-2018-18074, GHSA-x84v-xcm2-53pg, PYSEC-2018-28
- **requests — CVE-2023-32681:** 2 OSV record(s)
  - **Identifiers:** CVE-2023-32681, GHSA-j8r2-6x86-q33q, PYSEC-2023-74
- **requests — CVE-2024-35195:** 2 OSV record(s)
  - **Identifiers:** CVE-2024-35195, GHSA-9wx4-h78v-vm56, PYSEC-2026-1873
- **requests — CVE-2024-47081:** 2 OSV record(s)
  - **Identifiers:** CVE-2024-47081, GHSA-9hjg-9r4m-mvj7, PYSEC-2026-1872
- **requests — CVE-2026-25645:** 2 OSV record(s)
  - **Identifiers:** CVE-2026-25645, GHSA-gc5v-m9x4-r6x2, PYSEC-2026-2275
- **flask — CVE-2023-30861:** 2 OSV record(s)
  - **Identifiers:** CVE-2023-30861, GHSA-m2qf-hxjv-5gpq, PYSEC-2023-62
- **flask — CVE-2026-27205:** 2 OSV record(s)
  - **Identifiers:** CVE-2026-27205, GHSA-68rp-wp8r-4726, PYSEC-2026-2151

## Findings

### 1. requests==2.19.0
- **Source:** `C:\Users\Aayush(work)\aegis-demo\requirements.txt:1`
- **Vulnerability query:** checked
- **Candidate fixed versions (review required):** 2.20.0, 2.31.0, 2.32.0, 2.32.4, 2.33.0
- **OSV ID:** GHSA-9hjg-9r4m-mvj7
  - **Summary:** Requests vulnerable to .netrc credentials leak via malicious URLs
  - **Aliases:** CVE-2024-47081, PYSEC-2026-1872
  - **Known fixed versions:** 2.32.4
  - **References:** https://github.com/psf/requests/security/advisories/GHSA-9hjg-9r4m-mvj7, https://nvd.nist.gov/vuln/detail/CVE-2024-47081, https://github.com/psf/requests/pull/6965, https://github.com/psf/requests/commit/96ba401c1296ab1dda74a2365ef36d88f7d144ef, https://github.com/advisories/GHSA-9hjg-9r4m-mvj7
- **OSV ID:** GHSA-9wx4-h78v-vm56
  - **Summary:** Requests `Session` object does not verify requests after making first request with verify=False
  - **Aliases:** CVE-2024-35195, PYSEC-2026-1873
  - **Known fixed versions:** 2.32.0
  - **References:** https://github.com/psf/requests/security/advisories/GHSA-9wx4-h78v-vm56, https://nvd.nist.gov/vuln/detail/CVE-2024-35195, https://github.com/psf/requests/pull/6655, https://github.com/psf/requests/commit/a58d7f2ffb4d00b46dca2d70a3932a0b37e22fac, https://github.com/psf/requests
- **OSV ID:** GHSA-gc5v-m9x4-r6x2
  - **Summary:** Requests has Insecure Temp File Reuse in its extract_zipped_paths() utility function
  - **Aliases:** CVE-2026-25645, PYSEC-2026-2275
  - **Known fixed versions:** 2.33.0
  - **References:** https://github.com/psf/requests/security/advisories/GHSA-gc5v-m9x4-r6x2, https://nvd.nist.gov/vuln/detail/CVE-2026-25645, https://github.com/psf/requests/commit/66d21cb07bd6255b1280291c4fafb71803cdb3b7, https://github.com/psf/requests, https://github.com/psf/requests/releases/tag/v2.33.0
- **OSV ID:** GHSA-j8r2-6x86-q33q
  - **Summary:** Unintended leak of Proxy-Authorization header in requests
  - **Aliases:** CVE-2023-32681, PYSEC-2023-74
  - **Known fixed versions:** 2.31.0
  - **References:** https://github.com/psf/requests/security/advisories/GHSA-j8r2-6x86-q33q, https://nvd.nist.gov/vuln/detail/CVE-2023-32681, https://github.com/psf/requests/commit/74ea7cf7a6a27a4eeb2ae24e162bcc942a6706d5, https://github.com/psf/requests, https://github.com/psf/requests/releases/tag/v2.31.0
- **OSV ID:** GHSA-x84v-xcm2-53pg
  - **Summary:** Insufficiently Protected Credentials in Requests
  - **Aliases:** CVE-2018-18074, PYSEC-2018-28
  - **Known fixed versions:** 2.20.0
  - **References:** https://nvd.nist.gov/vuln/detail/CVE-2018-18074, https://github.com/requests/requests/issues/4716, https://github.com/requests/requests/pull/4718, https://github.com/requests/requests/commit/c45d7c49ea75133e52ab22a8e9e13173938e36ff, https://access.redhat.com/errata/RHSA-2019:2035
- **OSV ID:** PYSEC-2018-28
  - **Summary:** No summary supplied by OSV.
  - **Aliases:** CVE-2018-18074, GHSA-x84v-xcm2-53pg
  - **Known fixed versions:** 2.20.0
  - **References:** https://github.com/requests/requests/pull/4718, https://github.com/requests/requests/issues/4716, https://github.com/requests/requests/commit/c45d7c49ea75133e52ab22a8e9e13173938e36ff, https://bugs.debian.org/910766, https://usn.ubuntu.com/3790-1/
- **OSV ID:** PYSEC-2023-74
  - **Summary:** No summary supplied by OSV.
  - **Aliases:** CVE-2023-32681, GHSA-j8r2-6x86-q33q
  - **Known fixed versions:** 2.31.0
  - **References:** https://github.com/psf/requests/security/advisories/GHSA-j8r2-6x86-q33q, https://github.com/psf/requests/releases/tag/v2.31.0, https://github.com/psf/requests/commit/74ea7cf7a6a27a4eeb2ae24e162bcc942a6706d5, https://lists.fedoraproject.org/archives/list/package-announce@lists.fedoraproject.org/message/AW7HNFGYP44RT3DUDQXG2QT3OEV2PJ7Y/
- **OSV ID:** PYSEC-2026-1872
  - **Summary:** Requests vulnerable to .netrc credentials leak via malicious URLs
  - **Aliases:** CVE-2024-47081, GHSA-9hjg-9r4m-mvj7
  - **Known fixed versions:** 2.32.4
  - **References:** https://github.com/psf/requests/security/advisories/GHSA-9hjg-9r4m-mvj7, https://nvd.nist.gov/vuln/detail/CVE-2024-47081, https://github.com/psf/requests/pull/6965, https://github.com/psf/requests/commit/96ba401c1296ab1dda74a2365ef36d88f7d144ef, https://github.com/psf/requests
- **OSV ID:** PYSEC-2026-1873
  - **Summary:** Requests `Session` object does not verify requests after making first request with verify=False
  - **Aliases:** CVE-2024-35195, GHSA-9wx4-h78v-vm56
  - **Known fixed versions:** 2.32.0
  - **References:** https://github.com/psf/requests/security/advisories/GHSA-9wx4-h78v-vm56, https://nvd.nist.gov/vuln/detail/CVE-2024-35195, https://github.com/psf/requests/pull/6655, https://github.com/psf/requests/commit/a58d7f2ffb4d00b46dca2d70a3932a0b37e22fac, https://github.com/psf/requests
- **OSV ID:** PYSEC-2026-2275
  - **Summary:** No summary supplied by OSV.
  - **Aliases:** CVE-2026-25645, GHSA-gc5v-m9x4-r6x2
  - **Known fixed versions:** 2.33.0
  - **References:** https://github.com/psf/requests/releases/tag/v2.33.0, https://github.com/psf/requests/security/advisories/GHSA-gc5v-m9x4-r6x2, https://github.com/psf/requests/commit/66d21cb07bd6255b1280291c4fafb71803cdb3b7

### 2. flask==2.0.0
- **Source:** `C:\Users\Aayush(work)\aegis-demo\requirements.txt:2`
- **Vulnerability query:** checked
- **Candidate fixed versions (review required):** 2.2.5, 2.3.2, 3.1.3
- **OSV ID:** GHSA-68rp-wp8r-4726
  - **Summary:** Flask session does not add `Vary: Cookie` header when accessed in some ways
  - **Aliases:** CVE-2026-27205, PYSEC-2026-2151
  - **Known fixed versions:** 3.1.3
  - **References:** https://github.com/pallets/flask/security/advisories/GHSA-68rp-wp8r-4726, https://nvd.nist.gov/vuln/detail/CVE-2026-27205, https://github.com/pallets/flask/commit/089cb86dd22bff589a4eafb7ab8e42dc357623b4, https://github.com/pallets/flask, https://github.com/pallets/flask/releases/tag/3.1.3
- **OSV ID:** GHSA-m2qf-hxjv-5gpq
  - **Summary:** Flask vulnerable to possible disclosure of permanent session cookie due to missing Vary: Cookie header
  - **Aliases:** CVE-2023-30861, PYSEC-2023-62
  - **Known fixed versions:** 2.2.5, 2.3.2
  - **References:** https://github.com/pallets/flask/security/advisories/GHSA-m2qf-hxjv-5gpq, https://nvd.nist.gov/vuln/detail/CVE-2023-30861, https://github.com/pallets/flask/commit/70f906c51ce49c485f1d355703e9cc3386b1cc2b, https://github.com/pallets/flask/commit/afd63b16170b7c047f5758eb910c416511e9c965, https://github.com/pallets/flask
- **OSV ID:** PYSEC-2023-62
  - **Summary:** No summary supplied by OSV.
  - **Aliases:** CVE-2023-30861, GHSA-m2qf-hxjv-5gpq
  - **Known fixed versions:** 2.2.5, 2.3.2
  - **References:** https://github.com/pallets/flask/commit/70f906c51ce49c485f1d355703e9cc3386b1cc2b, https://github.com/pallets/flask/releases/tag/2.3.2, https://github.com/pallets/flask/releases/tag/2.2.5, https://github.com/pallets/flask/security/advisories/GHSA-m2qf-hxjv-5gpq, https://github.com/pallets/flask/commit/afd63b16170b7c047f5758eb910c416511e9c965
- **OSV ID:** PYSEC-2026-2151
  - **Summary:** No summary supplied by OSV.
  - **Aliases:** CVE-2026-27205, GHSA-68rp-wp8r-4726
  - **Known fixed versions:** 3.1.3
  - **References:** https://github.com/pallets/flask/releases/tag/3.1.3, https://github.com/pallets/flask/security/advisories/GHSA-68rp-wp8r-4726, https://github.com/pallets/flask/commit/089cb86dd22bff589a4eafb7ab8e42dc357623b4

## Issues and Limitations

No analysis issues were recorded.

## Interpretation

This report is decision support, not a guarantee that the project is secure. OSV results depend on network availability and source coverage. Static parsing does not resolve the complete environment, prove that a vulnerability affects runtime behavior, or verify application compatibility. Candidate fixed versions require independent review and compatibility testing. No dependency files were changed by this analysis.
