-----------------------------------
-- Schema: ext
-----------------------------------
CREATE SCHEMA IF NOT EXISTS ext;

-----------------------------------
-- Extension Category
-----------------------------------
CREATE TABLE IF NOT EXISTS ext.cate (
    id      INTEGER PRIMARY KEY,
    name    TEXT UNIQUE,
    icon    TEXT,
    zh_desc TEXT,
    en_desc TEXT
);

-- COPY ext.cate FROM '/Users/vonng/pgsty/extension/data/cate.csv' CSV HEADER;
-- cat data/cate.csv | psql service=sty -c 'COPY ext.cate FROM STDIN CSV HEADER'


-----------------------------------
-- Repo
-----------------------------------
DROP TABLE IF EXISTS ext.repo;
CREATE TABLE IF NOT EXISTS ext.repo
(
    id           TEXT,
    os           TEXT, -- u22.arm, el7.amd
    org          TEXT, -- pgdg, pigsty, ...
    type         TEXT, -- rpm / deb
    os_code      TEXT, -- u22, el7
    os_arch      text, -- x86_64, aarch64
    default_url  text, -- default pgdg/io url
    default_meta text, -- where to get default meta
    mirror_url   text, -- china mirror cc base url
    mirror_meta  text, -- where to get mirror meta
    extra        jsonb,
    comment      text,
    primary key (id)
);

COMMENT ON TABLE ext.repo IS 'PostgreSQL Extension Repo';
COMMENT ON COLUMN ext.repo.id IS 'format as os_code.os_arch.org, such as d12.arm.pigsty';
COMMENT ON COLUMN ext.repo.os IS 'os_code.arch, such as u22.arm, el7.amd';
COMMENT ON COLUMN ext.repo.org IS 'repo upstream, pgdg, pigsty';
COMMENT ON COLUMN ext.repo.type IS 'rpm or deb';
COMMENT ON COLUMN ext.repo.os_code IS '3 char os code, like u24, el7, el8';
COMMENT ON COLUMN ext.repo.os_arch IS 'amd or arm';
COMMENT ON COLUMN ext.repo.default_url IS 'default base url of this repo (base of href)';
COMMENT ON COLUMN ext.repo.default_meta IS 'metadata url, global default';
COMMENT ON COLUMN ext.repo.mirror_url IS 'china mirror base url of this repo';
COMMENT ON COLUMN ext.repo.mirror_meta IS 'metadata url, china mirror';
COMMENT ON COLUMN ext.repo.extra IS 'extra metadata';
COMMENT ON COLUMN ext.repo.comment IS 'extra description';

-- COPY pgext.repo TO '/Users/vonng/pgsty/extension/data/repo.csv' CSV HEADER;
-- TRUNCATE ext.repo CASCADE; COPY ext.repo FROM '/Users/vonng/pgsty/extension/data/repo.csv' CSV HEADER;
-- cat data/repo.csv | psql service=sty -c 'COPY ext.repo FROM STDIN CSV HEADER'



-----------------------------------
-- Extension
-----------------------------------
DROP TABLE IF EXISTS ext.extension CASCADE;
CREATE TABLE IF NOT EXISTS ext.extension
(
    id          INTEGER PRIMARY KEY,
    name        TEXT NOT NULL,
    pkg         TEXT NOT NULL,
    alias       TEXT,
    category    TEXT,
    state       TEXT,
    url         TEXT,
    license     TEXT,
    tags        TEXT[],
    version     TEXT,
    repo        TEXT,
    lang        TEXT,
    contrib     BOOLEAN,
    lead        BOOLEAN,
    has_bin     BOOLEAN,
    has_lib     BOOLEAN,
    need_ddl    BOOLEAN,
    need_load   BOOLEAN,
    trusted     BOOLEAN,
    relocatable BOOLEAN,
    schemas     TEXT[],
    pg_ver      TEXT[],
    requires    TEXT[],
    rpm_ver     TEXT,
    rpm_repo    TEXT,
    rpm_pkg     TEXT,
    rpm_pg      TEXT[],
    rpm_deps    TEXT[],
    deb_ver     TEXT,
    deb_repo    TEXT,
    deb_pkg     TEXT,
    deb_deps    TEXT[],
    deb_pg      TEXT[],
    bad_case    TEXT[],
    extra       JSONB,
    ctime       DATE DEFAULT CURRENT_DATE,
    mtime       DATE DEFAULT CURRENT_DATE,
    en_desc     TEXT,
    zh_desc     TEXT,
    comment     TEXT
);

