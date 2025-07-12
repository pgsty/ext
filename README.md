# PostgreSQL Extension Catalog

[![Webite: ext.pgsty.com](https://img.shields.io/badge/website-pigsty.io-slategray?style=flat&logo=cilium&logoColor=white)](https://ext.pgsty.com)
[![CLI: pig v0.5.0](https://img.shields.io/badge/pig-v0.4.2-slategray?style=flat&logo=cilium&logoColor=white)](https://github.com/pgsty/pig)
[![Extensions: 423](https://img.shields.io/badge/extensions-423-%233E668F?style=flat&logo=postgresql&logoColor=white&labelColor=3E668F)](https://pigsty.io/ext/list)
[![License: Apache-2.0](https://img.shields.io/github/license/pgsty/extension?logo=opensourceinitiative&logoColor=green&color=slategray)](https://github.com/pgsty/pig/blob/main/LICENSE)

The supplementary [APT](#apt-repo) and [YUM](#yum-repo) repo for PostgreSQL extensions, maintained and used by [Pigsty](https://www.pigsty.io)

Provide [423](https://ext.pgsty.com/list) available extensions as RPM / DEB for PostgreSQL **13** - **17** in addition to the official PGDG repo.

Available on Linux: Debian 12 / Ubuntu 24.04 / 22.04 / EL8 / EL9 compatible distros, and `x86_64` & `ARM64` arch.

| Entry | All | PGDG | PIGSTY | CONTRIB | MISC | MISS | PG17 | PG16 | PG15 | PG14 | PG13 |
|:-----:|:---:|:----:|:------:|:-------:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|
|  RPM  | 417 | 119  |  227   |   71    |  0   |  6   | 399  | 407  | 410  | 394  | 368  |
|  DEB  | 410 | 103  |  236   |   71    |  0   |  13  | 397  | 400  | 403  | 391  | 363  |


**Why extension matters to PostgreSQL?** check the post: "[***PostgreSQL is eating the database world!***](https://medium.com/@fengruohang/postgres-is-eating-the-database-world-157c204dcfc4)"

**Why using this repo?** check the post: [***The idea way to deliver PostgreSQL extensions***](https://medium.com/@fengruohang/the-idea-way-to-deliver-postgresql-extensions-35646464bb71)

[![PostgreSQL Extension Ecosystem](public/img/ecosystem.gif)](https://medium.com/@fengruohang/postgres-is-eating-the-database-world-157c204dcfc4)

> [The idea way to deliver PostgreSQL extensions](https://medium.com/@fengruohang/the-idea-way-to-deliver-postgresql-extensions-35646464bb71)

-------

## Get Started

### Pig CLI

You can use the [`pig`](https://ext.pgsty.com/pig) cli tool (pg package manager) or just use the traditional way. It's up to you.

```bash
curl -fsSL https://repo.pigsty.io/pig | bash  # install pig rpm/deb package
$ pig repo add pigsty pgdg -u                 # add pgdg & pigsty repo, update cache      
$ pig ext install pg17                        # install PostgreSQL 17 kernels with PGDG native packages
$ pig ext install pg_duckdb                   # install the pg_duckdb extension (for current pg17)
```

### APT Repo

[![Linux AMD](https://img.shields.io/badge/Linux-AMD64-%%23FCC624?style=flat&logo=linux&labelColor=FCC624&logoColor=black)](https://doc.pgsty.com/node)
[![Linux ARM](https://img.shields.io/badge/Linux-ARM64-%%23FCC624?style=flat&logo=linux&labelColor=FCC624&logoColor=black)](https://doc.pgsty.com/node)
[![Ubuntu Support: 24](https://img.shields.io/badge/Ubuntu-24/noble-%%23E95420?style=flat&logo=ubuntu&logoColor=%%23E95420)](https://ext.pgsty.com.com/list/)
[![Ubuntu Support: 22](https://img.shields.io/badge/Ubuntu-22/jammy-%%23E95420?style=flat&logo=ubuntu&logoColor=%%23E95420)](https://ext.pgsty.com/list/)
[![Debian Support: 12](https://img.shields.io/badge/Debian-12/bookworm-%%23A81D33?style=flat&logo=debian&logoColor=%%23A81D33)](https://doc.pgsty.com/prepare/linux/)

All rpm/deb packages are signed with GPG key `B9BD8B20` (`9592A7BC7A682E7333376E09E7935D8DB9BD8B20` ).

For Ubuntu 22.04 / 24.04 & Debian 12 or any compatible platforms, use the following commands:

```bash
curl -fsSL https://repo.pigsty.io/key | sudo gpg --dearmor -o /etc/apt/keyrings/pigsty.gpg  # add gpg key
sudo tee /etc/apt/sources.list.d/pigsty-io.list > /dev/null <<EOF
deb [signed-by=/etc/apt/keyrings/pigsty.gpg] https://repo.pigsty.io/apt/infra generic main 
deb [signed-by=/etc/apt/keyrings/pigsty.gpg] https://repo.pigsty.io/apt/pgsql/$(lsb_release -cs) $(lsb_release -cs) main
EOF
sudo apt update;  # sudo apt install pig
```

### YUM Repo

[![Linux x86_64](https://img.shields.io/badge/Linux-x86_64-%%23FCC624?style=flat&logo=linux&labelColor=FCC624&logoColor=black)](https://pigsty.io/docs/node)
[![Linux AARCH64](https://img.shields.io/badge/Linux-Aarch64-%%23FCC624?style=flat&logo=linux&labelColor=FCC624&logoColor=black)](https://pigsty.io/docs/node)
[![RHEL Support: 8](https://img.shields.io/badge/EL-8-red?style=flat&logo=redhat&logoColor=red)](https://pigsty.io/docs/pgext/list/rpm/)
[![RHEL Support: 9](https://img.shields.io/badge/EL-9-red?style=flat&logo=redhat&logoColor=red)](https://pigsty.io/docs/pgext/list/rpm/)
[![RHEL](https://img.shields.io/badge/RHEL-slategray?style=flat&logo=redhat&logoColor=red)](https://pigsty.io/docs/pgext/list/rpm/)
[![CentOS](https://img.shields.io/badge/CentOS-slategray?style=flat&logo=centos&logoColor=%%23262577)](https://almalinux.org/)
[![RockyLinux](https://img.shields.io/badge/RockyLinux-slategray?style=flat&logo=rockylinux&logoColor=%%2310B981)](https://almalinux.org/)
[![AlmaLinux](https://img.shields.io/badge/AlmaLinux-slategray?style=flat&logo=almalinux&logoColor=black)](https://almalinux.org/)
[![OracleLinux](https://img.shields.io/badge/OracleLinux-slategray?style=flat&logo=oracle&logoColor=%%23F80000)](https://almalinux.org/)

For EL 8/9 and compatible platforms, use the following commands to add the YUM repo:

```bash
curl -fsSL https://repo.pigsty.io/key      | sudo tee /etc/pki/rpm-gpg/RPM-GPG-KEY-pigsty >/dev/null  # add gpg key
curl -fsSL https://repo.pigsty.io/yum/repo | sudo tee /etc/yum.repos.d/pigsty.repo        >/dev/null  # add repo file
sudo yum makecache; # sudo yum install pig 
```


-------

## What's Inside

Linux x86_64/amd64 [Extension](https://ext.pgsty.com/list) packages for PostgreSQL 12 - 17, on El8, EL9, Ubuntu 22.04 and Debian 12.

Check the [extension list](https://ext.pgsty.com/list) for details.


----------------

## Contrib

If you have any suggestions on including new extensions or bumping to new versions, or find any mistake about metadata,
PR or [Issue](https://github.com/pgsty/ext/issues/new) are welcome!

You can edit the [`pigsty.csv`](https://github.com/pgsty/ext/blob/main/data/extension.csv) raw data and create a pull
request to update the metadata.

You can also suggest new extensions [here](https://github.com/orgs/pgsty/discussions/333)


--------

## Compatibility

`pig` runs on: RHEL 8/9, Ubuntu 22.04/24.04, and Debian 12, on both `amd64/arm64` arch

|  Code   | Distribution                   |  `x86_64`  | `aarch64`  |
|:-------:|--------------------------------|:----------:|:----------:|
| **el9** | RHEL 9 / Rocky9 / Alma9  / ... | PG 17 - 13 | PG 17 - 13 |
| **el8** | RHEL 8 / Rocky8 / Alma8 / ...  | PG 17 - 13 | PG 17 - 13 |
| **u24** | Ubuntu 24.04 (`noble`)         | PG 17 - 13 | PG 17 - 13 |
| **u22** | Ubuntu 22.04 (`jammy`)         | PG 17 - 13 | PG 17 - 13 |
| **d12** | Debian 12 (`bookworm`)         | PG 17 - 13 | PG 17 - 13 |

Here are some bad cases and limitations for the above distros:

- [`pg_duckdb`](https://ext.pigsty.io/#/pg_duckdb) `el8:*:*`
- [`pljava`](https://ext.pigsty.io/#/pljava): `el8:*:*`
- [`pllua`](https://ext.pigsty.io/#/pllua): `el8:arm:13,14,15`
- [`h3`](https://ext.pigsty.io/#/h3): `el8.amd.pg17`
- [`jdbc_fdw`](https://ext.pigsty.io/#/jdbc_fdw): `el:arm:*`
- [`pg_partman`](https://ext.pigsty.io/#/pg_partman): `u24:*:13`
- [`wiltondb`](https://ext.pigsty.io/#/babelfishpg_common): `d12:*:*`
- [`citus`](https://ext.pigsty.io/#/citus) and [`hydra`](https://ext.pigsty.io/#/hydra) are mutually exclusive
- [`pg_duckdb`](https://ext.pigsty.io/#/pg_duckdb) and [`pg_mooncake`](https://ext.pigsty.io/#/pg_mooncake) are mutually exclusive
- [`pg_duckdb`](https://ext.pigsty.io/#/pg_duckdb) will invalidate [`duckdb_fdw`](https://ext.pigsty.io/#/duckdb_fdw)
- [`documentdb_core`](https://ext.pigsty.io/#/documentdb_core) is not available on `arm` arch
- [`vchord`](https://ext.pigsty.io/#/vchord) 0.2+ is not available on `d12/u22` (0.1 available)

----------------

## About

[![Github: Repo](https://img.shields.io/badge/GitHub-Repo-slategray?style=flat&logo=github&logoColor=black)](https://github.com/pgsty/extension)
[![Author: RuohangFeng](https://img.shields.io/badge/Author-Ruohang_Feng-steelblue?style=flat)](https://vonng.com/)
[![About: @Vonng](https://img.shields.io/badge/%40Vonng-steelblue?style=flat)](https://vonng.com/en/)
[![Mail: rh@vonng.com](https://img.shields.io/badge/rh%40vonng.com-steelblue?style=flat)](mailto:rh@vonng.com)
[![Copyright: 2018-2025 rh@Vonng.com](https://img.shields.io/badge/Copyright-2018--2025_(rh%40vonng.com)-red?logo=c&color=steelblue)](https://github.com/Vonng)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache2.0-steelblue?style=flat&logo=opensourceinitiative&logoColor=green)](https://pigsty.io/docs/about/license/)