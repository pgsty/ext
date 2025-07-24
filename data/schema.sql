-----------------------------------
-- Schema: pgext
-----------------------------------
-- DROP SCHEMA IF EXISTS pgext CASCADE;
CREATE SCHEMA IF NOT EXISTS pgext;
CREATE EXTENSION IF NOT EXISTS semver;


-----------------------------------
-- Extension Category (16 category)
-----------------------------------
CREATE TABLE IF NOT EXISTS pgext.category (
    id      INTEGER PRIMARY KEY,
    name    TEXT UNIQUE,
    icon1    TEXT,   -- font-awesome
    icon2    TEXT,   -- lucid icon
    extra   JSONB DEFAULT '{}'::JSONB,
    zh_desc TEXT,
    en_desc TEXT
);

INSERT INTO pgext.category (id, name, icon1, zh_desc, en_desc)
    SELECT id , name ,icon, zh_desc, en_desc FROM ext.cate ORDER BY id;

-- SELECT category, min(id) / 100 FROM ext.extension GROUP BY category ORDER BY min(id);
-- COPY (select * FROM pgext.category ORDER BY id) TO '/Users/vonng/pgsty/ext/data/category.csv' CSV HEADER;
-- TRUNCATE pgext.category; COPY pgext.category FROM '/Users/vonng/pgsty/ext/data/category.csv' CSV HEADER;


-----------------------------------
-- Postgres Major Version
-----------------------------------
DROP TABLE IF EXISTS pgext.pg_major CASCADE;
CREATE TABLE pgext.pg_major (
    pg  INTEGER PRIMARY KEY, -- PostgreSQL major version 13 - 18
    extra JSONB DEFAULT '{}'::JSONB -- extra metadata
);
COMMENT ON TABLE pgext.pg_major IS 'PostgreSQL Major Version Table';
INSERT INTO pgext.pg_major (pg, extra) VALUES
    (13, '{}'::JSONB),
    (14, '{}'::JSONB),
    (15, '{}'::JSONB),
    (16, '{}'::JSONB),
    (17, '{}'::JSONB),
    (18, '{}'::JSONB);


-----------------------------------
-- Extension Repository
-----------------------------------
DROP TABLE IF EXISTS pgext.repository CASCADE;
CREATE TABLE IF NOT EXISTS pgext.repository
(
    id           TEXT PRIMARY KEY,
    os           TEXT, -- u22.arm, el7.amd
    org          TEXT, -- pgdg, pigsty, ...
    type         TEXT, -- rpm / deb
    os_code      TEXT, -- u22, el7
    os_arch      TEXT, -- x86_64, aarch64
    default_url  TEXT, -- default pgdg/io url
    default_meta TEXT, -- where to get default meta
    mirror_url   TEXT, -- china mirror cc base url
    mirror_meta  TEXT, -- where to get mirror meta
    comment      TEXT, -- extra description
    extra        JSONB DEFAULT '{}'::JSONB -- extra metadata
);

COMMENT ON TABLE  pgext.repository IS 'PostgreSQL Extension Repo';
COMMENT ON COLUMN pgext.repository.id IS 'format as os_code.os_arch.org, such as d12.arm.pigsty';
COMMENT ON COLUMN pgext.repository.os IS 'os_code.arch, such as u22.arm, el7.amd';
COMMENT ON COLUMN pgext.repository.org IS 'repo upstream, pgdg, pigsty';
COMMENT ON COLUMN pgext.repository.type IS 'rpm or deb';
COMMENT ON COLUMN pgext.repository.os_code IS '3 char os code, like u24, el7, el8';
COMMENT ON COLUMN pgext.repository.os_arch IS 'amd or arm';
COMMENT ON COLUMN pgext.repository.default_url IS 'default base url of this repo (base of href)';
COMMENT ON COLUMN pgext.repository.default_meta IS 'metadata url, global default';
COMMENT ON COLUMN pgext.repository.mirror_url IS 'china mirror base url of this repo';
COMMENT ON COLUMN pgext.repository.mirror_meta IS 'metadata url, china mirror';
COMMENT ON COLUMN pgext.repository.comment IS 'extra description';
COMMENT ON COLUMN pgext.repository.extra IS 'extra metadata';

