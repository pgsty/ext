# periods


> [periods](https://github.com/xocolatl/periods): Provide Standard SQL functionality for PERIODs and SYSTEM VERSIONING
>
> https://github.com/xocolatl/periods





[TIME](/time) extensions: [`timescaledb`](/timescaledb), [`timescaledb_toolkit`](/timescaledb_toolkit), [`timeseries`](/timeseries), [`periods`](/periods), [`temporal_tables`](/temporal_tables), [`emaj`](/emaj), [`table_version`](/table_version), [`pg_cron`](/pg_cron), [`pg_task`](/pg_task), [`pg_later`](/pg_later), [`pg_background`](/pg_background)


-------
## Extension


| Extension | Version | License | RPM | DEB | PL |
|-----------|:-------:|:-------:|:---:|:---:|:--:|
| [periods](https://github.com/xocolatl/periods) | 1.2.3 | **<span class="tcblue">PostgreSQL</span>** | **<span class="tccyan">PGDG</span>** | **<span class="tccyan">PGDG</span>** | `C` |



| `Bin` | `LOAD` | `DYLIB` | `DDL` | `TRUST` | `RELOC` |
|:-----:|:------:|:-------:|:-----:|:-------:|:-------:|
|  |  | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | <span class="tcwarn">✘</span> | <span class="tcwarn">✘</span> |



| Alias | Tags | Schemas | Requires | Required by |
|-------|------|---------|----------|-------------|
| [periods](/periods) |  |  | [`btree_gist`](btree_gist) |  |



| Distro / Ver | PG17 | PG16 | PG15 | PG14 | PG13 |
|:------------:|:----:|:----:|:----:|:----:|:----:|
| `el8` | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> |
| `el9` | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> |
| `d12` | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> |
| `u22` | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> |
| `u24` | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> |





```sql
CREATE EXTENSION periods CASCADE;
```

-----------


## Packages


| OS | Version | License | REPO | Package Pattern | 17 | 16 | 15 | 14 | 13 | Dependency |
|:--:|---------|:-------:|:----:|-----------------|:--:|:--:|:--:|:--:|:--:|------------|
| [RPM](/rpm) | 1.2.2 | **<span class="tcblue">PostgreSQL</span>** | **<span class="tccyan">PGDG</span>** | `periods_$v*` | **<span class="tccyan">✔</span>** | **<span class="tccyan">✔</span>** | **<span class="tccyan">✔</span>** | **<span class="tccyan">✔</span>** | **<span class="tccyan">✔</span>** |  |
| [DEB](/deb) | 1.2.3 | **<span class="tcblue">PostgreSQL</span>** | **<span class="tccyan">PGDG</span>** | `postgresql-$v-periods` | **<span class="tccyan">✔</span>** | **<span class="tccyan">✔</span>** | **<span class="tccyan">✔</span>** | **<span class="tccyan">✔</span>** | **<span class="tccyan">✔</span>** |  |



Install `periods` via the [`pig`](https://github.com/pgsty/pig) cli tool:

```bash
pig ext add periods
```


Install `periods` via [Pigsty](https://pigsty.io/docs/pgext/usage/install/) playbook:

```bash
./pgsql.yml -t pg_extension -e '{"pg_extensions": ["periods"]}'
```


Install `periods` [RPM](/rpm) from the **<span class="tccyan">PGDG</span>** **YUM** repo:

```bash
dnf install periods_17*;
dnf install periods_16*;
dnf install periods_15*;
dnf install periods_14*;
dnf install periods_13*;
```


Install `periods` [DEB](/deb) from the **<span class="tccyan">PGDG</span>** **APT** repo:

```bash
apt install postgresql-17-periods;
apt install postgresql-16-periods;
apt install postgresql-15-periods;
apt install postgresql-14-periods;
apt install postgresql-13-periods;
```




| Distro / Ver | PG17 | PG16 | PG15 | PG14 | PG13 |
|:------------:|:----:|:----:|:----:|:----:|:----:|
| `el8` | `periods_17*` | `periods_16*` | `periods_15*` | `periods_14*` | `periods_13*` |
| `el9` | `periods_17*` | `periods_16*` | `periods_15*` | `periods_14*` | `periods_13*` |
| `d12` | `postgresql-17-periods` | `postgresql-16-periods` | `postgresql-15-periods` | `postgresql-14-periods` | `postgresql-13-periods` |
| `u22` | `postgresql-17-periods` | `postgresql-16-periods` | `postgresql-15-periods` | `postgresql-14-periods` | `postgresql-13-periods` |
| `u24` | `postgresql-17-periods` | `postgresql-16-periods` | `postgresql-15-periods` | `postgresql-14-periods` | `postgresql-13-periods` |





