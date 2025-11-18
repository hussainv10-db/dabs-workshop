# Databricks notebook source
# ===========================================================
# Starter Notebook Template
# - Minimal, aligns with standardized job and DLT templates
# - Includes naming conventions, required widgets, and UC setup
# ===========================================================

# =========================
# Notebook Identifiers — Naming Conventions & Builder
# =========================
# 1. Schema Name
#    - mdl_projectnumber_modelname      (i.e. mdl_54321_precon_forecasting)
#    - rpt_projectnumber_reportname     (i.e. rpt_12345_financial_reporting)
#    - src_sourcename                   (i.e. src_finance_road_map)
#    - z_sandbox_username               (i.e. z_sandbox_sean_)
#
# 2. Table Name
#    - tabledescription_medallionlayer  (e.g., monthly_safety_reports_gold)
#
# Notebook-owned identifiers are fixed per job — the table_name should match
# the notebook’s purpose exactly, ensuring consistency across DLT and Job YAMLs.

# ===========================================================
# Naming & placement
# -----------------------------------------------------------
# Repo path:    domains/<domain>/notebooks/<project>/<notebook>.py
# Examples:     domains/ops/notebooks/powerbiusage/activity_events_to_silver.py
#               domains/finance/notebooks/receivables/ingest_receivables.py
#
# Notebook name: match the job/pipeline intent exactly (lower_snake_case)
# table_name widget: should mirror notebook name where possible
# -----------------------------------------------------------

# COMMAND ----------

# Required imports
from pyspark.sql import functions as F

# COMMAND ----------

# -----------------------------------------------------------
# Standard runtime widgets (add more as needed for your workload)
# -----------------------------------------------------------
dbutils.widgets.text("catalog", "")          # e.g., empbi_dev / empbi_stg / empbi_prod
dbutils.widgets.text("schema", "")           # e.g., src_ops, mdl_finance_forecast
dbutils.widgets.text("table_name", "")       # e.g., monthly_safety_reports_gold
dbutils.widgets.text("read_volume_uri", "")  # e.g., /Volumes/empbi_prod/bi_team_blob/...
dbutils.widgets.text("read_subfolder", "")   # optional (for file-arrival jobs)
dbutils.widgets.text("extra_json", "{}")     # optional JSON blob for additional params

CATALOG         = dbutils.widgets.get("catalog").strip()
SCHEMA          = dbutils.widgets.get("schema").strip()
TABLE_NAME      = dbutils.widgets.get("table_name").strip()
READ_VOLUME_URI = dbutils.widgets.get("read_volume_uri").strip()
READ_SUBFOLDER  = dbutils.widgets.get("read_subfolder").strip()

assert CATALOG and SCHEMA, "Both catalog and schema are required."
spark.sql(f"USE CATALOG {CATALOG}")
spark.sql(f"CREATE SCHEMA IF NOT EXISTS `{CATALOG}`.`{SCHEMA}`")
spark.sql(f"USE {SCHEMA}")

# COMMAND ----------

# -----------------------------------------------------------
# Notebook logic starts here
# -----------------------------------------------------------
# Use the Read → Transform → Write pattern.
# Example:
# df = spark.table(f"`{CATALOG}`.`{SCHEMA}`.`source_table`")
# df = df.withColumn("ingested_at", F.current_timestamp())
# df.write.mode("overwrite").saveAsTable(f"`{CATALOG}`.`{SCHEMA}`.`{TABLE_NAME}`")

# Notes:
# - Maintain consistent identifiers (schema, table_name, notebook name).
# - Add additional widgets for dates, toggles, or keys as needed.
# - Use dbutils.secrets.get(scope="${var.secret_scope}", key="<key-name>") if secrets are required.
