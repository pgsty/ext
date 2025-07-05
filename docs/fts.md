# FTS


> FTS: ElasticSearch Alternative with BM25, 2-gram/3-gram Fuzzy Search, Zhparser & Hunspell Segregation Dicts, etc...
## Extensions


There are 20 available extensions in this category:

[`pg_search`](/pg_search) [`pgroonga`](/pgroonga) [`pgroonga_database`](/pgroonga_database) [`pg_bigm`](/pg_bigm) [`zhparser`](/zhparser) [`pg_bestmatch`](/pg_bestmatch) [`vchord_bm25`](/vchord_bm25) [`pg_tokenizer`](/pg_tokenizer) [`hunspell_cs_cz`](/hunspell_cs_cz) [`hunspell_de_de`](/hunspell_de_de) [`hunspell_en_us`](/hunspell_en_us) [`hunspell_fr`](/hunspell_fr) [`hunspell_ne_np`](/hunspell_ne_np) [`hunspell_nl_nl`](/hunspell_nl_nl) [`hunspell_nn_no`](/hunspell_nn_no) [`hunspell_pt_pt`](/hunspell_pt_pt) [`hunspell_ru_ru`](/hunspell_ru_ru) [`hunspell_ru_ru_aot`](/hunspell_ru_ru_aot) [`fuzzystrmatch`](/fuzzystrmatch) [`pg_trgm`](/pg_trgm)