-- DROP TABLE IF EXISTS pgext.repo_data;
CREATE TABLE IF NOT EXISTS pgext.repo_data
(
    id           TEXT PRIMARY KEY, -- REFERENCES pgext.repository(id),
    etag         TEXT, -- etag of the repo data
    size         BIGINT, -- size of the repo data
    extra        JSONB, -- extra metadata
    data         BYTEA, -- the repo binary data
    last_modified TIMESTAMPTZ, -- last modified time
    update_at    TIMESTAMP DEFAULT now()::DATE
);

COMMENT ON TABLE  pgext.repo_data IS 'the repo metadata table';
COMMENT ON COLUMN pgext.repository.id IS 'format as os_code.os_arch.org, such as d12.arm.pigsty';
COMMENT ON COLUMN pgext.repo_data.etag IS 'etag of the repo data, used for cache';
COMMENT ON COLUMN pgext.repo_data.size IS 'size of the repo data, used for cache';
COMMENT ON COLUMN pgext.repo_data.extra IS 'extra metadata, used for cache';
COMMENT ON COLUMN pgext.repo_data.data IS 'the repo binary data, used for yum/apt repo';
COMMENT ON COLUMN pgext.repo_data.last_modified IS 'last modified time of the repo data file';
COMMENT ON COLUMN pgext.repo_data.update_at IS 'the last modified time of this record';

-- COPY pgext.repo_data TO '/Users/vonng/pgsty/ext/data/repo_data.csv' CSV HEADER;
-- TRUNCATE pgext.repo_data CASCADE; COPY pgext.repository FROM '/Users/vonng/pgsty/ext/data/repo_data.csv' CSV HEADER;


-----------------------------------
-- Extension
-----------------------------------
DROP TABLE IF EXISTS pgext.extension CASCADE;
CREATE TABLE IF NOT EXISTS pgext.extension
(
    id          INTEGER PRIMARY KEY,
    name        TEXT NOT NULL,
    pkg         TEXT NOT NULL,
    lead_ext    TEXT,
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
    requires    TEXT[], --
    require_by  TEXT[], -- extensions depend on this extension
    see_also    TEXT[], -- similar extensions
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
    source      TEXT,
    extra       JSONB,
    en_desc     TEXT,
    zh_desc     TEXT,
    comment     TEXT,
    mtime       DATE DEFAULT CURRENT_DATE
);

CREATE INDEX IF NOT EXISTS ext_name_pkg_idx ON pgext.extension (name,pkg);

