# pg_search


> [pg_search](https://github.com/paradedb/paradedb/tree/dev/pg_search): Full text search for PostgreSQL using BM25
>
> https://github.com/paradedb/paradedb/tree/dev/pg_search





[FTS](/fts) extensions: [`pg_search`](/pg_search), [`pgroonga`](/pgroonga), [`pgroonga_database`](/pgroonga_database), [`pg_bigm`](/pg_bigm), [`zhparser`](/zhparser), [`pg_bestmatch`](/pg_bestmatch), [`vchord_bm25`](/vchord_bm25), [`pg_tokenizer`](/pg_tokenizer), [`hunspell_cs_cz`](/hunspell_cs_cz), [`hunspell_de_de`](/hunspell_de_de), [`hunspell_en_us`](/hunspell_en_us), [`hunspell_fr`](/hunspell_fr), [`hunspell_ne_np`](/hunspell_ne_np), [`hunspell_nl_nl`](/hunspell_nl_nl), [`hunspell_nn_no`](/hunspell_nn_no), [`hunspell_pt_pt`](/hunspell_pt_pt), [`hunspell_ru_ru`](/hunspell_ru_ru), [`hunspell_ru_ru_aot`](/hunspell_ru_ru_aot), [`fuzzystrmatch`](/fuzzystrmatch), [`pg_trgm`](/pg_trgm)


-------
## Extension


| Extension | Version | License | RPM | DEB | PL |
|-----------|:-------:|:-------:|:---:|:---:|:--:|
| [pg_search](https://github.com/paradedb/paradedb/tree/dev/pg_search) | 0.16.2 | **<span class="tcwarn">AGPLv3</span>** | **<span class="tcwarn">PIGSTY</span>** | **<span class="tcwarn">PIGSTY</span>** | `Rust` |



| `Bin` | `LOAD` | `DYLIB` | `DDL` | `TRUST` | `RELOC` |
|:-----:|:------:|:-------:|:-----:|:-------:|:-------:|
|  |  | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | <span class="tcwarn">✘</span> |



| Alias | Tags | Schemas | Requires | Required by |
|-------|------|---------|----------|-------------|
| [pg_search](/pg_search) | `pgrx` | `paradedb` |  |  |



| Distro / Ver | PG17 | PG16 | PG15 | PG14 | PG13 |
|:------------:|:----:|:----:|:----:|:----:|:----:|
| `el8` | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | <span class="tcred">✘</span> |
| `el9` | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | <span class="tcred">✘</span> |
| `d12` | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | <span class="tcred">✘</span> |
| `u22` | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | <span class="tcred">✘</span> |
| `u24` | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | <span class="tcred">✘</span> |





```sql
CREATE EXTENSION pg_search;
```
> **Comment**: pgrx=0.14.1 0.15.19+ has broken libicu on el systems, build by ParadeDB team 
-----------


## Packages


| OS | Version | License | REPO | Package Pattern | 17 | 16 | 15 | 14 | 13 | Dependency |
|:--:|---------|:-------:|:----:|-----------------|:--:|:--:|:--:|:--:|:--:|------------|
| [RPM](/rpm) | 0.15.18 | **<span class="tcwarn">AGPLv3</span>** | **<span class="tcwarn">PIGSTY</span>** | `pg_search_$v` | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** |  |  |
| [DEB](/deb) | 0.16.2 | **<span class="tcwarn">AGPLv3</span>** | **<span class="tcwarn">PIGSTY</span>** | `postgresql-$v-pg-search` | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** |  |  |



Install `pg_search` via the [`pig`](https://github.com/pgsty/pig) cli tool:

```bash
pig ext add pg_search
```


Install `pg_search` via [Pigsty](https://pigsty.io/docs/pgext/usage/install/) playbook:

```bash
./pgsql.yml -t pg_extension -e '{"pg_extensions": ["pg_search"]}'
```


Install `pg_search` [RPM](/rpm) from the **<span class="tcwarn">PIGSTY</span>** **YUM** repo:

```bash
dnf install pg_search_17;
dnf install pg_search_16;
dnf install pg_search_15;
dnf install pg_search_14;
```


Install `pg_search` [DEB](/deb) from the **<span class="tcwarn">PIGSTY</span>** **APT** repo:

```bash
apt install postgresql-17-pg-search;
apt install postgresql-16-pg-search;
apt install postgresql-15-pg-search;
apt install postgresql-14-pg-search;
```




| Distro / Ver | PG17 | PG16 | PG15 | PG14 | PG13 |
|:------------:|:----:|:----:|:----:|:----:|:----:|
| `el8` | `pg_search_17` | `pg_search_16` | `pg_search_15` | `pg_search_14` | <span class="tcred">✘</span> |
| `el9` | `pg_search_17` | `pg_search_16` | `pg_search_15` | `pg_search_14` | <span class="tcred">✘</span> |
| `d12` | `postgresql-17-pg-search` | `postgresql-16-pg-search` | `postgresql-15-pg-search` | `postgresql-14-pg-search` | <span class="tcred">✘</span> |
| `u22` | `postgresql-17-pg-search` | `postgresql-16-pg-search` | `postgresql-15-pg-search` | `postgresql-14-pg-search` | <span class="tcred">✘</span> |
| `u24` | `postgresql-17-pg-search` | `postgresql-16-pg-search` | `postgresql-15-pg-search` | `postgresql-14-pg-search` | <span class="tcred">✘</span> |





--------

## Usage

https://docs.paradedb.com/documentation/getting-started/quickstart

```sql
CREATE EXTENSION pg_search;

ALTER SYSTEM SET paradedb.pg_search_telemetry TO 'off';

CALL paradedb.create_bm25_test_table(
  schema_name => 'public',
  table_name => 'mock_items'
);
    
SELECT description, rating, category FROM mock_items LIMIT 3;

CALL paradedb.create_bm25(
        index_name => 'search_idx',
        schema_name => 'public',
        table_name => 'mock_items',
        key_field => 'id',
        text_fields => paradedb.field('description', tokenizer => paradedb.tokenizer('en_stem')) ||
                       paradedb.field('category'),
        numeric_fields => paradedb.field('rating')
     );

SELECT description, rating, category
FROM search_idx.search('(description:keyboard OR category:electronics) AND rating:>2',limit_rows => 5);

CALL paradedb.create_bm25(
        index_name => 'ngrams_idx',
        schema_name => 'public',
        table_name => 'mock_items',
        key_field => 'id',
        text_fields => paradedb.field('description', tokenizer => paradedb.tokenizer('ngram', min_gram => 4, max_gram => 4, prefix_only => false)) ||
                       paradedb.field('category')
     );

SELECT description, rating, category
FROM ngrams_idx.search('description:blue');
```