CREATE INDEX IF NOT EXISTS ext_name_pkg_idx ON ext.extension (name,pkg);

COMMENT ON TABLE ext.extension IS 'PostgreSQL Extension Table';
COMMENT ON COLUMN ext.extension.id IS 'Extension Identifier (integer)';
COMMENT ON COLUMN ext.extension.name IS 'Extension Name (in system catalog)';
COMMENT ON COLUMN ext.extension.pkg IS 'Normalized extension package name';
COMMENT ON COLUMN ext.extension.alias IS 'Download pkg group alias';
COMMENT ON COLUMN ext.extension.category IS 'Category of this extension';
COMMENT ON COLUMN ext.extension.state IS 'Extension State (available, deprecated, removed, not-ready)';
COMMENT ON COLUMN ext.extension.url IS 'Extension Repo URL';
COMMENT ON COLUMN ext.extension.license IS 'Extension License';
COMMENT ON COLUMN ext.extension.tags IS 'Extra tags';
COMMENT ON COLUMN ext.extension.version IS 'the latest available version of this extension';
COMMENT ON COLUMN ext.extension.lang IS 'Programming Language of this extension';
COMMENT ON COLUMN ext.extension.lead IS 'Mark the primary extension among one multi-ext package';
COMMENT ON COLUMN ext.extension.has_bin IS 'does this extension has binary utils';
COMMENT ON COLUMN ext.extension.has_lib IS 'Does the extension have shared library?';
COMMENT ON COLUMN ext.extension.need_ddl IS 'Extension need `CREATE EXTENSION` to work?';
COMMENT ON COLUMN ext.extension.need_load IS 'Require LOAD & shared_preload_libraries to work?';
COMMENT ON COLUMN ext.extension.trusted IS 'A Trusted extension does not require superuser to work';
COMMENT ON COLUMN ext.extension.relocatable IS 'Can this extension be relocated?';
COMMENT ON COLUMN ext.extension.schemas IS 'Installed Schema, if not relocatable';
COMMENT ON COLUMN ext.extension.pg_ver IS 'Supported PostgreSQL major versions';
COMMENT ON COLUMN ext.extension.requires IS 'Dependencies of this extension';
COMMENT ON COLUMN ext.extension.rpm_pkg IS 'RPM package name, major version is replace with $v';
COMMENT ON COLUMN ext.extension.deb_pkg IS 'DEB package name, major version is replace with $v';
COMMENT ON COLUMN ext.extension.en_desc IS 'English description';
COMMENT ON COLUMN ext.extension.zh_desc IS 'Chinese description';
COMMENT ON COLUMN ext.extension.comment IS 'Extra information';

-- COPY (SELECT * FROM ext.extension ORDER BY id) TO '/Users/vonng/pgsty/extension/data/extension.csv' CSV HEADER;
-- TRUNCATE ext.extension; COPY ext.extension FROM '/Users/vonng/pgsty/extension/data/extension.csv' CSV HEADER;
-- cat data/extension.csv | psql service=sty -c 'COPY ext.extension FROM STDIN CSV HEADER'


-----------------------------------
-- Extension Legacy
-----------------------------------
DROP VIEW IF EXISTS ext.pigsty;
CREATE OR REPLACE VIEW ext.pigsty AS
    SELECT id,name,pkg AS alias,category,url,license,tags,version,repo,lang,has_bin AS utility,lead,has_lib AS has_solib,need_ddl,need_load,trusted,relocatable,
           schemas,pg_ver,requires,rpm_ver,rpm_repo,rpm_pkg,rpm_pg,rpm_deps,deb_ver,deb_repo,deb_pkg,deb_deps,deb_pg,bad_case,en_desc,zh_desc,comment
    FROM ext.extension
    ORDER BY id;