COMMENT ON TABLE  pgext.extension IS 'PostgreSQL Extension Table';
COMMENT ON COLUMN pgext.extension.id IS 'Extension Identifier (integer)';
COMMENT ON COLUMN pgext.extension.name IS 'Extension Name (in system catalog)';
COMMENT ON COLUMN pgext.extension.pkg IS 'Normalized extension package name';
COMMENT ON COLUMN pgext.extension.lead_ext IS 'The leading extension in this package';
COMMENT ON COLUMN pgext.extension.category IS 'Category of this extension';
COMMENT ON COLUMN pgext.extension.state IS 'Extension State (available, deprecated, removed, not-ready)';
COMMENT ON COLUMN pgext.extension.url IS 'Extension Repo URL';
COMMENT ON COLUMN pgext.extension.license IS 'Extension License';
COMMENT ON COLUMN pgext.extension.tags IS 'Extra tags';
COMMENT ON COLUMN pgext.extension.version IS 'the latest available version of this extension';
COMMENT ON COLUMN pgext.extension.lang IS 'Programming Language of this extension';
COMMENT ON COLUMN pgext.extension.lead IS 'Mark the primary extension among one multi-ext package';
COMMENT ON COLUMN pgext.extension.has_bin IS 'does this extension has binary utils';
COMMENT ON COLUMN pgext.extension.has_lib IS 'Does the extension have shared library?';
COMMENT ON COLUMN pgext.extension.need_ddl IS 'Extension need `CREATE EXTENSION` to work?';
COMMENT ON COLUMN pgext.extension.need_load IS 'Require LOAD & shared_preload_libraries to work?';
COMMENT ON COLUMN pgext.extension.trusted IS 'A Trusted extension does not require superuser to work';
COMMENT ON COLUMN pgext.extension.relocatable IS 'Can this extension be relocated?';
COMMENT ON COLUMN pgext.extension.schemas IS 'Installed Schema, if not relocatable';
COMMENT ON COLUMN pgext.extension.pg_ver IS 'Supported PostgreSQL major versions';
COMMENT ON COLUMN pgext.extension.requires IS 'Dependencies of this extension';
COMMENT ON COLUMN pgext.extension.require_by IS 'List of extensions depend on this extension';
COMMENT ON COLUMN pgext.extension.see_also IS 'List of extensions that works well with this extension';
COMMENT ON COLUMN pgext.extension.rpm_pkg IS 'RPM package name, major version is replace with $v';
COMMENT ON COLUMN pgext.extension.deb_pkg IS 'DEB package name, major version is replace with $v';
COMMENT ON COLUMN pgext.extension.source IS 'Source code tarball name, if build by pigsty';
COMMENT ON COLUMN pgext.extension.en_desc IS 'English description';
COMMENT ON COLUMN pgext.extension.zh_desc IS 'Chinese description';
COMMENT ON COLUMN pgext.extension.comment IS 'Extra information';
COMMENT ON COLUMN pgext.extension.mtime IS 'Last Modify Time';

-- update require_by
-- UPDATE pgext.extension SET require_by = (SELECT array_agg(DISTINCT dependent.name ORDER BY dependent.name) FROM pgext.extension dependent WHERE pgext.extension.name = ANY(dependent.requires))
-- WHERE EXISTS (SELECT 1 FROM pgext.extension dependentWHERE pgext.extension.name = ANY(dependent.requires));

-- update lead extension
-- UPDATE pgext.extension SET lead_ext = (SELECT l.name FROM pgext.extension l WHERE l.pkg = pgext.extension.pkg AND l.lead = true LIMIT 1)

-- COPY (SELECT * FROM pgext.extension ORDER BY id) TO '/Users/vonng/pgsty/ext/data/extension.csv' CSV HEADER;
-- TRUNCATE pgext.extension; COPY pgext.extension FROM '/Users/vonng/pgsty/ext/data/extension.csv' CSV HEADER;


-----------------------------------
-- Extension Legacy
-----------------------------------
-- DROP VIEW IF EXISTS pgext.pigsty;
-- CREATE OR REPLACE VIEW pgext.pigsty AS
-- SELECT id,name,pkg AS alias,category,url,license,tags,version,repo,lang,has_bin AS utility,lead,has_lib AS has_solib,need_ddl,need_load,trusted,relocatable,
--        schemas,pg_ver,requires,rpm_ver,rpm_repo,rpm_pkg,rpm_pg,rpm_deps,deb_ver,deb_repo,deb_pkg,deb_deps,deb_pg,bad_case,en_desc,zh_desc,comment
-- FROM pgext..extension
-- ORDER BY id;


-----------------------------------
-- Availability Matrix
-----------------------------------
DROP TABLE IF EXISTS pgext.matrix CASCADE;
CREATE TABLE IF NOT EXISTS pgext.matrix
(
    pg      INTEGER,
    os      TEXT,
    type    TEXT,
    os_code TEXT,
    os_arch TEXT,
    pkg     TEXT,
    ext     TEXT,
    pname   TEXT,
    miss    BOOLEAN DEFAULT false, -- extension not available for this combo
    hide    BOOLEAN DEFAULT false, -- comment it in the extension cate list?
    pkg_repo TEXT DEFAULT NULL, -- the repo where the latest package is from
    pkg_ver   TEXT DEFAULT NULL, -- the latest version of this extension
    count   BIGINT DEFAULT 0,
    PRIMARY KEY (pg, os, pkg)
);
CREATE INDEX IF NOT EXISTS matrix_pg_os_pname_idx ON pgext.matrix(pg, os, pname);

