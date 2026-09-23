<<<<<<< HEAD
#!/bin/bash
# ==============================================================================
# ULPF — Stop Script
# Gracefully shuts down containers while preserving persistent volumes
# ==============================================================================

echo " Stopping ULPF container stack..."
docker compose down

echo ""
echo " All ULPF containers stopped successfully."
echo " Persistent volumes (MinIO raw logs, OpenSearch index, SQLite DB) are safely preserved."
echo "   To start again: ./scripts/start.sh"
echo "   To completely wipe data: ./scripts/reset.sh"
=======
#!/bin/bash
# ==============================================================================
# ULPF — Stop Script
# Gracefully shuts down containers while preserving persistent volumes
# ==============================================================================

echo " Stopping ULPF container stack..."
docker compose down

echo ""
echo " All ULPF containers stopped successfully."
echo " Persistent volumes (MinIO raw logs, OpenSearch index, SQLite DB) are safely preserved."
echo "   To start again: ./scripts/start.sh"
echo "   To completely wipe data: ./scripts/reset.sh"
>>>>>>> 3831b7383e78d54d129d8499c87cadb87be6e6c0
