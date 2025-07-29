#!/bin/sh

echo "⏳ Attente que PostgreSQL soit prêt..."

until PGPASSWORD=$DB_PASSWORD pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" > /dev/null 2>&1; do
  echo "❌ PostgreSQL pas encore prêt — nouvelle tentative..."
  sleep 2
done

echo "✅ PostgreSQL est prêt."
