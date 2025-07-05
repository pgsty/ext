# SIM


> SIM: Protocol Simulation & heterogeneous DBMS Compatibility: Oracle, MSSQL, DB2, MySQL, Memcached, and Babelfish!
## Extensions


There are 16 available extensions in this category:

[`documentdb`](/documentdb) [`documentdb_core`](/documentdb_core) [`documentdb_distributed`](/documentdb_distributed) [`orafce`](/orafce) [`pgtt`](/pgtt) [`session_variable`](/session_variable) [`pg_statement_rollback`](/pg_statement_rollback) [`pg_dbms_metadata`](/pg_dbms_metadata) [`pg_dbms_lock`](/pg_dbms_lock) [`pg_dbms_job`](/pg_dbms_job) [`babelfishpg_common`](/babelfishpg_common) [`babelfishpg_tsql`](/babelfishpg_tsql) [`babelfishpg_tds`](/babelfishpg_tds) [`babelfishpg_money`](/babelfishpg_money) [`spat`](/spat) [`pgmemcache`](/pgmemcache)


| ID | Extension | Version | Package | License | RPM | DEB | Website | `Bin` | `LOAD` | `DYLIB` | `DDL` | Description |
|:--:|-----------|:-------:|---------|:-------:|:---:|:---:|:-------:|:-----:|:------:|:-------:|:-----:|-------------|
| 9000 | [documentdb](/documentdb) | 0.103 | [documentdb](/documentdb) | **<span class="tcblue">MIT</span>** | **<span class="tcwarn">PIGSTY</span>** | **<span class="tcwarn">PIGSTY</span>** | [LINK](https://github.com/microsoft/documentdb) |  | <span class="tcred">❗</span> | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | API surface for DocumentDB for PostgreSQL |
| 9010 | [documentdb_core](/documentdb_core) | 0.103 | [documentdb](/documentdb_core) | **<span class="tcblue">MIT</span>** | **<span class="tcwarn">PIGSTY</span>** | **<span class="tcwarn">PIGSTY</span>** | [LINK](https://github.com/microsoft/documentdb) |  | <span class="tcred">❗</span> | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | Core API surface for DocumentDB for PostgreSQL |
| 9020 | [documentdb_distributed](/documentdb_distributed) | 0.103 | [documentdb](/documentdb_distributed) | **<span class="tcblue">MIT</span>** | **<span class="tcwarn">PIGSTY</span>** | **<span class="tcwarn">PIGSTY</span>** | [LINK](https://github.com/microsoft/documentdb) |  | <span class="tcred">❗</span> | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | Multi-Node API surface for DocumentDB |
| 9100 | [orafce](/orafce) | 4.14.4 | [orafce](/orafce) | **<span class="tcblue">BSD-0</span>** | **<span class="tccyan">PGDG</span>** | **<span class="tccyan">PGDG</span>** | [LINK](https://github.com/orafce/orafce) |  |  | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | Functions and operators that emulate a subset of functions and packages from the Oracle RDBMS |
| 9110 | [pgtt](/pgtt) | 4.3 | [pgtt](/pgtt) | **<span class="tcblue">ISC</span>** | **<span class="tccyan">PGDG</span>** | **<span class="tccyan">PGDG</span>** | [LINK](https://github.com/darold/pgtt) |  |  | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | Extension to add Global Temporary Tables feature to PostgreSQL |
| 9120 | [session_variable](/session_variable) | 3.4 | [session_variable](/session_variable) | **<span class="tcwarn">GPLv3</span>** | **<span class="tcwarn">PIGSTY</span>** | **<span class="tcwarn">PIGSTY</span>** | [LINK](https://github.com/splendiddata/session_variable) |  |  | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | Registration and manipulation of session variables and constants |
| 9130 | [pg_statement_rollback](/pg_statement_rollback) | 1.4 | [pg_statement_rollback](/pg_statement_rollback) | **<span class="tcblue">ISC</span>** | **<span class="tccyan">PGDG</span>** | **<span class="tcwarn">PIGSTY</span>** | [LINK](https://github.com/lzlabs/pg_statement_rollback) |  | <span class="tcred">❗</span> | <span class="tcblue">✔</span> | <span class="tcwarn">✘</span> | Server side rollback at statement level for PostgreSQL like Oracle or DB2 |
| 9240 | [pg_dbms_metadata](/pg_dbms_metadata) | 1.0.0 | [pg_dbms_metadata](/pg_dbms_metadata) | **<span class="tcblue">PostgreSQL</span>** | **<span class="tccyan">PGDG</span>** |  | [LINK](https://github.com/HexaCluster/pg_dbms_metadata) |  |  | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | Extension to add Oracle DBMS_METADATA compatibility to PostgreSQL |
| 9250 | [pg_dbms_lock](/pg_dbms_lock) | 1.0 | [pg_dbms_lock](/pg_dbms_lock) | **<span class="tcblue">PostgreSQL</span>** | **<span class="tccyan">PGDG</span>** |  | [LINK](https://github.com/HexaCluster/pg_dbms_lock) |  |  | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | Extension to add Oracle DBMS_LOCK full compatibility to PostgreSQL |
| 9260 | [pg_dbms_job](/pg_dbms_job) | 1.5 | [pg_dbms_job](/pg_dbms_job) | **<span class="tcblue">PostgreSQL</span>** | **<span class="tccyan">PGDG</span>** |  | [LINK](https://github.com/MigOpsRepos/pg_dbms_job) |  |  | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | Extension to add Oracle DBMS_JOB full compatibility to PostgreSQL |
| 9300 | [babelfishpg_common](/babelfishpg_common) | 3.3.3 | [babelfishpg_common](/babelfishpg_common) | **<span class="tccyan">Apache-2</span>** | **<span class="tcwarn">PIGSTY</span>** | **<span class="tcwarn">PIGSTY</span>** | [LINK](https://babelfishpg.org/) |  |  | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | SQL Server Transact SQL Datatype Support |
| 9310 | [babelfishpg_tsql](/babelfishpg_tsql) | 3.3.1 | [babelfishpg_tsql](/babelfishpg_tsql) | **<span class="tccyan">Apache-2</span>** | **<span class="tcwarn">PIGSTY</span>** | **<span class="tcwarn">PIGSTY</span>** | [LINK](https://babelfishpg.org/) |  | <span class="tcred">❗</span> | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | SQL Server Transact SQL compatibility |
| 9320 | [babelfishpg_tds](/babelfishpg_tds) | 1.0.0 | [babelfishpg_tds](/babelfishpg_tds) | **<span class="tccyan">Apache-2</span>** | **<span class="tcwarn">PIGSTY</span>** | **<span class="tcwarn">PIGSTY</span>** | [LINK](https://babelfishpg.org/) |  |  | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | SQL Server TDS protocol extension |
| 9330 | [babelfishpg_money](/babelfishpg_money) | 1.1.0 | [babelfishpg_money](/babelfishpg_money) | **<span class="tccyan">Apache-2</span>** | **<span class="tcwarn">PIGSTY</span>** | **<span class="tcwarn">PIGSTY</span>** | [LINK](https://babelfishpg.org/) |  |  | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | SQL Server Money Data Type |
| 9400 | [spat](/spat) | 0.1.0a4 | [spat](/spat) | **<span class="tcwarn">AGPLv3</span>** | **<span class="tccyan">PGDG</span>** | **<span class="tcwarn">PIGSTY</span>** | [LINK](https://github.com/Florents-Tselai/spat) |  |  | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | Redis-like In-Memory DB Embedded in Postgres |
| 9410 | [pgmemcache](/pgmemcache) | 2.3.0 | [pgmemcache](/pgmemcache) | **<span class="tcblue">MIT</span>** | **<span class="tccyan">PGDG</span>** | **<span class="tccyan">PGDG</span>** | [LINK](https://github.com/ohmu/pgmemcache) |  |  | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | memcached interface |



### RHEL 8 Compatible (el8)

```yaml
pg17: documentdb orafce pgtt session_variable pg_statement_rollback pg_dbms_metadata pg_dbms_lock spat pgmemcache #pg_dbms_job #wiltondb
pg16: documentdb orafce pgtt session_variable pg_statement_rollback pg_dbms_metadata pg_dbms_lock pgmemcache #pg_dbms_job #wiltondb #spat
pg15: documentdb orafce pgtt session_variable pg_statement_rollback pg_dbms_metadata pg_dbms_lock pgmemcache #pg_dbms_job #wiltondb #spat
pg14: orafce pgtt session_variable pg_statement_rollback pg_dbms_metadata pg_dbms_lock #documentdb #pg_dbms_job #wiltondb #spat #pgmemcache
pg13: orafce pgtt session_variable pg_statement_rollback pg_dbms_metadata pg_dbms_lock #documentdb #pg_dbms_job #wiltondb #spat #pgmemcache
```


### RHEL 9 Compatible (el9)

```yaml
pg17: documentdb orafce pgtt session_variable pg_statement_rollback pg_dbms_metadata pg_dbms_lock spat pgmemcache #pg_dbms_job #wiltondb
pg16: documentdb orafce pgtt session_variable pg_statement_rollback pg_dbms_metadata pg_dbms_lock pgmemcache #pg_dbms_job #wiltondb #spat
pg15: documentdb orafce pgtt session_variable pg_statement_rollback pg_dbms_metadata pg_dbms_lock pgmemcache #pg_dbms_job #wiltondb #spat
pg14: orafce pgtt session_variable pg_statement_rollback pg_dbms_metadata pg_dbms_lock #documentdb #pg_dbms_job #wiltondb #spat #pgmemcache
pg13: orafce pgtt session_variable pg_statement_rollback pg_dbms_metadata pg_dbms_lock #documentdb #pg_dbms_job #wiltondb #spat #pgmemcache
```


### Debian 12 bookworm Compatible (d12)

```yaml
pg17: documentdb orafce pgtt session_variable pg_statement_rollback spat pgmemcache #pg_dbms_metadata #pg_dbms_lock #pg_dbms_job
pg16: documentdb orafce pgtt session_variable pg_statement_rollback pgmemcache #pg_dbms_metadata #pg_dbms_lock #pg_dbms_job #spat
pg15: documentdb orafce pgtt session_variable pg_statement_rollback pgmemcache #pg_dbms_metadata #pg_dbms_lock #pg_dbms_job #spat
pg14: orafce pgtt session_variable pg_statement_rollback pgmemcache #documentdb #pg_dbms_metadata #pg_dbms_lock #pg_dbms_job #spat
pg13: orafce pgtt session_variable pg_statement_rollback pgmemcache #documentdb #pg_dbms_metadata #pg_dbms_lock #pg_dbms_job #spat
```


### Ubuntu 24.04 jammy Compatible (u22)

```yaml
pg17: documentdb orafce pgtt session_variable pg_statement_rollback spat pgmemcache #pg_dbms_metadata #pg_dbms_lock #pg_dbms_job #wiltondb
pg16: documentdb orafce pgtt session_variable pg_statement_rollback pgmemcache #pg_dbms_metadata #pg_dbms_lock #pg_dbms_job #wiltondb #spat
pg15: documentdb orafce pgtt session_variable pg_statement_rollback pgmemcache #pg_dbms_metadata #pg_dbms_lock #pg_dbms_job #wiltondb #spat
pg14: orafce pgtt session_variable pg_statement_rollback pgmemcache #documentdb #pg_dbms_metadata #pg_dbms_lock #pg_dbms_job #wiltondb #spat
pg13: orafce pgtt session_variable pg_statement_rollback pgmemcache #documentdb #pg_dbms_metadata #pg_dbms_lock #pg_dbms_job #wiltondb #spat
```


### Ubuntu 24.04 noble Compatible (u24)

```yaml
pg17: documentdb orafce pgtt session_variable pg_statement_rollback spat pgmemcache #pg_dbms_metadata #pg_dbms_lock #pg_dbms_job #wiltondb
pg16: documentdb orafce pgtt session_variable pg_statement_rollback pgmemcache #pg_dbms_metadata #pg_dbms_lock #pg_dbms_job #wiltondb #spat
pg15: documentdb orafce pgtt session_variable pg_statement_rollback pgmemcache #pg_dbms_metadata #pg_dbms_lock #pg_dbms_job #wiltondb #spat
pg14: orafce pgtt session_variable pg_statement_rollback pgmemcache #documentdb #pg_dbms_metadata #pg_dbms_lock #pg_dbms_job #wiltondb #spat
pg13: orafce pgtt session_variable pg_statement_rollback pgmemcache #documentdb #pg_dbms_metadata #pg_dbms_lock #pg_dbms_job #wiltondb #spat
```



--------

## RPM Packages


| Package | Version | License | RPM | RPM Package | 17 | 16 | 15 | 14 | 13 | Description |
|---------|---------|:-------:|:---:|-------------|:--:|:--:|:--:|:--:|:--:|-------------|
| [documentdb](/documentdb) | 0.103 | **<span class="tcblue">MIT</span>** | **<span class="tcwarn">PIGSTY</span>** | `documentdb_$v*` | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** |  |  | API surface for DocumentDB for PostgreSQL |
| [orafce](/orafce) | 4.14.4 | **<span class="tcblue">BSD-0</span>** | **<span class="tccyan">PGDG</span>** | `orafce_$v` | **<span class="tccyan">✔</span>** | **<span class="tccyan">✔</span>** | **<span class="tccyan">✔</span>** | **<span class="tccyan">✔</span>** | **<span class="tccyan">✔</span>** | Functions and operators that emulate a subset of functions and packages from the Oracle RDBMS |
| [pgtt](/pgtt) | 4.3 | **<span class="tcblue">ISC</span>** | **<span class="tccyan">PGDG</span>** | `pgtt_$v*` | **<span class="tccyan">✔</span>** | **<span class="tccyan">✔</span>** | **<span class="tccyan">✔</span>** | **<span class="tccyan">✔</span>** | **<span class="tccyan">✔</span>** | Extension to add Global Temporary Tables feature to PostgreSQL |
| [session_variable](/session_variable) | 3.4 | **<span class="tcwarn">GPLv3</span>** | **<span class="tcwarn">PIGSTY</span>** | `session_variable_$v*` | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | Registration and manipulation of session variables and constants |
| [pg_statement_rollback](/pg_statement_rollback) | 1.4 | **<span class="tcblue">ISC</span>** | **<span class="tccyan">PGDG</span>** | `pg_statement_rollback_$v*` | **<span class="tccyan">✔</span>** | **<span class="tccyan">✔</span>** | **<span class="tccyan">✔</span>** | **<span class="tccyan">✔</span>** | **<span class="tccyan">✔</span>** | Server side rollback at statement level for PostgreSQL like Oracle or DB2 |
| [pg_dbms_metadata](/pg_dbms_metadata) | 1.0.0 | **<span class="tcblue">PostgreSQL</span>** | **<span class="tccyan">PGDG</span>** | `pg_dbms_metadata_$v` | **<span class="tccyan">✔</span>** | **<span class="tccyan">✔</span>** | **<span class="tccyan">✔</span>** | **<span class="tccyan">✔</span>** | **<span class="tccyan">✔</span>** | Extension to add Oracle DBMS_METADATA compatibility to PostgreSQL |
| [pg_dbms_lock](/pg_dbms_lock) | 1.0 | **<span class="tcblue">PostgreSQL</span>** | **<span class="tccyan">PGDG</span>** | `pg_dbms_lock_$v` | **<span class="tccyan">✔</span>** | **<span class="tccyan">✔</span>** | **<span class="tccyan">✔</span>** | **<span class="tccyan">✔</span>** | **<span class="tccyan">✔</span>** | Extension to add Oracle DBMS_LOCK full compatibility to PostgreSQL |
| [pg_dbms_job](/pg_dbms_job) | 1.5 | **<span class="tcblue">PostgreSQL</span>** | **<span class="tccyan">PGDG</span>** | `pg_dbms_job_$v` | **<span class="tccyan">✔</span>** | **<span class="tccyan">✔</span>** | **<span class="tccyan">✔</span>** | **<span class="tccyan">✔</span>** | **<span class="tccyan">✔</span>** | Extension to add Oracle DBMS_JOB full compatibility to PostgreSQL |
| [babelfishpg_common](/babelfishpg_common) | 3.3.3 | **<span class="tccyan">Apache-2</span>** | **<span class="tcwarn">PIGSTY</span>** | `babelfishpg-common*` |  |  | **<span class="tcwarn">✔</span>** |  |  | SQL Server Transact SQL Datatype Support |
| [babelfishpg_tsql](/babelfishpg_tsql) | 3.3.1 | **<span class="tccyan">Apache-2</span>** | **<span class="tcwarn">PIGSTY</span>** | `babelfishpg-tsql*` |  |  | **<span class="tcwarn">✔</span>** |  |  | SQL Server Transact SQL compatibility |
| [babelfishpg_tds](/babelfishpg_tds) | 1.0.0 | **<span class="tccyan">Apache-2</span>** | **<span class="tcwarn">PIGSTY</span>** | `babelfishpg-tds*` |  |  | **<span class="tcwarn">✔</span>** |  |  | SQL Server TDS protocol extension |
| [babelfishpg_money](/babelfishpg_money) | 1.1.0 | **<span class="tccyan">Apache-2</span>** | **<span class="tcwarn">PIGSTY</span>** | `babelfishpg-money*` |  |  | **<span class="tcwarn">✔</span>** |  |  | SQL Server Money Data Type |
| [spat](/spat) | 0.1.0a4 | **<span class="tcwarn">AGPLv3</span>** | **<span class="tccyan">PGDG</span>** | `spat_$v*` | **<span class="tccyan">✔</span>** |  |  |  |  | Redis-like In-Memory DB Embedded in Postgres |
| [pgmemcache](/pgmemcache) | 2.3.0 | **<span class="tcblue">MIT</span>** | **<span class="tccyan">PGDG</span>** | `pgmemcache_$v*` | **<span class="tccyan">✔</span>** | **<span class="tccyan">✔</span>** | **<span class="tccyan">✔</span>** |  |  | memcached interface |



### RHEL 8 Compatible (el8)

```yaml
pg17: documentdb_17* orafce_17 pgtt_17* session_variable_17* pg_statement_rollback_17* pg_dbms_metadata_17 pg_dbms_lock_17 spat_17* pgmemcache_17* #pg_dbms_job_17 #wiltondb
pg16: documentdb_16* orafce_16 pgtt_16* session_variable_16* pg_statement_rollback_16* pg_dbms_metadata_16 pg_dbms_lock_16 pgmemcache_16* #pg_dbms_job_16 #wiltondb #spat_16*
pg15: documentdb_15* orafce_15 pgtt_15* session_variable_15* pg_statement_rollback_15* pg_dbms_metadata_15 pg_dbms_lock_15 pgmemcache_15* #pg_dbms_job_15 #wiltondb #spat_15*
pg14: orafce_14 pgtt_14* session_variable_14* pg_statement_rollback_14* pg_dbms_metadata_14 pg_dbms_lock_14 #documentdb_14* #pg_dbms_job_14 #wiltondb #spat_14* #pgmemcache_14*
pg13: orafce_13 pgtt_13* session_variable_13* pg_statement_rollback_13* pg_dbms_metadata_13 pg_dbms_lock_13 #documentdb_13* #pg_dbms_job_13 #wiltondb #spat_13* #pgmemcache_13*
```


### RHEL 9 Compatible (el9)

```yaml
pg17: documentdb_17* orafce_17 pgtt_17* session_variable_17* pg_statement_rollback_17* pg_dbms_metadata_17 pg_dbms_lock_17 spat_17* pgmemcache_17* #pg_dbms_job_17 #wiltondb
pg16: documentdb_16* orafce_16 pgtt_16* session_variable_16* pg_statement_rollback_16* pg_dbms_metadata_16 pg_dbms_lock_16 pgmemcache_16* #pg_dbms_job_16 #wiltondb #spat_16*
pg15: documentdb_15* orafce_15 pgtt_15* session_variable_15* pg_statement_rollback_15* pg_dbms_metadata_15 pg_dbms_lock_15 pgmemcache_15* #pg_dbms_job_15 #wiltondb #spat_15*
pg14: orafce_14 pgtt_14* session_variable_14* pg_statement_rollback_14* pg_dbms_metadata_14 pg_dbms_lock_14 #documentdb_14* #pg_dbms_job_14 #wiltondb #spat_14* #pgmemcache_14*
pg13: orafce_13 pgtt_13* session_variable_13* pg_statement_rollback_13* pg_dbms_metadata_13 pg_dbms_lock_13 #documentdb_13* #pg_dbms_job_13 #wiltondb #spat_13* #pgmemcache_13*
```



--------

## DEB Packages


| Package | Version | License | DEB | DEB Package | 17 | 16 | 15 | 14 | 13 | Description |
|---------|---------|:-------:|:---:|-------------|:--:|:--:|:--:|:--:|:--:|-------------|
| [documentdb](/documentdb) | 0.103 | **<span class="tcblue">MIT</span>** | **<span class="tcwarn">PIGSTY</span>** | `postgresql-$v-documentdb` | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** |  |  | API surface for DocumentDB for PostgreSQL |
| [orafce](/orafce) | 4.14.3 | **<span class="tcblue">BSD-0</span>** | **<span class="tccyan">PGDG</span>** | `postgresql-$v-orafce` | **<span class="tccyan">✔</span>** | **<span class="tccyan">✔</span>** | **<span class="tccyan">✔</span>** | **<span class="tccyan">✔</span>** | **<span class="tccyan">✔</span>** | Functions and operators that emulate a subset of functions and packages from the Oracle RDBMS |
| [pgtt](/pgtt) | 4.1 | **<span class="tcblue">ISC</span>** | **<span class="tccyan">PGDG</span>** | `postgresql-$v-pgtt` | **<span class="tccyan">✔</span>** | **<span class="tccyan">✔</span>** | **<span class="tccyan">✔</span>** | **<span class="tccyan">✔</span>** | **<span class="tccyan">✔</span>** | Extension to add Global Temporary Tables feature to PostgreSQL |
| [session_variable](/session_variable) | 3.4 | **<span class="tcwarn">GPLv3</span>** | **<span class="tcwarn">PIGSTY</span>** | `postgresql-$v-session-variable` | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | Registration and manipulation of session variables and constants |
| [pg_statement_rollback](/pg_statement_rollback) | 1.4 | **<span class="tcblue">ISC</span>** | **<span class="tcwarn">PIGSTY</span>** | `postgresql-$v-pg-statement-rollback` | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | Server side rollback at statement level for PostgreSQL like Oracle or DB2 |
| [babelfishpg_common](/babelfishpg_common) | 3.3.3 | **<span class="tccyan">Apache-2</span>** | **<span class="tcwarn">PIGSTY</span>** | `babelfishpg-common` |  |  | **<span class="tcwarn">✔</span>** |  |  | SQL Server Transact SQL Datatype Support |
| [babelfishpg_tsql](/babelfishpg_tsql) | 3.3.1 | **<span class="tccyan">Apache-2</span>** | **<span class="tcwarn">PIGSTY</span>** | `babelfishpg-tsql` |  |  | **<span class="tcwarn">✔</span>** |  |  | SQL Server Transact SQL compatibility |
| [babelfishpg_tds](/babelfishpg_tds) | 1.0.0 | **<span class="tccyan">Apache-2</span>** | **<span class="tcwarn">PIGSTY</span>** | `babelfishpg-tds` |  |  | **<span class="tcwarn">✔</span>** |  |  | SQL Server TDS protocol extension |
| [babelfishpg_money](/babelfishpg_money) | 1.1.0 | **<span class="tccyan">Apache-2</span>** | **<span class="tcwarn">PIGSTY</span>** | `babelfishpg-money` |  |  | **<span class="tcwarn">✔</span>** |  |  | SQL Server Money Data Type |
| [spat](/spat) | 0.1.0a4 | **<span class="tcwarn">AGPLv3</span>** | **<span class="tcwarn">PIGSTY</span>** | `postgresql-$v-spat` | **<span class="tcwarn">✔</span>** |  |  |  |  | Redis-like In-Memory DB Embedded in Postgres |
| [pgmemcache](/pgmemcache) | 2.3.0 | **<span class="tcblue">MIT</span>** | **<span class="tccyan">PGDG</span>** | `postgresql-$v-pgmemcache` | **<span class="tccyan">✔</span>** | **<span class="tccyan">✔</span>** | **<span class="tccyan">✔</span>** | **<span class="tccyan">✔</span>** | **<span class="tccyan">✔</span>** | memcached interface |



### Debian 12 bookworm Compatible (d12)

```yaml
pg17: postgresql-17-documentdb postgresql-17-orafce postgresql-17-pgtt postgresql-17-session-variable postgresql-17-pg-statement-rollback postgresql-17-spat postgresql-17-pgmemcache
pg16: postgresql-16-documentdb postgresql-16-orafce postgresql-16-pgtt postgresql-16-session-variable postgresql-16-pg-statement-rollback postgresql-16-pgmemcache # #postgresql-16-spat
pg15: postgresql-15-documentdb postgresql-15-orafce postgresql-15-pgtt postgresql-15-session-variable postgresql-15-pg-statement-rollback postgresql-15-pgmemcache # #postgresql-15-spat
pg14: postgresql-14-orafce postgresql-14-pgtt postgresql-14-session-variable postgresql-14-pg-statement-rollback postgresql-14-pgmemcache #postgresql-14-documentdb # #postgresql-14-spat
pg13: postgresql-13-orafce postgresql-13-pgtt postgresql-13-session-variable postgresql-13-pg-statement-rollback postgresql-13-pgmemcache #postgresql-13-documentdb # #postgresql-13-spat
```


### Ubuntu 24.04 jammy Compatible (u22)

```yaml
pg17: postgresql-17-documentdb postgresql-17-orafce postgresql-17-pgtt postgresql-17-session-variable postgresql-17-pg-statement-rollback postgresql-17-spat postgresql-17-pgmemcache # #wiltondb
pg16: postgresql-16-documentdb postgresql-16-orafce postgresql-16-pgtt postgresql-16-session-variable postgresql-16-pg-statement-rollback postgresql-16-pgmemcache # #wiltondb #postgresql-16-spat
pg15: postgresql-15-documentdb postgresql-15-orafce postgresql-15-pgtt postgresql-15-session-variable postgresql-15-pg-statement-rollback postgresql-15-pgmemcache # #wiltondb #postgresql-15-spat
pg14: postgresql-14-orafce postgresql-14-pgtt postgresql-14-session-variable postgresql-14-pg-statement-rollback postgresql-14-pgmemcache #postgresql-14-documentdb # #wiltondb #postgresql-14-spat
pg13: postgresql-13-orafce postgresql-13-pgtt postgresql-13-session-variable postgresql-13-pg-statement-rollback postgresql-13-pgmemcache #postgresql-13-documentdb # #wiltondb #postgresql-13-spat
```


### Ubuntu 24.04 noble Compatible (u24)

```yaml
pg17: postgresql-17-documentdb postgresql-17-orafce postgresql-17-pgtt postgresql-17-session-variable postgresql-17-pg-statement-rollback postgresql-17-spat postgresql-17-pgmemcache # #wiltondb
pg16: postgresql-16-documentdb postgresql-16-orafce postgresql-16-pgtt postgresql-16-session-variable postgresql-16-pg-statement-rollback postgresql-16-pgmemcache # #wiltondb #postgresql-16-spat
pg15: postgresql-15-documentdb postgresql-15-orafce postgresql-15-pgtt postgresql-15-session-variable postgresql-15-pg-statement-rollback postgresql-15-pgmemcache # #wiltondb #postgresql-15-spat
pg14: postgresql-14-orafce postgresql-14-pgtt postgresql-14-session-variable postgresql-14-pg-statement-rollback postgresql-14-pgmemcache #postgresql-14-documentdb # #wiltondb #postgresql-14-spat
pg13: postgresql-13-orafce postgresql-13-pgtt postgresql-13-session-variable postgresql-13-pg-statement-rollback postgresql-13-pgmemcache #postgresql-13-documentdb # #wiltondb #postgresql-13-spat
```



--------
