#!/bin/bash
# MinIO bucket setup script for Ledgerly

set -e

echo "Setting up MinIO buckets for Ledgerly..."

# Wait for MinIO to be ready
echo "Waiting for MinIO to be ready..."
until mc alias set local http://minio:9000 minioadmin minioadmin; do
  echo "MinIO not ready yet, waiting 5 seconds..."
  sleep 5
done

# Create buckets
echo "Creating buckets..."
mc mb local/ledgerly-statements --ignore-existing
mc mb local/ledgerly-temp --ignore-existing
mc mb local/ledgerly-backups --ignore-existing

# Set bucket policies
echo "Setting bucket policies..."

# Statements bucket - private (pre-signed URLs only)
mc anonymous set none local/ledgerly-statements

# Temp bucket - private (for upload processing)
mc anonymous set none local/ledgerly-temp

# Backups bucket - private
mc anonymous set none local/ledgerly-backups

# Set lifecycle policies
echo "Setting lifecycle policies..."

# Auto-delete temp files after 24 hours
cat > /tmp/temp-lifecycle.json <<EOF
{
    "Rules": [
        {
            "ID": "delete-temp-files",
            "Status": "Enabled",
            "Expiration": {
                "Days": 1
            }
        }
    ]
}
EOF

mc ilm import local/ledgerly-temp < /tmp/temp-lifecycle.json

# Auto-delete old statements after 90 days (configurable)
cat > /tmp/statements-lifecycle.json <<EOF
{
    "Rules": [
        {
            "ID": "delete-old-statements",
            "Status": "Enabled",
            "Expiration": {
                "Days": 90
            }
        }
    ]
}
EOF

mc ilm import local/ledgerly-statements < /tmp/statements-lifecycle.json

echo "MinIO bucket setup completed successfully!"
echo "Available buckets:"
mc ls local/