COMMENT ON TABLE  pgext.matrix IS 'PostgreSQL Extension Availbility PG & OS Matrix';
COMMENT ON COLUMN pgext.matrix.pg IS 'PostgreSQL Major Version 13-17 (integer)';
COMMENT ON COLUMN pgext.matrix.os IS 'os.arch identifier like el8.arm, u24.amd';
COMMENT ON COLUMN pgext.matrix.type IS 'platform package type rpm or deb';
COMMENT ON COLUMN pgext.matrix.os_code IS '3 char os code, like u24, el7, el8';
COMMENT ON COLUMN pgext.matrix.os_arch IS 'simplified arch name: amd or arm';
COMMENT ON COLUMN pgext.matrix.pkg IS 'Normalized extension package name';
COMMENT ON COLUMN pgext.matrix.pkg IS 'The leading extension in this package';
COMMENT ON COLUMN pgext.matrix.pname IS 'PG Major Versioned DEB/RPM Package Name';
COMMENT ON COLUMN pgext.matrix.miss IS 'Extension not available for this combination of PG & OS';
COMMENT ON COLUMN pgext.matrix.hide IS 'Hide this extension in the extension cate list?';
COMMENT ON COLUMN pgext.matrix.pkg_repo IS 'The repository where the latest package is from? PGDG/PIGSTY';
COMMENT ON COLUMN pgext.matrix.pkg_ver IS 'The latest version of this extension for this combination';
COMMENT ON COLUMN pgext.matrix.count IS 'Stat place holder counter';

-- if the extension list is changed, you can reload the matrix
CREATE OR REPLACE FUNCTION pgext.init_matrix() RETURNS BIGINT AS $$
DECLARE
BEGIN
    TRUNCATE pgext.matrix;
    INSERT INTO pgext.matrix (pg, os, type, os_code, os_arch, pkg, ext, pname, count)
        WITH packages AS (SELECT DISTINCT ON (pkg) pkg,name AS ext,id,name AS extname,category,state,pg_ver,replace(rpm_pkg, '*', '') AS rpm,deb_pkg AS deb FROM pgext.extension WHERE NOT contrib ORDER BY pkg, lead DESC)
        SELECT pg::INTEGER, os, type, os_code, os_arch, pkg, ext, pname, 0 AS count FROM
        (
            SELECT * FROM (SELECT pkg, ext,'deb' AS type, pg, os, os_code, os_arch, replace((regexp_split_to_array(deb, ' '))[1], '$v', pg::text) AS pname FROM packages, unnest(ARRAY[17,16,15,14,13]) AS pg, (SELECT distinct os, type, os_code, os_arch FROM pgext.repository WHERE type = 'deb' ORDER BY os) r) rp UNION ALL
            SELECT pkg, ext,'rpm' AS type, pg, os, os_code, os_arch, replace( (regexp_split_to_array(rpm, ' '))[1], '$v', pg::text) AS pname FROM packages, unnest(ARRAY[17,16,15,14,13]) AS pg, (SELECT distinct os, type, os_code, os_arch FROM pgext.repository WHERE type = 'rpm' ORDER BY os) r
        ) d ORDER BY pg DESC, type, os;
    UPDATE pgext.matrix SET pname = replace(pname, 'pgaudit', 'pgaudit' || (pg+2)::TEXT ) WHERE pkg = 'pgaudit' AND pg IN (13,14,15) AND type = 'rpm';
    RETURN (SELECT count(*) FROM pgext.matrix);
END;
$$ LANGUAGE PlPGSQL VOLATILE;

