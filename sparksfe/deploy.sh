#! /bin/bash

# Sync media files first (Cache: expire in 10weeks)
echo "\n--> Syncing media files..."
s3cmd sync --acl-public --exclude '*.*' --include '*.png' --include '*.jpg' --include '*.ico' --add-header="Expires: Sat, 20 Nov 2020 18:46:39 GMT" --add-header="Cache-Control: max-age=6048000"  dist/ s3://sparks.thirtytwobits.com/

# Sync Javascript and CSS assets next (Cache: expire in 1 week)
echo "\n--> Syncing .js and .css files..."
s3cmd sync --acl-public --exclude '*.*' --include  '*.css' --include '*.js' --add-header="Cache-Control: max-age=604800"  dist/ s3://sparks.thirtytwobits.com/

# Sync html files (Cache: 2 hours)
echo "\n--> Syncing .html"
s3cmd sync --acl-public --exclude '*.*' --include  '*.html' --add-header="Cache-Control: no-cache"  dist/ s3://sparks.thirtytwobits.com/

# Sync everything else, but ignore the assets!
echo "\n--> Syncing everything else"
s3cmd sync --acl-public --exclude '.DS_Store' --exclude 'scripts/' --exclude 'styles/'  dist/ s3://sparks.thirtytwobits.com/

# Sync: remaining files & delete removed
s3cmd sync --acl-public --delete-removed  dist/ s3://sparks.thirtytwobits.com/

