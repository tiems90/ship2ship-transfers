# Databricks notebook source
# MAGIC %md This notebook sets up the companion cluster(s) to run the solution accelerator. It also creates the Workflow to illustrate the order of execution. Happy exploring! 
# MAGIC 🎉
# MAGIC 
# MAGIC **Steps**
# MAGIC 1. Simply attach this notebook to a cluster with DBR 11.0 and above, and hit Run-All for this notebook. A multi-step job and the clusters used in the job will be created for you and hyperlinks are printed on the last block of the notebook. 
# MAGIC 
# MAGIC 2. Run the accelerator notebooks: Feel free to explore the multi-step job page and **run the Workflow**, or **run the notebooks interactively** with the cluster to see how this solution accelerator executes. 
# MAGIC 
# MAGIC     2a. **Run the Workflow**: Navigate to the Workflow link and hit the `Run Now` 💥. 
# MAGIC   
# MAGIC     2b. **Run the notebooks interactively**: Attach the notebook with the cluster(s) created and execute as described in the `job_json['tasks']` below.
# MAGIC 
# MAGIC **Prerequisites** 
# MAGIC 1. You need to have cluster creation permissions in this workspace.
# MAGIC 
# MAGIC 2. In case the environment has cluster-policies that interfere with automated deployment, you may need to manually create the cluster in accordance with the workspace cluster policy. The `job_json` definition below still provides valuable information about the configuration these series of notebooks should run with. 
# MAGIC 
# MAGIC **Notes**
# MAGIC 1. The pipelines, workflows and clusters created in this script are not user-specific. Keep in mind that rerunning this script again after modification resets them for other users too.
# MAGIC 
# MAGIC 2. If the job execution fails, please confirm that you have set up other environment dependencies as specified in the accelerator notebooks. Accelerators may require the user to set up additional cloud infra or secrets to manage credentials. 

# COMMAND ----------

# DBTITLE 0,Install util packages
# MAGIC %pip install git+https://github.com/databricks-academy/dbacademy-rest git+https://github.com/databricks-academy/dbacademy-gems git+https://github.com/databricks-industry-solutions/notebook-solution-companion

# COMMAND ----------

from solacc.companion import NotebookSolutionCompanion

# COMMAND ----------

job_json = {
        "timeout_seconds": 7200,
        "max_concurrent_runs": 1,
        "tags": {
            "usage": "solacc_testing",
            "group": "MFG"
        },
        "tasks": [
        {
            "job_cluster_key": "ship2ship_cluster",
            "libraries": [],
            "notebook_task": {
                "notebook_path": f"00_README"
            },
            "task_key": "ship2ship_00",
            "description": ""
        },
        {
            "job_cluster_key": "ship2ship_cluster",
            "notebook_task": {
                "notebook_path": f"01_Data Prep"
            },
            "task_key": "ship2ship_01",
            "depends_on": [
                {
                    "task_key": "ship2ship_00"
                }
            ]
        },
        {
            "job_cluster_key": "ship2ship_cluster",
            "notebook_task": {
                "notebook_path": f"02_Data Ingestion",
                "base_parameters": {
                    "holdout days": "90"
                }
            },
            "task_key": "ship2ship_02",
            "depends_on": [
                {
                    "task_key": "ship2ship_01"
                }
            ]
        },
        {
            "job_cluster_key": "ship2ship_cluster",
            "notebook_task": {
                "notebook_path": f"03a_Overlap Detection"
            },
            "task_key": "ship2ship_03a",
            "depends_on": [
                {
                    "task_key": "ship2ship_02"
                }
            ]
        },
        {
            "job_cluster_key": "ship2ship_cluster",
            "notebook_task": {
                "notebook_path": f"03b_Advanced Overlap Detection"
            },
            "task_key": "ship2ship_03b",
            "depends_on": [
                {
                    "task_key": "ship2ship_02"
                }
            ]
        }
    ],
        "job_clusters": [
            {
                "job_cluster_key": "ship2ship_cluster",
                "new_cluster": {
                    "spark_version": "10.4.x-cpu-ml-scala2.12",
                "spark_conf": {
                    "spark.databricks.delta.formatCheck.enabled": "false"
                    },
                    "num_workers": 8,
                    "node_type_id": {"AWS": "i3.xlarge", "MSA": "Standard_D3_v2", "GCP": "n1-highmem-4"},
                    "custom_tags": {
                        "usage": "solacc_testing"
                    },
                }
            }
        ]
    }

# COMMAND ----------

dbutils.widgets.dropdown("run_job", "False", ["True", "False"])
run_job = dbutils.widgets.get("run_job") == "True"
NotebookSolutionCompanion().deploy_compute(job_json, run_job=run_job)

# COMMAND ----------


