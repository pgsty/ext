# pg_ivm


> [pg_ivm](https://github.com/sraoss/pg_ivm): incremental view maintenance on PostgreSQL
>
> https://github.com/sraoss/pg_ivm





[FEAT](/feat) extensions: [`age`](/age), [`hll`](/hll), [`rum`](/rum), [`pg_graphql`](/pg_graphql), [`pg_jsonschema`](/pg_jsonschema), [`jsquery`](/jsquery), [`pg_hint_plan`](/pg_hint_plan), [`hypopg`](/hypopg), [`index_advisor`](/index_advisor), [`plan_filter`](/plan_filter), [`imgsmlr`](/imgsmlr), [`pg_ivm`](/pg_ivm), [`pg_incremental`](/pg_incremental), [`pgmq`](/pgmq), [`pgq`](/pgq), [`orioledb`](/orioledb), [`pg_cardano`](/pg_cardano), [`rdkit`](/rdkit), [`omni`](/omni), [`omni_auth`](/omni_auth), [`omni_aws`](/omni_aws), [`omni_cloudevents`](/omni_cloudevents), [`omni_containers`](/omni_containers), [`omni_credentials`](/omni_credentials), [`omni_email`](/omni_email), [`omni_http`](/omni_http), [`omni_httpc`](/omni_httpc), [`omni_httpd`](/omni_httpd), [`omni_id`](/omni_id), [`omni_json`](/omni_json), [`omni_kube`](/omni_kube), [`omni_ledger`](/omni_ledger), [`omni_manifest`](/omni_manifest), [`omni_mimetypes`](/omni_mimetypes), [`omni_os`](/omni_os), [`omni_polyfill`](/omni_polyfill), [`omni_python`](/omni_python), [`omni_regex`](/omni_regex), [`omni_rest`](/omni_rest), [`omni_schema`](/omni_schema), [`omni_seq`](/omni_seq), [`omni_service`](/omni_service), [`omni_session`](/omni_session), [`omni_sql`](/omni_sql), [`omni_sqlite`](/omni_sqlite), [`omni_test`](/omni_test), [`omni_txn`](/omni_txn), [`omni_types`](/omni_types), [`omni_var`](/omni_var), [`omni_vfs`](/omni_vfs), [`omni_vfs_types_v1`](/omni_vfs_types_v1), [`omni_web`](/omni_web), [`omni_worker`](/omni_worker), [`omni_xml`](/omni_xml), [`omni_yaml`](/omni_yaml), [`bloom`](/bloom)


-------
## Extension


| Extension | Version | License | RPM | DEB | PL |
|-----------|:-------:|:-------:|:---:|:---:|:--:|
| [pg_ivm](https://github.com/sraoss/pg_ivm) | 1.11 | **<span class="tcblue">PostgreSQL</span>** | **<span class="tccyan">PGDG</span>** | **<span class="tcwarn">PIGSTY</span>** | `C` |



| `Bin` | `LOAD` | `DYLIB` | `DDL` | `TRUST` | `RELOC` |
|:-----:|:------:|:-------:|:-----:|:-------:|:-------:|
|  |  | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | <span class="tcwarn">✘</span> | <span class="tcwarn">✘</span> |



| Alias | Tags | Schemas | Requires | Required by |
|-------|------|---------|----------|-------------|
| [pg_ivm](/pg_ivm) |  | `pg_catalog` |  | [`timeseries`](/timeseries) |



| Distro / Ver | PG17 | PG16 | PG15 | PG14 | PG13 |
|:------------:|:----:|:----:|:----:|:----:|:----:|
| `el8` | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> |
| `el9` | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> |
| `d12` | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> |
| `u22` | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> |
| `u24` | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> |





```sql
CREATE EXTENSION pg_ivm;
```
> **Comment**: no pg12 on el8/9 pgdg repo
-----------


## Packages


| OS | Version | License | REPO | Package Pattern | 17 | 16 | 15 | 14 | 13 | Dependency |
|:--:|---------|:-------:|:----:|-----------------|:--:|:--:|:--:|:--:|:--:|------------|
| [RPM](/rpm) | 1.11 | **<span class="tcblue">PostgreSQL</span>** | **<span class="tccyan">PGDG</span>** | `pg_ivm_$v*` | **<span class="tccyan">✔</span>** | **<span class="tccyan">✔</span>** | **<span class="tccyan">✔</span>** | **<span class="tccyan">✔</span>** | **<span class="tccyan">✔</span>** |  |
| [DEB](/deb) | 1.11 | **<span class="tcblue">PostgreSQL</span>** | **<span class="tcwarn">PIGSTY</span>** | `postgresql-$v-pg-ivm` | **<span class="tccyan">✔</span>** | **<span class="tccyan">✔</span>** | **<span class="tccyan">✔</span>** | **<span class="tccyan">✔</span>** | **<span class="tccyan">✔</span>** |  |



Install `pg_ivm` via the [`pig`](https://github.com/pgsty/pig) cli tool:

```bash
pig ext add pg_ivm
```


Install `pg_ivm` via [Pigsty](https://pigsty.io/docs/pgext/usage/install/) playbook:

```bash
./pgsql.yml -t pg_extension -e '{"pg_extensions": ["pg_ivm"]}'
```


Install `pg_ivm` [RPM](/rpm) from the **<span class="tccyan">PGDG</span>** **YUM** repo:

```bash
dnf install pg_ivm_17*;
dnf install pg_ivm_16*;
dnf install pg_ivm_15*;
dnf install pg_ivm_14*;
dnf install pg_ivm_13*;
```


Install `pg_ivm` [DEB](/deb) from the **<span class="tcwarn">PIGSTY</span>** **APT** repo:

```bash
apt install postgresql-17-pg-ivm;
apt install postgresql-16-pg-ivm;
apt install postgresql-15-pg-ivm;
apt install postgresql-14-pg-ivm;
apt install postgresql-13-pg-ivm;
```




| Distro / Ver | PG17 | PG16 | PG15 | PG14 | PG13 |
|:------------:|:----:|:----:|:----:|:----:|:----:|
| `el8` | `pg_ivm_17*` | `pg_ivm_16*` | `pg_ivm_15*` | `pg_ivm_14*` | `pg_ivm_13*` |
| `el9` | `pg_ivm_17*` | `pg_ivm_16*` | `pg_ivm_15*` | `pg_ivm_14*` | `pg_ivm_13*` |
| `d12` | `postgresql-17-pg-ivm` | `postgresql-16-pg-ivm` | `postgresql-15-pg-ivm` | `postgresql-14-pg-ivm` | `postgresql-13-pg-ivm` |
| `u22` | `postgresql-17-pg-ivm` | `postgresql-16-pg-ivm` | `postgresql-15-pg-ivm` | `postgresql-14-pg-ivm` | `postgresql-13-pg-ivm` |
| `u24` | `postgresql-17-pg-ivm` | `postgresql-16-pg-ivm` | `postgresql-15-pg-ivm` | `postgresql-14-pg-ivm` | `postgresql-13-pg-ivm` |





