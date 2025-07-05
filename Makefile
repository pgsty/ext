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

# building (SSG)
b: build
build:
	npm run build

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

# dump extension data to data dir
dump: save
save: save-data
save-data:
	psql $(PGURL) -c "COPY (SELECT * FROM ext.pigsty ORDER BY id) TO '/Users/vonng/pgsty/extension/data/pigsty.csv' CSV HEADER;"
	psql $(PGURL) -c "COPY (SELECT * FROM ext.extension ORDER BY id) TO '/Users/vonng/pgsty/extension/data/extension.csv' CSV HEADER;"
	psql $(PGURL) -c "COPY (select id,name,alias,category,lead,rpm_repo,rpm_pkg,rpm_pg,deb_repo,deb_pkg,deb_pg FROM ext.pigsty ORDER BY id) TO '/Users/vonng/pgsty/extension/data/ext.csv' CSV HEADER;"
	psql $(PGURL) -c "COPY (select * FROM ext.cate ORDER BY id) TO '/Users/vonng/pgsty/extension/data/cate.csv' CSV HEADER;"
	psql $(PGURL) -c "COPY (select * FROM ext.repo ORDER BY id) TO '/Users/vonng/pgsty/extension/data/repo.csv' CSV HEADER;"
# load extension data from data dir
load:
	psql $(PGURL) -c "TRUNCATE ext.extension; COPY ext.extension FROM '/Users/vonng/pgsty/extension/data/extension.csv' CSV HEADER;"

# inventory
.PHONY: default run gen dump save load