-----------------------------------
-- Availability Matrix
-----------------------------------
DROP TABLE IF EXISTS ext.matrix CASCADE;
CREATE TABLE IF NOT EXISTS ext.matrix
(
    pg      INTEGER,
    os      TEXT,
    type    TEXT,
    os_code TEXT,
    os_arch TEXT,
    pkg     TEXT,
    pname   TEXT,
    count   BIGINT,
    PRIMARY KEY (pg, os, pkg)
);
CREATE INDEX IF NOT EXISTS matrix_pg_os_pname_idx ON ext.matrix(pg, os, pname);

COMMENT ON TABLE  ext.matrix IS 'PostgreSQL Extension Availbility PG & OS Matrix';
COMMENT ON COLUMN ext.matrix.pg IS 'PostgreSQL Major Version 13-17 (integer)';
COMMENT ON COLUMN ext.matrix.os IS 'os.arch identifier like el8.arm, u24.amd';
COMMENT ON COLUMN ext.matrix.type IS 'platform package type rpm or deb';
COMMENT ON COLUMN ext.matrix.os_code IS '3 char os code, like u24, el7, el8';
COMMENT ON COLUMN ext.matrix.os_arch IS 'simplified arch name: amd or arm';
COMMENT ON COLUMN ext.matrix.pkg IS 'Normalized extension package name';
COMMENT ON COLUMN ext.matrix.pname IS 'PG Major Versioned DEB/RPM Package Name';
COMMENT ON COLUMN ext.matrix.count IS 'Stat place holder counter';

TRUNCATE ext.matrix;
INSERT INTO ext.matrix
WITH packages AS (SELECT DISTINCT ON (pkg) pkg,id,name AS extname,category,state,pg_ver,replace(rpm_pkg, '*', '') AS rpm,deb_pkg AS deb FROM ext.extension WHERE NOT contrib ORDER BY pkg, lead DESC)
SELECT pg::INTEGER, os, type, os_code, os_arch, pkg, pname, 0 AS count FROM
    (
        SELECT * FROM (SELECT pkg, 'deb' AS type, pg, os, os_code, os_arch, replace((regexp_split_to_array(deb, ' '))[1], '$v', pg::text) AS pname FROM packages, unnest(ARRAY[17,16,15,14,13]) AS pg, (SELECT distinct os, type, os_code, os_arch FROM ext.repo WHERE type = 'deb' ORDER BY os) r) rp UNION ALL
        SELECT pkg, 'rpm' AS type, pg, os, os_code, os_arch, replace( (regexp_split_to_array(rpm, ' '))[1], '$v', pg::text) AS pname FROM packages, unnest(ARRAY[17,16,15,14,13]) AS pg, (SELECT distinct os, type, os_code, os_arch FROM ext.repo WHERE type = 'rpm' ORDER BY os) r
    ) d ORDER BY pg DESC, type, os;

-- hot fix for pgaudit
UPDATE ext.matrix SET pname = replace(pname, 'pgaudit', 'pgaudit' || (pg+2)::TEXT ) WHERE pkg = 'pgaudit' AND pg IN (13,14,15) AND type = 'rpm';


-----------------------------------
-- YUM Packages
-----------------------------------
DROP TABLE IF EXISTS ext.yum;
CREATE TABLE IF NOT EXISTS ext.yum
(
    repo             TEXT    NOT NULL REFERENCES ext.repo (id),
    pkg_key          INTEGER NOT NULL,
    pkg_id           TEXT    NOT NULL,
    name             TEXT    NOT NULL,
    arch             TEXT,
    version          TEXT,
    epoch            TEXT,
    release          TEXT,
    summary          TEXT,
    description      TEXT,
    url              TEXT,
    time_file        INTEGER,
    time_build       INTEGER,
    rpm_license      TEXT,
    rpm_vendor       TEXT,
    rpm_group        TEXT,
    rpm_buildhost    TEXT,
    rpm_sourcerpm    TEXT,
    rpm_header_start INTEGER,
    rpm_header_end   INTEGER,
    rpm_packager     TEXT,
    size_package     INTEGER,
    size_installed   INTEGER,
    size_archive     INTEGER,
    location_href    TEXT,
    location_base    TEXT,
    checksum_type    TEXT,
    PRIMARY KEY (repo, pkg_key)
);


