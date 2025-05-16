#!/bin/sh
cat <<EOF > /app/frontend/env-config.js
window.env = {
  VITE_LOCAL_DISCOVERY: "${LOCAL_DISCOVERY}"
};
EOF

exec "$@"