COMMENT ON FUNCTION pgext.init_matrix() IS 'init extension package matrix data';

SELECT pgext.init_matrix();

-- SELECT category, min(id) / 100 FROM ext.extension GROUP BY category ORDER BY min(id);
-- COPY (select * FROM pgext.matrix ORDER BY pg,os,pkg) TO '/Users/vonng/pgsty/ext/data/matrix.csv' CSV HEADER;
-- TRUNCATE pgext.matrix; COPY pgext.matrix FROM '/Users/vonng/pgsty/ext/data/matrix.csv' CSV HEADER;

-----------------------------------
-- YUM Packages
-----------------------------------
DROP TABLE IF EXISTS pgext.yum;
CREATE TABLE IF NOT EXISTS pgext.yum
(
    repo             TEXT    NOT NULL REFERENCES pgext.repository (id),
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
DROP TABLE IF EXISTS pgext.apt;
CREATE TABLE IF NOT EXISTS pgext.apt
(
    repo         TEXT NOT NULL REFERENCES pgext.repository (id),
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
    PRIMARY KEY (repo,package,version,architecture)
);


-----------------------------------
-- Normalize Version String
-----------------------------------
CREATE OR REPLACE FUNCTION pgext.normalize_version(version text) RETURNS text AS $$
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
-- RPM / DEB Merged Package Table
-----------------------------------
DROP TABLE IF EXISTS pgext.package CASCADE;
CREATE TABLE IF NOT EXISTS pgext.package
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

CREATE INDEX IF NOT EXISTS package_os_pname_idx ON pgext.package USING BTREE(os,pname);


-- if the yum / apt packages changed, you can reload the package table
CREATE OR REPLACE FUNCTION pgext.reload_package() RETURNS BIGINT AS $$
DECLARE
BEGIN
    TRUNCATE pgext.package;
    INSERT INTO pgext.package
    SELECT pg, os, pname, org, type, os_code, os_arch,  repo, name, ver, version, release, file, d.sha256,url, mirror_url, size, size_full
    FROM
        (
            SELECT 17 as pg, r.os, substr(name, 0, position('_17' in name)+3) AS pname, r.org,r.type,r.os_code,r.os_arch,pkg_id AS sha256,
                   repo, name, version || '-' || release AS ver, version, release, regexp_replace(y.location_href, '^.*/', '') AS file, format('%s/%s', r.default_url, y.location_href) AS url, format('%s/%s', r.mirror_url, y.location_href) AS mirror_url, size_package AS size, size_installed AS size_full
            FROM pgext.yum y JOIN pgext.repository r ON y.repo = r.id WHERE position('_17' in name) > 0
            UNION ALL
            SELECT 16 as pg, r.os, substr(name, 0, position('_16' in name)+3) AS pname, r.org,r.type,r.os_code,r.os_arch,pkg_id AS sha256,
                   repo, name, version || '-' || release AS ver, version, release, regexp_replace(y.location_href, '^.*/', '') AS file, format('%s/%s', r.default_url, y.location_href) AS url, format('%s/%s', r.mirror_url, y.location_href) AS mirror_url, size_package AS size, size_installed AS size_full
            FROM pgext.yum y JOIN pgext.repository r ON y.repo = r.id WHERE position('_16' in name) > 0
            UNION ALL
            SELECT 15 as pg, r.os, substr(name, 0, position('_15' in name)+3) AS pname, r.org,r.type,r.os_code,r.os_arch,pkg_id AS sha256,
                   repo, name, version || '-' || release AS ver, version, release, regexp_replace(y.location_href, '^.*/', '') AS file, format('%s/%s', r.default_url, y.location_href) AS url, format('%s/%s', r.mirror_url, y.location_href) AS mirror_url, size_package AS size, size_installed AS size_full
            FROM pgext.yum y JOIN pgext.repository r ON y.repo = r.id WHERE position('_15' in name) > 0
            UNION ALL
            SELECT 14 as pg, r.os, substr(name, 0, position('_14' in name)+3) AS pname, r.org,r.type,r.os_code,r.os_arch,pkg_id AS sha256,
                   repo, name, version || '-' || release AS ver, version, release, regexp_replace(y.location_href, '^.*/', '') AS file, format('%s/%s', r.default_url, y.location_href) AS url, format('%s/%s', r.mirror_url, y.location_href) AS mirror_url, size_package AS size, size_installed AS size_full
            FROM pgext.yum y JOIN pgext.repository r ON y.repo = r.id WHERE position('_14' in name) > 0
            UNION ALL
            SELECT 13 as pg, r.os, substr(name, 0, position('_13' in name)+3) AS pname, r.org,r.type,r.os_code,r.os_arch,pkg_id AS sha256,
                   repo, name, version || '-' || release AS ver, version, release, regexp_replace(y.location_href, '^.*/', '') AS file, format('%s/%s', r.default_url, y.location_href) AS url, format('%s/%s', r.mirror_url, y.location_href) AS mirror_url, size_package AS size, size_installed AS size_full
            FROM pgext.yum y JOIN pgext.repository r ON y.repo = r.id WHERE position('_13' in name) > 0
        ) d
    UNION ALL
    SELECT pg, os, pname, org, type, os_code, os_arch, repo, name, ver, version, release, file, sha256, url, mirror_url, size, size_full
    FROM
        (
            SELECT 17 AS pg, r.os, regexp_replace(regexp_replace(regexp_replace(regexp_replace(package, '-scripts$', ''), '-doc$', ''), '-dbgsym$', ''), '-pgq-node$', '-pgq') AS pname, r.org,r.type,r.os_code,r.os_arch,package as name, repo, version as ver, coalesce(((regexp_match(version, '^(.*)-([^-]+)$'))[1]),version) AS version, (regexp_match(version, '^(.*)-([^-]+)$'))[2] AS release,sha256,
                   regexp_replace(a.filename, '^.*/', '') AS file, format('%s/%s', r.default_url, a.filename) AS url, format('%s/%s', r.mirror_url, a.filename) AS mirror_url, size, size_install AS size_full FROM pgext.apt a JOIN pgext.repository r ON a.repo = r.id WHERE position('-17' in package) > 0 UNION ALL
            SELECT 16 AS pg, r.os, regexp_replace(regexp_replace(regexp_replace(regexp_replace(package, '-scripts$', ''), '-doc$', ''), '-dbgsym$', ''), '-pgq-node$', '-pgq') AS pname, r.org,r.type,r.os_code,r.os_arch,package as name, repo, version as ver, coalesce(((regexp_match(version, '^(.*)-([^-]+)$'))[1]),version) AS version, (regexp_match(version, '^(.*)-([^-]+)$'))[2] AS release,sha256,
                   regexp_replace(a.filename, '^.*/', '') AS file, format('%s/%s', r.default_url, a.filename) AS url, format('%s/%s', r.mirror_url, a.filename) AS mirror_url, size, size_install AS size_full FROM pgext.apt a JOIN pgext.repository r ON a.repo = r.id WHERE position('-16' in package) > 0 UNION ALL
            SELECT 15 AS pg, r.os, regexp_replace(regexp_replace(regexp_replace(regexp_replace(package, '-scripts$', ''), '-doc$', ''), '-dbgsym$', ''), '-pgq-node$', '-pgq') AS pname, r.org,r.type,r.os_code,r.os_arch,package as name, repo, version as ver, coalesce(((regexp_match(version, '^(.*)-([^-]+)$'))[1]),version) AS version, (regexp_match(version, '^(.*)-([^-]+)$'))[2] AS release,sha256,
                   regexp_replace(a.filename, '^.*/', '') AS file, format('%s/%s', r.default_url, a.filename) AS url, format('%s/%s', r.mirror_url, a.filename) AS mirror_url, size, size_install AS size_full FROM pgext.apt a JOIN pgext.repository r ON a.repo = r.id WHERE position('-15' in package) > 0 UNION ALL
            SELECT 14 AS pg, r.os, regexp_replace(regexp_replace(regexp_replace(regexp_replace(package, '-scripts$', ''), '-doc$', ''), '-dbgsym$', ''), '-pgq-node$', '-pgq') AS pname, r.org,r.type,r.os_code,r.os_arch,package as name, repo, version as ver, coalesce(((regexp_match(version, '^(.*)-([^-]+)$'))[1]),version) AS version, (regexp_match(version, '^(.*)-([^-]+)$'))[2] AS release,sha256,
                   regexp_replace(a.filename, '^.*/', '') AS file, format('%s/%s', r.default_url, a.filename) AS url, format('%s/%s', r.mirror_url, a.filename) AS mirror_url, size, size_install AS size_full FROM pgext.apt a JOIN pgext.repository r ON a.repo = r.id WHERE position('-14' in package) > 0 UNION ALL
            SELECT 13 AS pg, r.os, regexp_replace(regexp_replace(regexp_replace(regexp_replace(package, '-scripts$', ''), '-doc$', ''), '-dbgsym$', ''), '-pgq-node$', '-pgq') AS pname, r.org,r.type,r.os_code,r.os_arch,package as name, repo, version as ver, coalesce(((regexp_match(version, '^(.*)-([^-]+)$'))[1]),version) AS version, (regexp_match(version, '^(.*)-([^-]+)$'))[2] AS release,sha256,
                   regexp_replace(a.filename, '^.*/', '') AS file, format('%s/%s', r.default_url, a.filename) AS url, format('%s/%s', r.mirror_url, a.filename) AS mirror_url, size, size_install AS size_full FROM pgext.apt a JOIN pgext.repository r ON a.repo = r.id WHERE position('-13' in package) > 0
        ) d
    ORDER BY pg, os, pname, name, org, ver;
    RETURN (SELECT count(*) FROM pgext.package);
END;
$$ LANGUAGE PlPGSQL VOLATILE;

COMMENT ON FUNCTION pgext.reload_package() IS 'reload apt/yum package, return the count of packages';


-----------------------------------
-- Availability View
-----------------------------------
DROP VIEW IF EXISTS pgext.availability CASCADE;
CREATE OR REPLACE VIEW pgext.availability AS
SELECT pkg, ext, pname, os, pg, name, ver, org, type, os_code, os_arch, repo, version, release, file, sha256, url, mirror_url, size, size_full
FROM
    (
        SELECT m.pkg, m.ext, m.pg, m.os, name, ver, m.type, m.os_code, m.os_arch, m.pname, org, repo, version, release, file,sha256, url, mirror_url, size, size_full
        FROM pgext.matrix m JOIN pgext.package p ON m.os = p.os AND m.pname = p.name
    ) pa
ORDER BY pkg, pname, os, pgext.normalize_version(version)::SEMVER DESC, ver DESC, org DESC;

-- SELECT * FROM ext.availability WHERE pkg = 'pgvector';


-----------------------------------
-- Update Matrix Statistics
-----------------------------------
CREATE OR REPLACE FUNCTION pgext.update_matrix() RETURNS BIGINT AS $$
DECLARE
    updated_count BIGINT;
BEGIN
    -- Single UPDATE statement that combines all three operations:
    -- 1. Calculate count from availability
    -- 2. Get the latest package info (pkg_repo, pkg_ver)
    -- 3. Handle NULL cases
    WITH availability_stats AS (
        SELECT 
            m.pg, m.os, m.pkg, m.pname,
            COUNT(a.pkg) as pkg_count,
            FIRST_VALUE(a.org) OVER (
                PARTITION BY m.pg, m.os, m.pkg, m.pname 
                ORDER BY pgext.normalize_version(a.version)::SEMVER DESC, a.ver DESC, a.org DESC
            ) as latest_repo,
            FIRST_VALUE(a.version) OVER (
                PARTITION BY m.pg, m.os, m.pkg, m.pname 
                ORDER BY pgext.normalize_version(a.version)::SEMVER DESC, a.ver DESC, a.org DESC
            ) as latest_version
        FROM pgext.matrix m
        LEFT JOIN pgext.availability a ON (
            a.pkg = m.pkg AND a.pg = m.pg AND a.os = m.os
        )
        GROUP BY m.pg, m.os, m.pkg, m.pname, a.org, a.version, a.ver
    ),
    aggregated_stats AS (
        SELECT 
            pg, os, pkg, pname,
            SUM(pkg_count) as total_count,
            FIRST_VALUE(latest_repo) OVER (
                PARTITION BY pg, os, pkg, pname 
                ORDER BY latest_version DESC NULLS LAST
            ) as final_repo,
            FIRST_VALUE(latest_version) OVER (
                PARTITION BY pg, os, pkg, pname 
                ORDER BY latest_version DESC NULLS LAST
            ) as final_version
        FROM availability_stats
        GROUP BY pg, os, pkg, pname, latest_repo, latest_version
    ),
    final_stats AS (
        SELECT DISTINCT ON (pg, os, pkg, pname)
            pg, os, pkg, pname,
            total_count,
            final_repo,
            final_version
        FROM aggregated_stats
        ORDER BY pg, os, pkg, pname
    )
    UPDATE pgext.matrix 
    SET 
        count = COALESCE(fs.total_count, 0),
        pkg_repo = fs.final_repo,
        pkg_ver = fs.final_version
    FROM final_stats fs
    WHERE matrix.pg = fs.pg 
      AND matrix.os = fs.os 
      AND matrix.pkg = fs.pkg 
      AND matrix.pname = fs.pname;

    -- Handle any remaining NULL cases (fallback)
    UPDATE pgext.matrix 
    SET count = 0, pkg_repo = NULL, pkg_ver = NULL 
    WHERE count IS NULL;

    RETURN updated_count;
END;
$$ LANGUAGE PlPGSQL VOLATILE;

COMMENT ON FUNCTION pgext.update_matrix() IS 'Update matrix table with package counts and latest version info';



-----------------------------------
-- Update Matrix Statistics
-----------------------------------
CREATE OR REPLACE FUNCTION pgext.update_matrix() RETURNS BIGINT AS $$
BEGIN
    UPDATE pgext.matrix SET count = (SELECT COUNT(*) FROM pgext.availability
        WHERE availability.pkg = matrix.pkg
          AND availability.pg = matrix.pg
          AND availability.os = matrix.os
    );

    WITH latest_packages AS (
        SELECT DISTINCT ON (pkg, pname, os) pkg, pname, os, pg, org as pkg_repo, version as pkg_ver FROM pgext.availability
        ORDER BY pkg, pname, os, pgext.normalize_version(version)::SEMVER DESC, ver DESC, org DESC
    ) UPDATE pgext.matrix SET pkg_repo = lp.pkg_repo, pkg_ver = lp.pkg_ver
    FROM latest_packages lp WHERE matrix.pkg = lp.pkg AND matrix.pname = lp.pname AND matrix.os = lp.os AND matrix.pg = lp.pg;

    UPDATE pgext.matrix SET count = 0, pkg_repo = NULL, pkg_ver = NULL WHERE count IS NULL;
    UPDATE pgext.matrix SET miss = true WHERE count = 0 OR count IS NULL;
    UPDATE pgext.matrix SET miss = false WHERE count > 0;
    RETURN (SELECT count(*) FROM pgext.matrix);
END;
$$ LANGUAGE PlPGSQL VOLATILE;
COMMENT ON FUNCTION pgext.update_matrix() IS 'Update matrix table with package counts and latest version info';



-----------------------------------
-- Reload
-----------------------------------
SELECT pgext.init_matrix();
SELECT pgext.reload_package();
SELECT pgext.update_matrix();
VACUUM FULL pgext.matrix;