-----------------------------------
-- APT Packages
-----------------------------------
DROP TABLE IF EXISTS ext.apt;
CREATE TABLE ext.apt
(
    repo         TEXT NOT NULL REFERENCES ext.repo (id),
    package      TEXT NOT NULL, -- required, Package name
    version      TEXT NOT NULL, -- required, Package version
    architecture TEXT NOT NULL, -- required, Target architecture
    size         INTEGER,       -- required, Package size in bytes
    size_install INTEGER,       -- required, Installed size in KB
    priority     TEXT,          -- required, Package priority
    section      TEXT,          -- required, Package section/category
    filename     TEXT,          -- required, Package filename
    sha256       TEXT,          -- required, SHA256 checksum
    sha1         TEXT,          -- required, SHA1 checksum
    md5sum       TEXT,          -- required, MD5 checksum
    maintainer   TEXT,          -- required, Package maintainer
    homepage     TEXT,          -- Package homepage URL
    depends      TEXT,          -- Package dependencies
    source       TEXT,          -- Source package name
    provides     TEXT,          -- Virtual packages provided
    recommends   TEXT,          -- Recommended packages
    suggests     TEXT,          -- Suggested packages
    conflicts    TEXT,          -- Conflicting packages
    breaks       TEXT,          -- Packages this breaks
    replaces     TEXT,          -- Packages this replaces
    enhances     TEXT,          -- Packages this enhances
    pre_depends  TEXT,          -- Pre-dependencies
    build_ids    TEXT,          -- Build IDs
    package_type TEXT,          -- Package type (deb, udeb, etc)
    auto_built   TEXT,          -- Auto-built package flag
    multi_arch   TEXT,          -- Multi-arch support
    description  TEXT,          -- Package description
    extra        JSONB,         -- Other fields as JSON
    PRIMARY KEY (repo, package,version,architecture)
);

CREATE OR REPLACE FUNCTION ext.normalize_version(version text) RETURNS text AS $$
DECLARE
    version_parts text[];
BEGIN
    version_parts := string_to_array(regexp_replace(version, '^1:', ''), '.');
    RETURN array_to_string(
        array[
       coalesce(version_parts[1], '0'),
       regexp_replace(coalesce(version_parts[2], '0'), '^(\d+).*', '\1'),
       regexp_replace(coalesce(version_parts[3], '0'), '^(\d+).*', '\1')
    ], '.');
END; $$ LANGUAGE plpgsql IMMUTABLE;

-----------------------------------
-- RPM/DEB Package Table
-----------------------------------
DROP TABLE IF EXISTS ext.package CASCADE;
CREATE TABLE IF NOT EXISTS ext.package
(
    pg         INTEGER,
    os         TEXT,
    pname      TEXT,
    org        TEXT,
    type       TEXT,
    os_code    TEXT,
    os_arch    TEXT,
    repo       TEXT,
    name       TEXT,
    ver        TEXT,
    version    TEXT,
    release    TEXT,
    file       TEXT,
    sha256     TEXT,
    url        TEXT,
    mirror_url TEXT,
    size       integer,
    size_full  integer
);

CREATE INDEX IF NOT EXISTS package_os_pname_idx ON ext.package USING BTREE(os,pname);


