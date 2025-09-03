#==============================================================#
# File      :   Makefile
# Ctime     :   2024-10-30
# Mtime     :   2025-07-05
# Desc      :   Makefile shortcuts
# Path      :   Makefile
# Copyright (C) 2019-2025 Ruohang Feng
#==============================================================#

default: dev

PGURL="postgres:///vonng"

# run next dev server (3000)
d: dev
dev:
	TURBO_CONCURRENCY=25 npm run dev

# building (SSG) - new optimized version
b: build
build:
	TURBO_CONCURRENCY=25 npm run build

# building with legacy MDX files
build-mdx: gen-mdx
	TURBO_CONCURRENCY=25 npm run build

# open browser to view the app
v: view
view:
	open 'http://localhost:3000'

# remove the build output directory
c: clean
clean:
	rm -rf out

# run pnpm install
i: install
install:
	pnpm install

# update npm dependencies to the latest version
u: update
update:
	pnpm update


# serve wiht
s: serve
serve:
	cd out && python3 -m http.server 3001


# dump extension data to data dir
dump:
	psql $(PGURL) -c "COPY (SELECT * FROM pgext.category ORDER BY id) TO STDOUT CSV HEADER;"   > data/category.csv
	psql $(PGURL) -c "COPY (SELECT * FROM pgext.repository ORDER BY id) TO STDOUT CSV HEADER;" > data/repository.csv
	psql $(PGURL) -c "COPY (SELECT * FROM pgext.extension ORDER BY id) TO STDOUT CSV HEADER;"   > data/extension.csv
	psql $(PGURL) -c "COPY (SELECT * FROM pgext.matrix ORDER BY pg,os,pkg) TO STDOUT CSV HEADER;"     > data/matrix.csv
	psql $(PGURL) -c "COPY (SELECT id,name,pkg AS alias,category,url,license,tags,version,repo,lang,has_bin AS utility,lead,has_lib AS has_solib,need_ddl,need_load,trusted,relocatable,schemas,pg_ver,requires,rpm_ver,rpm_repo,rpm_pkg,rpm_pg,rpm_deps,deb_ver,deb_repo,deb_pkg,deb_deps,deb_pg,NULL as bad_case,en_desc,zh_desc,comment FROM pgext.extension ORDER BY id) TO STDOUT CSV HEADER"   > data/pigsty.csv
	psql $(PGURL) -c "COPY (select id,name,pkg as alias,category,lead,rpm_repo,rpm_pkg,rpm_pg,deb_repo,deb_pkg,deb_pg FROM pgext.extension ORDER BY id) TO STDOUT CSV HEADER;" > data/ext.csv

loade:
	cat data/extension.csv   | psql $(PGURL) -c "TRUNCATE pgext.extension; COPY pgext.extension FROM STDIN CSV HEADER;"

load:
	cat data/category.csv   | psql $(PGURL) -c "TRUNCATE pgext.category; COPY pgext.category FROM STDIN CSV HEADER;"
	cat data/repository.csv | psql $(PGURL) -c "TRUNCATE pgext.repository; COPY pgext.repository FROM STDIN CSV HEADER;"


# load extension data from data dir
#load:
#	psql $(PGURL) -c "TRUNCATE ext.extension; COPY ext.extension FROM '/Users/vonng/pgsty/extension/data/extension.csv' CSV HEADER;"

# generate extension data in JSON format (optimized)
gen-ext:
	@echo "Generating extension JSON data..."
	@source ~/.venv/bin/activate && python bin/gen-ext-json.py
	@echo "Extension JSON data generated in data/extensions/"

# generate extension MDX files (legacy)
gen-mdx:
	@echo "Generating extension MDX files..."
	@source ~/.venv/bin/activate && python bin/gen-ext.py
	@echo "Extension MDX files generated in content/docs/ext/"

# inventory
.PHONY: default run gen dump save load gen-json gen-mdx build-mdx