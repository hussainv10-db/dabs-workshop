# dabs-workshop
Repository for DABs workshop

This repository houses domain-based workloads built for Databricks and managed via Databricks Bundles.
Each domain (e.g. ops, finance) contains its own notebooks, pipelines, and jobs that together form a structured ELT framework.

Repository Layout
.github/
  ├── domains/
  │   ├── ops/                    # Core operations domain
  │   │   ├── databricks.yml      # Main bundle config (dev/stg/prod)
  │   │   ├── jobs/               # Scheduled jobs (pipeline refreshes, ingestions)
  │   │   ├── dlt/                # Delta Live Tables pipeline definitions
  │   │   ├── notebooks/          # Databricks notebooks (Python, SQL, or notebooks-as-code)
  │   │   ├── models/             # ML or analytical models
  │   │   ├── views/orm/          # ORM-style reusable SQL/Python views
  │   │   ├── resources/          # Shared templates and fixtures
  │   │   └── staging/, test/, utils/  # Support folders
  │   │
  │   ├── finance/                # Finance domain (same structure as above)
  │   └── precon/                 # Preconstruction domain (same structure as above)
  │
  ├── users/                      # Individual sandboxes for testing and prototyping
  │   └── <user>/scratch/         # Experimental work (dev-only)
  │
  ├── workflows/                  # GitHub Actions (Admin controlled)
  │   ├── path-guard.yml
  │   └── auto-merge-when-safe.yml
  │
  ├── CODEOWNERS                  # Review ownership (mirrors path-owners.json) (Admin controlled)
  ├── path-owners.json            # Used for workflow logic
  └── pull_request_template.md


Databricks Bundle Overview (Ops Domain Example - all domains mirror this)

NOTE: Bundles are defined at the domain level, eg. ops, finance are their own bundles within the same repo

The Ops bundle (.github/domains/ops/databricks.yml) defines how jobs, pipelines, and resources are deployed to Databricks across environments.

Key properties
| Setting               | Description                                                                    |
| --------------------- | ------------------------------------------------------------------------------ |
| `bundle.name`         | Unique bundle ID per engineer or deployment (e.g., `rpropp-dbab`).             |
| `workspace.root_path` | Deployment root in Databricks workspace.                                       |
| `include`             | Globs picking up all job and DLT YAMLs for packaging.                          |
| `catalog`             | Environment-scoped schema base (e.g., `dev`, `stg`, `prod`). |
| `read_volume_uri`     | Fixed path to production volume for data sharing.                              |
| `secret_scope`        | Default scope for environment secrets.                                         |
| `job_pause_status`    | Controls whether jobs start paused or unpaused by env.                         |
| `targets`             | Host configuration for dev/stg/prod workspaces.                                |

	
Environment strategy

Single monolithic bundle deployed from VS Code.
Developers switch between dev, stg, and prod via the Databricks VS Code extension target selector.
Only prod targets are unpaused by default.


Domain Layout – Example: ops

Each folder under ops represents a logical project or integration.

| Folder                        | Purpose                                                                                                                                                                    |
| ----------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `dlt/`                        | Delta Live Tables pipelines (e.g., PowerBI Usage, SAP, Procore, OpenAI). Each pipeline YAML defines a Databricks pipeline with secrets, source config, and runtime params. |
| `jobs/`                       | Job definitions that trigger pipeline refreshes or scheduled ingestions. Example: `powerbi_activity_to_silver_refresh.yml` refreshes the PowerBI Activity pipeline daily.  |
| `notebooks/`                  | Executable Python or SQL notebooks deployed to Databricks. These contain the transformation logic used by pipelines and jobs.                                              |
| `models/`                     | Reusable ML or statistical logic (e.g., `ai_revenue_model_registration_and_promotion.py`).                                                                                 |
| `views/orm/`                  | Python/SQL view definitions to expose consistent ORM-like tables across downstream users.                                                                                  |
| `resources/`                  | Common templates, YAML fixtures, and supporting assets.                                                                                                                    |
| `staging/`, `test/`, `utils/` | Optional utility directories to support testing, staging tables, and helper scripts.                                                                                       |



How Jobs and Pipelines Work

Example 1: Power BI Activity Pipeline

Defined in ops/dlt/powerbiusage/powerbiusage.yml:

Creates a pipeline named powerbi_activity_to_silver.
Reads from the Power BI Activity API.
Uses notebook libraries stored under /notebooks/powerbiusage/.
Manages runtime configuration like API credentials, OAuth endpoints, and backfill windows.

Example 1 above then is refreshed by Example 2 below:

Example 2: Pipeline Refresh Job

Defined in ops/jobs/powerbi_activity_to_silver_refresh.yml:

Triggers the above pipeline daily using a pipeline_task.
Sends on-failure alerts to the owner.
Inherits environment variables from the bundle (e.g., catalog, secret scope, pause status).

Operational pattern

Each DLT pipeline is declared in dlt/<project>/<pipeline_name>.yml.
A paired job YAML under jobs/ runs the pipeline on a defined schedule.
Both are pulled into deployment automatically via include: globs in databricks.yml.

User Folders

Located under .github/users/<username>/.
Serve as personal development sandboxes for testing notebooks, DLT pipelines, and prototypes.
Only dev deployments should reference these.
Production and staging deployments are going to be blocked from including user folders via workflow guards.

Ownership and Review Rules

CODEOWNERS defines official GitHub review ownership per domain.
path-owners.json mirrors this mapping and drives CI logic (used by workflows like path-guard.yml).
Required reviews are enforced via branch protection and CODEOWNERS.

Example from path-owners.json:

{
  "hussainv10": [".github/domains/finance/**"],
  "hussainv10-db": [".github/domains/ops/**"]
}


CI/CD Workflows

path-guard.yml – ensures only owners of changed paths can merge.
auto-merge-when-safe.yml – auto-merges PRs when checks pass and required owners approved.


Deployment Workflow

Develop/test notebooks or pipelines in your user folder.
Once validated, promote them to the appropriate domain (ops, finance, precon).
Update or add job/pipeline YAMLs.
Run or trigger a Databricks Bundle deployment from VS Code:
Select dev, stg, or prod target.
Deploy via Databricks CLI or VS Code “Deploy Bundle” action.

Monitor deployment output in Databricks workspace under:
/Workspace/Users/<you>/.bundle/<bundle-name>/<target>/

Deploy roles & model

| Phase      | Model                        | Who Deploys                           | Risks                     | Notes                                          |
| ---------- | ---------------------------- | ------------------------------------- | ------------------------- | ---------------------------------------------- |
| **Now**    | Manual deploy via VS Code    | One domain owner (backup optional)    | Low risk of duplication   | Keeps consistency until bundles stabilize      |
| **Next**   | Multi-bundle per domain      | Each sub-bundle has 1–2 owners        | Slightly more maintenance | Easier delegation, smaller blast radius        |
| **Future** | Service principal CI deploys | Automated (triggered by release tags) | Minimal                   | Ideal state: approvals only, no manual deploys |