TRUNCATE ext.package;
INSERT INTO ext.package
SELECT pg, os, pname, org, type, os_code, os_arch,  repo, name, ver, version, release, file, d.sha256,url, mirror_url, size, size_full
FROM
(
        SELECT 17 as pg, r.os, substr(name, 0, position('_17' in name)+3) AS pname, r.org,r.type,r.os_code,r.os_arch,pkg_id AS sha256,
               repo, name, version || '-' || release AS ver, version, release, regexp_replace(y.location_href, '^.*/', '') AS file, format('%s/%s', r.default_url, y.location_href) AS url, format('%s/%s', r.mirror_url, y.location_href) AS mirror_url, size_package AS size, size_installed AS size_full
        FROM ext.yum y JOIN ext.repo r ON y.repo = r.id WHERE position('_17' in name) > 0
        UNION ALL
        SELECT 16 as pg, r.os, substr(name, 0, position('_16' in name)+3) AS pname, r.org,r.type,r.os_code,r.os_arch,pkg_id AS sha256,
               repo, name, version || '-' || release AS ver, version, release, regexp_replace(y.location_href, '^.*/', '') AS file, format('%s/%s', r.default_url, y.location_href) AS url, format('%s/%s', r.mirror_url, y.location_href) AS mirror_url, size_package AS size, size_installed AS size_full
        FROM ext.yum y JOIN ext.repo r ON y.repo = r.id WHERE position('_16' in name) > 0
        UNION ALL
        SELECT 15 as pg, r.os, substr(name, 0, position('_15' in name)+3) AS pname, r.org,r.type,r.os_code,r.os_arch,pkg_id AS sha256,
               repo, name, version || '-' || release AS ver, version, release, regexp_replace(y.location_href, '^.*/', '') AS file, format('%s/%s', r.default_url, y.location_href) AS url, format('%s/%s', r.mirror_url, y.location_href) AS mirror_url, size_package AS size, size_installed AS size_full
        FROM ext.yum y JOIN ext.repo r ON y.repo = r.id WHERE position('_15' in name) > 0
        UNION ALL
        SELECT 14 as pg, r.os, substr(name, 0, position('_14' in name)+3) AS pname, r.org,r.type,r.os_code,r.os_arch,pkg_id AS sha256,
               repo, name, version || '-' || release AS ver, version, release, regexp_replace(y.location_href, '^.*/', '') AS file, format('%s/%s', r.default_url, y.location_href) AS url, format('%s/%s', r.mirror_url, y.location_href) AS mirror_url, size_package AS size, size_installed AS size_full
        FROM ext.yum y JOIN ext.repo r ON y.repo = r.id WHERE position('_14' in name) > 0
        UNION ALL
        SELECT 13 as pg, r.os, substr(name, 0, position('_13' in name)+3) AS pname, r.org,r.type,r.os_code,r.os_arch,pkg_id AS sha256,
               repo, name, version || '-' || release AS ver, version, release, regexp_replace(y.location_href, '^.*/', '') AS file, format('%s/%s', r.default_url, y.location_href) AS url, format('%s/%s', r.mirror_url, y.location_href) AS mirror_url, size_package AS size, size_installed AS size_full
        FROM ext.yum y JOIN ext.repo r ON y.repo = r.id WHERE position('_13' in name) > 0
    ) d
