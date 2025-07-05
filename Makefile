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



load:
	cat data/category.csv   | psql $(PGURL) -c "TRUNCATE pgext.category; COPY pgext.category FROM STDIN CSV HEADER;"
	cat data/repository.csv | psql $(PGURL) -c "TRUNCATE pgext.repository; COPY pgext.repository FROM STDIN CSV HEADER;"

save: save-data
save-data:
	psql $(PGURL) -c "COPY (SELECT * FROM ext.pigsty ORDER BY id) TO '/Users/vonng/pgsty/extension/data/pigsty.csv' CSV HEADER;"
	psql $(PGURL) -c "COPY (SELECT * FROM ext.extension ORDER BY id) TO '/Users/vonng/pgsty/extension/data/extension.csv' CSV HEADER;"
	psql $(PGURL) -c "COPY (select id,name,alias,category,lead,rpm_repo,rpm_pkg,rpm_pg,deb_repo,deb_pkg,deb_pg FROM ext.pigsty ORDER BY id) TO '/Users/vonng/pgsty/extension/data/ext.csv' CSV HEADER;"
	psql $(PGURL) -c "COPY (select * FROM ext.cate ORDER BY id) TO '/Users/vonng/pgsty/extension/data/cate.csv' CSV HEADER;"
	psql $(PGURL) -c "COPY (select * FROM ext.repo ORDER BY id) TO '/Users/vonng/pgsty/extension/data/repo.csv' CSV HEADER;"
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