| ID | Extension | Version | Package | License | RPM | DEB | Website | `Bin` | `LOAD` | `DYLIB` | `DDL` | Description |
|:--:|-----------|:-------:|---------|:-------:|:---:|:---:|:-------:|:-----:|:------:|:-------:|:-----:|-------------|
| 2100 | [pg_search](/pg_search) | 0.16.2 | [pg_search](/pg_search) | **<span class="tcwarn">AGPLv3</span>** | **<span class="tcwarn">PIGSTY</span>** | **<span class="tcwarn">PIGSTY</span>** | [LINK](https://github.com/paradedb/paradedb/tree/dev/pg_search) |  |  | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | Full text search for PostgreSQL using BM25 |
| 2110 | [pgroonga](/pgroonga) | 4.0.0 | [pgroonga](/pgroonga) | **<span class="tcblue">PostgreSQL</span>** | **<span class="tcwarn">PIGSTY</span>** | **<span class="tcwarn">PIGSTY</span>** | [LINK](https://github.com/pgroonga/pgroonga) |  |  | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | Use Groonga as index, fast full text search platform for all languages! |
| 2111 | [pgroonga_database](/pgroonga_database) | 4.0.0 | [pgroonga](/pgroonga_database) | **<span class="tcblue">PostgreSQL</span>** | **<span class="tcwarn">PIGSTY</span>** | **<span class="tcwarn">PIGSTY</span>** | [LINK](https://github.com/pgroonga/pgroonga) |  |  | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | PGroonga database management module |
| 2120 | [pg_bigm](/pg_bigm) | 1.2 | [pg_bigm](/pg_bigm) | **<span class="tcblue">PostgreSQL</span>** | **<span class="tccyan">PGDG</span>** | **<span class="tcwarn">PIGSTY</span>** | [LINK](https://github.com/pgbigm/pg_bigm) |  |  | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | create 2-gram (bigram) index for faster full text search. |
| 2130 | [zhparser](/zhparser) | 2.3 | [zhparser](/zhparser) | **<span class="tcblue">PostgreSQL</span>** | **<span class="tcwarn">PIGSTY</span>** | **<span class="tcwarn">PIGSTY</span>** | [LINK](https://github.com/amutu/zhparser) |  |  | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | a parser for full-text search of Chinese |
| 2140 | [pg_bestmatch](/pg_bestmatch) | 0.0.1 | [pg_bestmatch](/pg_bestmatch) | **<span class="tccyan">Apache-2</span>** | **<span class="tcwarn">PIGSTY</span>** | **<span class="tcwarn">PIGSTY</span>** | [LINK](https://github.com/tensorchord/pg_bestmatch.rs) |  | <span class="tcred">❗</span> | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | Generate BM25 sparse vector inside PostgreSQL |
| 2150 | [vchord_bm25](/vchord_bm25) | 0.2.1 | [vchord_bm25](/vchord_bm25) | **<span class="tcwarn">AGPLv3</span>** | **<span class="tcwarn">PIGSTY</span>** | **<span class="tcwarn">PIGSTY</span>** | [LINK](https://github.com/tensorchord/VectorChord-bm25) |  | <span class="tcred">❗</span> | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | A postgresql extension for bm25 ranking algorithm |
| 2160 | [pg_tokenizer](/pg_tokenizer) | 0.1.0 | [pg_tokenizer](/pg_tokenizer) | **<span class="tccyan">Apache-2</span>** | **<span class="tcwarn">PIGSTY</span>** | **<span class="tcwarn">PIGSTY</span>** | [LINK](https://github.com/tensorchord/pg_tokenizer.rs) |  |  | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | Tokenizers for full-text search |
| 2170 | [hunspell_cs_cz](/hunspell_cs_cz) | 1.0 | [hunspell_cs_cz](/hunspell_cs_cz) | **<span class="tcblue">PostgreSQL</span>** | **<span class="tcwarn">PIGSTY</span>** | **<span class="tcwarn">PIGSTY</span>** | [LINK](https://github.com/postgrespro/hunspell_dicts) |  |  | <span class="tcwarn">✘</span> | <span class="tcblue">✔</span> | Czech Hunspell Dictionary |
| 2171 | [hunspell_de_de](/hunspell_de_de) | 1.0 | [hunspell_de_de](/hunspell_de_de) | **<span class="tcblue">PostgreSQL</span>** | **<span class="tcwarn">PIGSTY</span>** | **<span class="tcwarn">PIGSTY</span>** | [LINK](https://github.com/postgrespro/hunspell_dicts) |  |  | <span class="tcwarn">✘</span> | <span class="tcblue">✔</span> | German Hunspell Dictionary |
| 2172 | [hunspell_en_us](/hunspell_en_us) | 1.0 | [hunspell_en_us](/hunspell_en_us) | **<span class="tcblue">PostgreSQL</span>** | **<span class="tcwarn">PIGSTY</span>** | **<span class="tcwarn">PIGSTY</span>** | [LINK](https://github.com/postgrespro/hunspell_dicts) |  |  | <span class="tcwarn">✘</span> | <span class="tcblue">✔</span> | en_US Hunspell Dictionary |
| 2173 | [hunspell_fr](/hunspell_fr) | 1.0 | [hunspell_fr](/hunspell_fr) | **<span class="tcblue">PostgreSQL</span>** | **<span class="tcwarn">PIGSTY</span>** | **<span class="tcwarn">PIGSTY</span>** | [LINK](https://github.com/postgrespro/hunspell_dicts) |  |  | <span class="tcwarn">✘</span> | <span class="tcblue">✔</span> | French Hunspell Dictionary |
| 2174 | [hunspell_ne_np](/hunspell_ne_np) | 1.0 | [hunspell_ne_np](/hunspell_ne_np) | **<span class="tcblue">PostgreSQL</span>** | **<span class="tcwarn">PIGSTY</span>** | **<span class="tcwarn">PIGSTY</span>** | [LINK](https://github.com/postgrespro/hunspell_dicts) |  |  | <span class="tcwarn">✘</span> | <span class="tcblue">✔</span> | Nepali Hunspell Dictionary |
| 2175 | [hunspell_nl_nl](/hunspell_nl_nl) | 1.0 | [hunspell_nl_nl](/hunspell_nl_nl) | **<span class="tcblue">PostgreSQL</span>** | **<span class="tcwarn">PIGSTY</span>** | **<span class="tcwarn">PIGSTY</span>** | [LINK](https://github.com/postgrespro/hunspell_dicts) |  |  | <span class="tcwarn">✘</span> | <span class="tcblue">✔</span> | Dutch Hunspell Dictionary |
| 2176 | [hunspell_nn_no](/hunspell_nn_no) | 1.0 | [hunspell_nn_no](/hunspell_nn_no) | **<span class="tcblue">PostgreSQL</span>** | **<span class="tcwarn">PIGSTY</span>** | **<span class="tcwarn">PIGSTY</span>** | [LINK](https://github.com/postgrespro/hunspell_dicts) |  |  | <span class="tcwarn">✘</span> | <span class="tcblue">✔</span> | Norwegian (norsk) Hunspell Dictionary |
| 2177 | [hunspell_pt_pt](/hunspell_pt_pt) | 1.0 | [hunspell_pt_pt](/hunspell_pt_pt) | **<span class="tcblue">PostgreSQL</span>** | **<span class="tcwarn">PIGSTY</span>** | **<span class="tcwarn">PIGSTY</span>** | [LINK](https://github.com/postgrespro/hunspell_dicts) |  |  | <span class="tcwarn">✘</span> | <span class="tcblue">✔</span> | Portuguese Hunspell Dictionary |
| 2178 | [hunspell_ru_ru](/hunspell_ru_ru) | 1.0 | [hunspell_ru_ru](/hunspell_ru_ru) | **<span class="tcblue">PostgreSQL</span>** | **<span class="tcwarn">PIGSTY</span>** | **<span class="tcwarn">PIGSTY</span>** | [LINK](https://github.com/postgrespro/hunspell_dicts) |  |  | <span class="tcwarn">✘</span> | <span class="tcblue">✔</span> | Russian Hunspell Dictionary |
| 2179 | [hunspell_ru_ru_aot](/hunspell_ru_ru_aot) | 1.0 | [hunspell_ru_ru_aot](/hunspell_ru_ru_aot) | **<span class="tcblue">PostgreSQL</span>** | **<span class="tcwarn">PIGSTY</span>** | **<span class="tcwarn">PIGSTY</span>** | [LINK](https://github.com/postgrespro/hunspell_dicts) |  |  | <span class="tcwarn">✘</span> | <span class="tcblue">✔</span> | Russian Hunspell Dictionary (from AOT.ru group) |
| 2180 | [fuzzystrmatch](/fuzzystrmatch) | 1.2 | [fuzzystrmatch](/fuzzystrmatch) | **<span class="tcblue">PostgreSQL</span>** | **<span class="tcblue">CONTRIB</span>** | **<span class="tcblue">CONTRIB</span>** | [LINK](https://www.postgresql.org/docs/current/fuzzystrmatch.html) |  |  | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | determine similarities and distance between strings |
| 2190 | [pg_trgm](/pg_trgm) | 1.6 | [pg_trgm](/pg_trgm) | **<span class="tcblue">PostgreSQL</span>** | **<span class="tcblue">CONTRIB</span>** | **<span class="tcblue">CONTRIB</span>** | [LINK](https://www.postgresql.org/docs/current/pgtrgm.html) |  |  | <span class="tcblue">✔</span> | <span class="tcblue">✔</span> | text similarity measurement and index searching based on trigrams |



### RHEL 8 Compatible (el8)

```yaml
pg17: pg_search pgroonga pg_bigm zhparser pg_bestmatch vchord_bm25 pg_tokenizer hunspell
pg16: pg_search pgroonga pg_bigm zhparser pg_bestmatch vchord_bm25 pg_tokenizer hunspell
pg15: pg_search pgroonga pg_bigm zhparser pg_bestmatch vchord_bm25 pg_tokenizer hunspell
pg14: pg_search pgroonga pg_bigm zhparser pg_bestmatch vchord_bm25 pg_tokenizer hunspell
pg13: pgroonga pg_bigm zhparser pg_bestmatch hunspell #pg_search #vchord_bm25 #pg_tokenizer
```


### RHEL 9 Compatible (el9)

```yaml
pg17: pg_search pgroonga pg_bigm zhparser pg_bestmatch vchord_bm25 pg_tokenizer hunspell
pg16: pg_search pgroonga pg_bigm zhparser pg_bestmatch vchord_bm25 pg_tokenizer hunspell
pg15: pg_search pgroonga pg_bigm zhparser pg_bestmatch vchord_bm25 pg_tokenizer hunspell
pg14: pg_search pgroonga pg_bigm zhparser pg_bestmatch vchord_bm25 pg_tokenizer hunspell
pg13: pgroonga pg_bigm zhparser pg_bestmatch hunspell #pg_search #vchord_bm25 #pg_tokenizer
```


### Debian 12 bookworm Compatible (d12)

```yaml
pg17: pg_search pgroonga pg_bigm zhparser pg_bestmatch vchord_bm25 pg_tokenizer hunspell
pg16: pg_search pgroonga pg_bigm zhparser pg_bestmatch vchord_bm25 pg_tokenizer hunspell
pg15: pg_search pgroonga pg_bigm zhparser pg_bestmatch vchord_bm25 pg_tokenizer hunspell
pg14: pg_search pgroonga pg_bigm zhparser pg_bestmatch vchord_bm25 pg_tokenizer hunspell
pg13: pgroonga pg_bigm zhparser pg_bestmatch hunspell #pg_search #vchord_bm25 #pg_tokenizer
```


### Ubuntu 24.04 jammy Compatible (u22)

```yaml
pg17: pg_search pgroonga pg_bigm zhparser pg_bestmatch vchord_bm25 pg_tokenizer hunspell
pg16: pg_search pgroonga pg_bigm zhparser pg_bestmatch vchord_bm25 pg_tokenizer hunspell
pg15: pg_search pgroonga pg_bigm zhparser pg_bestmatch vchord_bm25 pg_tokenizer hunspell
pg14: pg_search pgroonga pg_bigm zhparser pg_bestmatch vchord_bm25 pg_tokenizer hunspell
pg13: pgroonga pg_bigm zhparser pg_bestmatch hunspell #pg_search #vchord_bm25 #pg_tokenizer
```


### Ubuntu 24.04 noble Compatible (u24)

```yaml
pg17: pg_search pgroonga pg_bigm zhparser pg_bestmatch vchord_bm25 pg_tokenizer hunspell
pg16: pg_search pgroonga pg_bigm zhparser pg_bestmatch vchord_bm25 pg_tokenizer hunspell
pg15: pg_search pgroonga pg_bigm zhparser pg_bestmatch vchord_bm25 pg_tokenizer hunspell
pg14: pg_search pgroonga pg_bigm zhparser pg_bestmatch vchord_bm25 pg_tokenizer hunspell
pg13: pgroonga pg_bigm zhparser pg_bestmatch hunspell #pg_search #vchord_bm25 #pg_tokenizer
```



--------

## RPM Packages


| Package | Version | License | RPM | RPM Package | 17 | 16 | 15 | 14 | 13 | Description |
|---------|---------|:-------:|:---:|-------------|:--:|:--:|:--:|:--:|:--:|-------------|
| [pg_search](/pg_search) | 0.15.18 | **<span class="tcwarn">AGPLv3</span>** | **<span class="tcwarn">PIGSTY</span>** | `pg_search_$v` | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** |  | Full text search for PostgreSQL using BM25 |
| [pgroonga](/pgroonga) | 4.0.0 | **<span class="tcblue">PostgreSQL</span>** | **<span class="tcwarn">PIGSTY</span>** | `pgroonga_$v*` | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | Use Groonga as index, fast full text search platform for all languages! |
| [pg_bigm](/pg_bigm) | 1.2 | **<span class="tcblue">PostgreSQL</span>** | **<span class="tccyan">PGDG</span>** | `pg_bigm_$v*` | **<span class="tccyan">✔</span>** | **<span class="tccyan">✔</span>** | **<span class="tccyan">✔</span>** | **<span class="tccyan">✔</span>** | **<span class="tccyan">✔</span>** | create 2-gram (bigram) index for faster full text search. |
| [zhparser](/zhparser) | 2.3 | **<span class="tcblue">PostgreSQL</span>** | **<span class="tcwarn">PIGSTY</span>** | `zhparser_$v*` | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | a parser for full-text search of Chinese |
| [pg_bestmatch](/pg_bestmatch) | 0.0.1 | **<span class="tccyan">Apache-2</span>** | **<span class="tcwarn">PIGSTY</span>** | `pg_bestmatch_$v` | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | Generate BM25 sparse vector inside PostgreSQL |
| [vchord_bm25](/vchord_bm25) | 0.2.1 | **<span class="tcwarn">AGPLv3</span>** | **<span class="tcwarn">PIGSTY</span>** | `vchord_bm25_$v` | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** |  | A postgresql extension for bm25 ranking algorithm |
| [pg_tokenizer](/pg_tokenizer) | 0.1.0 | **<span class="tccyan">Apache-2</span>** | **<span class="tcwarn">PIGSTY</span>** | `pg_tokenizer_$v` | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** |  | Tokenizers for full-text search |
| [hunspell_cs_cz](/hunspell_cs_cz) | 1.0 | **<span class="tcblue">PostgreSQL</span>** | **<span class="tcwarn">PIGSTY</span>** | `hunspell_cs_cz_$v` | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | Czech Hunspell Dictionary |
| [hunspell_de_de](/hunspell_de_de) | 1.0 | **<span class="tcblue">PostgreSQL</span>** | **<span class="tcwarn">PIGSTY</span>** | `hunspell_de_de_$v` | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | German Hunspell Dictionary |
| [hunspell_en_us](/hunspell_en_us) | 1.0 | **<span class="tcblue">PostgreSQL</span>** | **<span class="tcwarn">PIGSTY</span>** | `hunspell_en_us_$v` | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | en_US Hunspell Dictionary |
| [hunspell_fr](/hunspell_fr) | 1.0 | **<span class="tcblue">PostgreSQL</span>** | **<span class="tcwarn">PIGSTY</span>** | `hunspell_fr_$v` | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | French Hunspell Dictionary |
| [hunspell_ne_np](/hunspell_ne_np) | 1.0 | **<span class="tcblue">PostgreSQL</span>** | **<span class="tcwarn">PIGSTY</span>** | `hunspell_ne_np_$v` | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | Nepali Hunspell Dictionary |
| [hunspell_nl_nl](/hunspell_nl_nl) | 1.0 | **<span class="tcblue">PostgreSQL</span>** | **<span class="tcwarn">PIGSTY</span>** | `hunspell_nl_nl_$v` | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | Dutch Hunspell Dictionary |
| [hunspell_nn_no](/hunspell_nn_no) | 1.0 | **<span class="tcblue">PostgreSQL</span>** | **<span class="tcwarn">PIGSTY</span>** | `hunspell_nn_no_$v` | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | Norwegian (norsk) Hunspell Dictionary |
| [hunspell_pt_pt](/hunspell_pt_pt) | 1.0 | **<span class="tcblue">PostgreSQL</span>** | **<span class="tcwarn">PIGSTY</span>** | `hunspell_pt_pt_$v` | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | Portuguese Hunspell Dictionary |
| [hunspell_ru_ru](/hunspell_ru_ru) | 1.0 | **<span class="tcblue">PostgreSQL</span>** | **<span class="tcwarn">PIGSTY</span>** | `hunspell_ru_ru_$v` | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | Russian Hunspell Dictionary |
| [hunspell_ru_ru_aot](/hunspell_ru_ru_aot) | 1.0 | **<span class="tcblue">PostgreSQL</span>** | **<span class="tcwarn">PIGSTY</span>** | `hunspell_ru_ru_aot_$v` | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | Russian Hunspell Dictionary (from AOT.ru group) |
| [fuzzystrmatch](/fuzzystrmatch) | 1.2 | **<span class="tcblue">PostgreSQL</span>** | **<span class="tcblue">CONTRIB</span>** | `postgresql$v-contrib` | **<span class="tcblue">✔</span>** | **<span class="tcblue">✔</span>** | **<span class="tcblue">✔</span>** | **<span class="tcblue">✔</span>** | **<span class="tcblue">✔</span>** | determine similarities and distance between strings |
| [pg_trgm](/pg_trgm) | 1.6 | **<span class="tcblue">PostgreSQL</span>** | **<span class="tcblue">CONTRIB</span>** | `postgresql$v-contrib` | **<span class="tcblue">✔</span>** | **<span class="tcblue">✔</span>** | **<span class="tcblue">✔</span>** | **<span class="tcblue">✔</span>** | **<span class="tcblue">✔</span>** | text similarity measurement and index searching based on trigrams |



### RHEL 8 Compatible (el8)

```yaml
pg17: pg_search_17 pgroonga_17* pg_bigm_17* zhparser_17* pg_bestmatch_17 vchord_bm25_17 pg_tokenizer_17 hunspell_cs_cz_17 hunspell_de_de_17 hunspell_en_us_17 hunspell_fr_17 hunspell_ne_np_17 hunspell_nl_nl_17 hunspell_nn_no_17 hunspell_pt_pt_17 hunspell_ru_ru_17 hunspell_ru_ru_aot_17
pg16: pg_search_16 pgroonga_16* pg_bigm_16* zhparser_16* pg_bestmatch_16 vchord_bm25_16 pg_tokenizer_16 hunspell_cs_cz_16 hunspell_de_de_16 hunspell_en_us_16 hunspell_fr_16 hunspell_ne_np_16 hunspell_nl_nl_16 hunspell_nn_no_16 hunspell_pt_pt_16 hunspell_ru_ru_16 hunspell_ru_ru_aot_16
pg15: pg_search_15 pgroonga_15* pg_bigm_15* zhparser_15* pg_bestmatch_15 vchord_bm25_15 pg_tokenizer_15 hunspell_cs_cz_15 hunspell_de_de_15 hunspell_en_us_15 hunspell_fr_15 hunspell_ne_np_15 hunspell_nl_nl_15 hunspell_nn_no_15 hunspell_pt_pt_15 hunspell_ru_ru_15 hunspell_ru_ru_aot_15
pg14: pg_search_14 pgroonga_14* pg_bigm_14* zhparser_14* pg_bestmatch_14 vchord_bm25_14 pg_tokenizer_14 hunspell_cs_cz_14 hunspell_de_de_14 hunspell_en_us_14 hunspell_fr_14 hunspell_ne_np_14 hunspell_nl_nl_14 hunspell_nn_no_14 hunspell_pt_pt_14 hunspell_ru_ru_14 hunspell_ru_ru_aot_14
pg13: pgroonga_13* pg_bigm_13* zhparser_13* pg_bestmatch_13 hunspell_cs_cz_13 hunspell_de_de_13 hunspell_en_us_13 hunspell_fr_13 hunspell_ne_np_13 hunspell_nl_nl_13 hunspell_nn_no_13 hunspell_pt_pt_13 hunspell_ru_ru_13 hunspell_ru_ru_aot_13 #pg_search_13 #vchord_bm25_13 #pg_tokenizer_13
```


### RHEL 9 Compatible (el9)

```yaml
pg17: pg_search_17 pgroonga_17* pg_bigm_17* zhparser_17* pg_bestmatch_17 vchord_bm25_17 pg_tokenizer_17 hunspell_cs_cz_17 hunspell_de_de_17 hunspell_en_us_17 hunspell_fr_17 hunspell_ne_np_17 hunspell_nl_nl_17 hunspell_nn_no_17 hunspell_pt_pt_17 hunspell_ru_ru_17 hunspell_ru_ru_aot_17
pg16: pg_search_16 pgroonga_16* pg_bigm_16* zhparser_16* pg_bestmatch_16 vchord_bm25_16 pg_tokenizer_16 hunspell_cs_cz_16 hunspell_de_de_16 hunspell_en_us_16 hunspell_fr_16 hunspell_ne_np_16 hunspell_nl_nl_16 hunspell_nn_no_16 hunspell_pt_pt_16 hunspell_ru_ru_16 hunspell_ru_ru_aot_16
pg15: pg_search_15 pgroonga_15* pg_bigm_15* zhparser_15* pg_bestmatch_15 vchord_bm25_15 pg_tokenizer_15 hunspell_cs_cz_15 hunspell_de_de_15 hunspell_en_us_15 hunspell_fr_15 hunspell_ne_np_15 hunspell_nl_nl_15 hunspell_nn_no_15 hunspell_pt_pt_15 hunspell_ru_ru_15 hunspell_ru_ru_aot_15
pg14: pg_search_14 pgroonga_14* pg_bigm_14* zhparser_14* pg_bestmatch_14 vchord_bm25_14 pg_tokenizer_14 hunspell_cs_cz_14 hunspell_de_de_14 hunspell_en_us_14 hunspell_fr_14 hunspell_ne_np_14 hunspell_nl_nl_14 hunspell_nn_no_14 hunspell_pt_pt_14 hunspell_ru_ru_14 hunspell_ru_ru_aot_14
pg13: pgroonga_13* pg_bigm_13* zhparser_13* pg_bestmatch_13 hunspell_cs_cz_13 hunspell_de_de_13 hunspell_en_us_13 hunspell_fr_13 hunspell_ne_np_13 hunspell_nl_nl_13 hunspell_nn_no_13 hunspell_pt_pt_13 hunspell_ru_ru_13 hunspell_ru_ru_aot_13 #pg_search_13 #vchord_bm25_13 #pg_tokenizer_13
```



--------

## DEB Packages


| Package | Version | License | DEB | DEB Package | 17 | 16 | 15 | 14 | 13 | Description |
|---------|---------|:-------:|:---:|-------------|:--:|:--:|:--:|:--:|:--:|-------------|
| [pg_search](/pg_search) | 0.16.2 | **<span class="tcwarn">AGPLv3</span>** | **<span class="tcwarn">PIGSTY</span>** | `postgresql-$v-pg-search` | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** |  | Full text search for PostgreSQL using BM25 |
| [pgroonga](/pgroonga) | 4.0.0 | **<span class="tcblue">PostgreSQL</span>** | **<span class="tcwarn">PIGSTY</span>** | `postgresql-$v-pgroonga` | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | Use Groonga as index, fast full text search platform for all languages! |
| [pg_bigm](/pg_bigm) | 1.2 | **<span class="tcblue">PostgreSQL</span>** | **<span class="tcwarn">PIGSTY</span>** | `postgresql-$v-pg-bigm` | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | create 2-gram (bigram) index for faster full text search. |
| [zhparser](/zhparser) | 2.3 | **<span class="tcblue">PostgreSQL</span>** | **<span class="tcwarn">PIGSTY</span>** | `postgresql-$v-zhparser` | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | a parser for full-text search of Chinese |
| [pg_bestmatch](/pg_bestmatch) | 0.0.1 | **<span class="tccyan">Apache-2</span>** | **<span class="tcwarn">PIGSTY</span>** | `postgresql-$v-pg-bestmatch` | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | Generate BM25 sparse vector inside PostgreSQL |
| [vchord_bm25](/vchord_bm25) | 0.2.1 | **<span class="tcwarn">AGPLv3</span>** | **<span class="tcwarn">PIGSTY</span>** | `postgresql-$v-vchord-bm25` | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** |  | A postgresql extension for bm25 ranking algorithm |
| [pg_tokenizer](/pg_tokenizer) | 0.1.0 | **<span class="tccyan">Apache-2</span>** | **<span class="tcwarn">PIGSTY</span>** | `postgresql-$v-pg-tokenizer` | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** |  | Tokenizers for full-text search |
| [hunspell_cs_cz](/hunspell_cs_cz) | 1.0 | **<span class="tcblue">PostgreSQL</span>** | **<span class="tcwarn">PIGSTY</span>** | `postgresql-$v-hunspell-cs-cz` | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | Czech Hunspell Dictionary |
| [hunspell_de_de](/hunspell_de_de) | 1.0 | **<span class="tcblue">PostgreSQL</span>** | **<span class="tcwarn">PIGSTY</span>** | `postgresql-$v-hunspell-de-de` | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | German Hunspell Dictionary |
| [hunspell_en_us](/hunspell_en_us) | 1.0 | **<span class="tcblue">PostgreSQL</span>** | **<span class="tcwarn">PIGSTY</span>** | `postgresql-$v-hunspell-en-us` | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | en_US Hunspell Dictionary |
| [hunspell_fr](/hunspell_fr) | 1.0 | **<span class="tcblue">PostgreSQL</span>** | **<span class="tcwarn">PIGSTY</span>** | `postgresql-$v-hunspell-fr` | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | French Hunspell Dictionary |
| [hunspell_ne_np](/hunspell_ne_np) | 1.0 | **<span class="tcblue">PostgreSQL</span>** | **<span class="tcwarn">PIGSTY</span>** | `postgresql-$v-hunspell-ne-np` | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | Nepali Hunspell Dictionary |
| [hunspell_nl_nl](/hunspell_nl_nl) | 1.0 | **<span class="tcblue">PostgreSQL</span>** | **<span class="tcwarn">PIGSTY</span>** | `postgresql-$v-hunspell-nl-nl` | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | Dutch Hunspell Dictionary |
| [hunspell_nn_no](/hunspell_nn_no) | 1.0 | **<span class="tcblue">PostgreSQL</span>** | **<span class="tcwarn">PIGSTY</span>** | `postgresql-$v-hunspell-nn-no` | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | Norwegian (norsk) Hunspell Dictionary |
| [hunspell_pt_pt](/hunspell_pt_pt) | 1.0 | **<span class="tcblue">PostgreSQL</span>** | **<span class="tcwarn">PIGSTY</span>** | `postgresql-$v-hunspell-pt-pt` | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | Portuguese Hunspell Dictionary |
| [hunspell_ru_ru](/hunspell_ru_ru) | 1.0 | **<span class="tcblue">PostgreSQL</span>** | **<span class="tcwarn">PIGSTY</span>** | `postgresql-$v-hunspell-ru-ru` | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | Russian Hunspell Dictionary |
| [hunspell_ru_ru_aot](/hunspell_ru_ru_aot) | 1.0 | **<span class="tcblue">PostgreSQL</span>** | **<span class="tcwarn">PIGSTY</span>** | `postgresql-$v-hunspell-ru-ru-aot` | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | **<span class="tcwarn">✔</span>** | Russian Hunspell Dictionary (from AOT.ru group) |
| [fuzzystrmatch](/fuzzystrmatch) | 1.2 | **<span class="tcblue">PostgreSQL</span>** | **<span class="tcblue">CONTRIB</span>** | `postgresql-$v` | **<span class="tcblue">✔</span>** | **<span class="tcblue">✔</span>** | **<span class="tcblue">✔</span>** | **<span class="tcblue">✔</span>** | **<span class="tcblue">✔</span>** | determine similarities and distance between strings |
| [pg_trgm](/pg_trgm) | 1.6 | **<span class="tcblue">PostgreSQL</span>** | **<span class="tcblue">CONTRIB</span>** | `postgresql-$v` | **<span class="tcblue">✔</span>** | **<span class="tcblue">✔</span>** | **<span class="tcblue">✔</span>** | **<span class="tcblue">✔</span>** | **<span class="tcblue">✔</span>** | text similarity measurement and index searching based on trigrams |



### Debian 12 bookworm Compatible (d12)

```yaml
pg17: postgresql-17-pg-search postgresql-17-pgroonga postgresql-17-pg-bigm postgresql-17-zhparser postgresql-17-pg-bestmatch postgresql-17-vchord-bm25 postgresql-17-pg-tokenizer postgresql-17-hunspell-cs-cz postgresql-17-hunspell-de-de postgresql-17-hunspell-en-us postgresql-17-hunspell-fr postgresql-17-hunspell-ne-np postgresql-17-hunspell-nl-nl postgresql-17-hunspell-nn-no postgresql-17-hunspell-pt-pt postgresql-17-hunspell-ru-ru postgresql-17-hunspell-ru-ru-aot
pg16: postgresql-16-pg-search postgresql-16-pgroonga postgresql-16-pg-bigm postgresql-16-zhparser postgresql-16-pg-bestmatch postgresql-16-vchord-bm25 postgresql-16-pg-tokenizer postgresql-16-hunspell-cs-cz postgresql-16-hunspell-de-de postgresql-16-hunspell-en-us postgresql-16-hunspell-fr postgresql-16-hunspell-ne-np postgresql-16-hunspell-nl-nl postgresql-16-hunspell-nn-no postgresql-16-hunspell-pt-pt postgresql-16-hunspell-ru-ru postgresql-16-hunspell-ru-ru-aot
pg15: postgresql-15-pg-search postgresql-15-pgroonga postgresql-15-pg-bigm postgresql-15-zhparser postgresql-15-pg-bestmatch postgresql-15-vchord-bm25 postgresql-15-pg-tokenizer postgresql-15-hunspell-cs-cz postgresql-15-hunspell-de-de postgresql-15-hunspell-en-us postgresql-15-hunspell-fr postgresql-15-hunspell-ne-np postgresql-15-hunspell-nl-nl postgresql-15-hunspell-nn-no postgresql-15-hunspell-pt-pt postgresql-15-hunspell-ru-ru postgresql-15-hunspell-ru-ru-aot
pg14: postgresql-14-pg-search postgresql-14-pgroonga postgresql-14-pg-bigm postgresql-14-zhparser postgresql-14-pg-bestmatch postgresql-14-vchord-bm25 postgresql-14-pg-tokenizer postgresql-14-hunspell-cs-cz postgresql-14-hunspell-de-de postgresql-14-hunspell-en-us postgresql-14-hunspell-fr postgresql-14-hunspell-ne-np postgresql-14-hunspell-nl-nl postgresql-14-hunspell-nn-no postgresql-14-hunspell-pt-pt postgresql-14-hunspell-ru-ru postgresql-14-hunspell-ru-ru-aot
pg13: postgresql-13-pgroonga postgresql-13-pg-bigm postgresql-13-zhparser postgresql-13-pg-bestmatch postgresql-13-hunspell-cs-cz postgresql-13-hunspell-de-de postgresql-13-hunspell-en-us postgresql-13-hunspell-fr postgresql-13-hunspell-ne-np postgresql-13-hunspell-nl-nl postgresql-13-hunspell-nn-no postgresql-13-hunspell-pt-pt postgresql-13-hunspell-ru-ru postgresql-13-hunspell-ru-ru-aot #postgresql-13-pg-search #postgresql-13-vchord-bm25 #postgresql-13-pg-tokenizer
```


### Ubuntu 24.04 jammy Compatible (u22)

```yaml
pg17: postgresql-17-pg-search postgresql-17-pgroonga postgresql-17-pg-bigm postgresql-17-zhparser postgresql-17-pg-bestmatch postgresql-17-vchord-bm25 postgresql-17-pg-tokenizer postgresql-17-hunspell-cs-cz postgresql-17-hunspell-de-de postgresql-17-hunspell-en-us postgresql-17-hunspell-fr postgresql-17-hunspell-ne-np postgresql-17-hunspell-nl-nl postgresql-17-hunspell-nn-no postgresql-17-hunspell-pt-pt postgresql-17-hunspell-ru-ru postgresql-17-hunspell-ru-ru-aot
pg16: postgresql-16-pg-search postgresql-16-pgroonga postgresql-16-pg-bigm postgresql-16-zhparser postgresql-16-pg-bestmatch postgresql-16-vchord-bm25 postgresql-16-pg-tokenizer postgresql-16-hunspell-cs-cz postgresql-16-hunspell-de-de postgresql-16-hunspell-en-us postgresql-16-hunspell-fr postgresql-16-hunspell-ne-np postgresql-16-hunspell-nl-nl postgresql-16-hunspell-nn-no postgresql-16-hunspell-pt-pt postgresql-16-hunspell-ru-ru postgresql-16-hunspell-ru-ru-aot
pg15: postgresql-15-pg-search postgresql-15-pgroonga postgresql-15-pg-bigm postgresql-15-zhparser postgresql-15-pg-bestmatch postgresql-15-vchord-bm25 postgresql-15-pg-tokenizer postgresql-15-hunspell-cs-cz postgresql-15-hunspell-de-de postgresql-15-hunspell-en-us postgresql-15-hunspell-fr postgresql-15-hunspell-ne-np postgresql-15-hunspell-nl-nl postgresql-15-hunspell-nn-no postgresql-15-hunspell-pt-pt postgresql-15-hunspell-ru-ru postgresql-15-hunspell-ru-ru-aot
pg14: postgresql-14-pg-search postgresql-14-pgroonga postgresql-14-pg-bigm postgresql-14-zhparser postgresql-14-pg-bestmatch postgresql-14-vchord-bm25 postgresql-14-pg-tokenizer postgresql-14-hunspell-cs-cz postgresql-14-hunspell-de-de postgresql-14-hunspell-en-us postgresql-14-hunspell-fr postgresql-14-hunspell-ne-np postgresql-14-hunspell-nl-nl postgresql-14-hunspell-nn-no postgresql-14-hunspell-pt-pt postgresql-14-hunspell-ru-ru postgresql-14-hunspell-ru-ru-aot
pg13: postgresql-13-pgroonga postgresql-13-pg-bigm postgresql-13-zhparser postgresql-13-pg-bestmatch postgresql-13-hunspell-cs-cz postgresql-13-hunspell-de-de postgresql-13-hunspell-en-us postgresql-13-hunspell-fr postgresql-13-hunspell-ne-np postgresql-13-hunspell-nl-nl postgresql-13-hunspell-nn-no postgresql-13-hunspell-pt-pt postgresql-13-hunspell-ru-ru postgresql-13-hunspell-ru-ru-aot #postgresql-13-pg-search #postgresql-13-vchord-bm25 #postgresql-13-pg-tokenizer
```


### Ubuntu 24.04 noble Compatible (u24)

```yaml
pg17: postgresql-17-pg-search postgresql-17-pgroonga postgresql-17-pg-bigm postgresql-17-zhparser postgresql-17-pg-bestmatch postgresql-17-vchord-bm25 postgresql-17-pg-tokenizer postgresql-17-hunspell-cs-cz postgresql-17-hunspell-de-de postgresql-17-hunspell-en-us postgresql-17-hunspell-fr postgresql-17-hunspell-ne-np postgresql-17-hunspell-nl-nl postgresql-17-hunspell-nn-no postgresql-17-hunspell-pt-pt postgresql-17-hunspell-ru-ru postgresql-17-hunspell-ru-ru-aot
pg16: postgresql-16-pg-search postgresql-16-pgroonga postgresql-16-pg-bigm postgresql-16-zhparser postgresql-16-pg-bestmatch postgresql-16-vchord-bm25 postgresql-16-pg-tokenizer postgresql-16-hunspell-cs-cz postgresql-16-hunspell-de-de postgresql-16-hunspell-en-us postgresql-16-hunspell-fr postgresql-16-hunspell-ne-np postgresql-16-hunspell-nl-nl postgresql-16-hunspell-nn-no postgresql-16-hunspell-pt-pt postgresql-16-hunspell-ru-ru postgresql-16-hunspell-ru-ru-aot
pg15: postgresql-15-pg-search postgresql-15-pgroonga postgresql-15-pg-bigm postgresql-15-zhparser postgresql-15-pg-bestmatch postgresql-15-vchord-bm25 postgresql-15-pg-tokenizer postgresql-15-hunspell-cs-cz postgresql-15-hunspell-de-de postgresql-15-hunspell-en-us postgresql-15-hunspell-fr postgresql-15-hunspell-ne-np postgresql-15-hunspell-nl-nl postgresql-15-hunspell-nn-no postgresql-15-hunspell-pt-pt postgresql-15-hunspell-ru-ru postgresql-15-hunspell-ru-ru-aot
pg14: postgresql-14-pg-search postgresql-14-pgroonga postgresql-14-pg-bigm postgresql-14-zhparser postgresql-14-pg-bestmatch postgresql-14-vchord-bm25 postgresql-14-pg-tokenizer postgresql-14-hunspell-cs-cz postgresql-14-hunspell-de-de postgresql-14-hunspell-en-us postgresql-14-hunspell-fr postgresql-14-hunspell-ne-np postgresql-14-hunspell-nl-nl postgresql-14-hunspell-nn-no postgresql-14-hunspell-pt-pt postgresql-14-hunspell-ru-ru postgresql-14-hunspell-ru-ru-aot
pg13: postgresql-13-pgroonga postgresql-13-pg-bigm postgresql-13-zhparser postgresql-13-pg-bestmatch postgresql-13-hunspell-cs-cz postgresql-13-hunspell-de-de postgresql-13-hunspell-en-us postgresql-13-hunspell-fr postgresql-13-hunspell-ne-np postgresql-13-hunspell-nl-nl postgresql-13-hunspell-nn-no postgresql-13-hunspell-pt-pt postgresql-13-hunspell-ru-ru postgresql-13-hunspell-ru-ru-aot #postgresql-13-pg-search #postgresql-13-vchord-bm25 #postgresql-13-pg-tokenizer
```



--------