UNION ALL
SELECT pg, os, pname, org, type, os_code, os_arch, repo, name, ver, version, release, file, sha256, url, mirror_url, size, size_full
FROM
(
    SELECT 17 AS pg, r.os, regexp_replace(regexp_replace(regexp_replace(regexp_replace(package, '-scripts$', ''), '-doc$', ''), '-dbgsym$', ''), '-pgq-node$', '-pgq') AS pname, r.org,r.type,r.os_code,r.os_arch,package as name, repo, version as ver, coalesce(((regexp_match(version, '^(.*)-([^-]+)$'))[1]),version) AS version, (regexp_match(version, '^(.*)-([^-]+)$'))[2] AS release,sha256,
        regexp_replace(a.filename, '^.*/', '') AS file, format('%s/%s', r.default_url, a.filename) AS url, format('%s/%s', r.mirror_url, a.filename) AS mirror_url, size, size_install AS size_full FROM ext.apt a JOIN ext.repo r ON a.repo = r.id WHERE position('-17' in package) > 0 UNION ALL
    SELECT 16 AS pg, r.os, regexp_replace(regexp_replace(regexp_replace(regexp_replace(package, '-scripts$', ''), '-doc$', ''), '-dbgsym$', ''), '-pgq-node$', '-pgq') AS pname, r.org,r.type,r.os_code,r.os_arch,package as name, repo, version as ver, coalesce(((regexp_match(version, '^(.*)-([^-]+)$'))[1]),version) AS version, (regexp_match(version, '^(.*)-([^-]+)$'))[2] AS release,sha256,
           regexp_replace(a.filename, '^.*/', '') AS file, format('%s/%s', r.default_url, a.filename) AS url, format('%s/%s', r.mirror_url, a.filename) AS mirror_url, size, size_install AS size_full FROM ext.apt a JOIN ext.repo r ON a.repo = r.id WHERE position('-16' in package) > 0 UNION ALL
    SELECT 15 AS pg, r.os, regexp_replace(regexp_replace(regexp_replace(regexp_replace(package, '-scripts$', ''), '-doc$', ''), '-dbgsym$', ''), '-pgq-node$', '-pgq') AS pname, r.org,r.type,r.os_code,r.os_arch,package as name, repo, version as ver, coalesce(((regexp_match(version, '^(.*)-([^-]+)$'))[1]),version) AS version, (regexp_match(version, '^(.*)-([^-]+)$'))[2] AS release,sha256,
           regexp_replace(a.filename, '^.*/', '') AS file, format('%s/%s', r.default_url, a.filename) AS url, format('%s/%s', r.mirror_url, a.filename) AS mirror_url, size, size_install AS size_full FROM ext.apt a JOIN ext.repo r ON a.repo = r.id WHERE position('-15' in package) > 0 UNION ALL
    SELECT 14 AS pg, r.os, regexp_replace(regexp_replace(regexp_replace(regexp_replace(package, '-scripts$', ''), '-doc$', ''), '-dbgsym$', ''), '-pgq-node$', '-pgq') AS pname, r.org,r.type,r.os_code,r.os_arch,package as name, repo, version as ver, coalesce(((regexp_match(version, '^(.*)-([^-]+)$'))[1]),version) AS version, (regexp_match(version, '^(.*)-([^-]+)$'))[2] AS release,sha256,
           regexp_replace(a.filename, '^.*/', '') AS file, format('%s/%s', r.default_url, a.filename) AS url, format('%s/%s', r.mirror_url, a.filename) AS mirror_url, size, size_install AS size_full FROM ext.apt a JOIN ext.repo r ON a.repo = r.id WHERE position('-14' in package) > 0 UNION ALL
    SELECT 13 AS pg, r.os, regexp_replace(regexp_replace(regexp_replace(regexp_replace(package, '-scripts$', ''), '-doc$', ''), '-dbgsym$', ''), '-pgq-node$', '-pgq') AS pname, r.org,r.type,r.os_code,r.os_arch,package as name, repo, version as ver, coalesce(((regexp_match(version, '^(.*)-([^-]+)$'))[1]),version) AS version, (regexp_match(version, '^(.*)-([^-]+)$'))[2] AS release,sha256,
           regexp_replace(a.filename, '^.*/', '') AS file, format('%s/%s', r.default_url, a.filename) AS url, format('%s/%s', r.mirror_url, a.filename) AS mirror_url, size, size_install AS size_full FROM ext.apt a JOIN ext.repo r ON a.repo = r.id WHERE position('-13' in package) > 0
    ) d
ORDER BY pg, os, pname, name, org, ver;


-----------------------------------
-- Latest Available Matrix
-----------------------------------
CREATE EXTENSION IF NOT EXISTS semver;

-- REFRESH MATERIALIZED VIEW ext.pkg;
DROP MATERIALIZED VIEW IF EXISTS ext.pkg CASCADE;
CREATE MATERIALIZED VIEW ext.pkg AS
    SELECT DISTINCT ON (pkg, pname, os)
        pkg, pname, os, pg, name, ver, org, type, os_code, os_arch, repo, version, release, file, sha256, url, mirror_url, size, size_full
    FROM
    (
        SELECT m.pkg, m.pg, m.os, name, ver, m.type, m.os_code, m.os_arch, m.pname, org,repo, version, release, file,sha256, url, mirror_url, size, size_full
        FROM ext.matrix m JOIN ext.package p ON m.os = p.os AND m.pname = p.name
    ) pa
    ORDER BY pkg, pname, os,
    ext.normalize_version(version)::SEMVER DESC, ver DESC, org DESC;


-- SELECT * FROM ext.pkg WHERE pname ~ 'citus';
-- SELECT * FROM ext.pkg WHERE pname ~ 'pg_graphql';



