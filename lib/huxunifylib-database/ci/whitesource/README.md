## Whitesource Scan Pipeline

A Codefresh pipeline will run for a project with multiple Git events:
  - PR Creation
  - Merge to mainline branch

The Codefresh pipeline will have a separate trigger configred for each of these events. In the case of a monorepo, Modified Files Glob should also be set to trigger based on changed files in the monorepo directory.

### PR Creation
When a PR is created, the pipeline will perform all steps to run a Whitesoure scan and save the results to a JSON file named scan_results.json. A custom step will follow that will parse the standard JSON file and extract the summary values. The summary report will be commented to the PR to provide visibility to developers and detail:
  - Package vulnerability assessments
  - Remediation tips
  - Links to CVE details
  - Outdated package list and used versions
  - Current package versions for comparison

The PR comment posts Whitesource scan summaries in order to bring security to the developer instead of making them track down the report in the WHitesource UI, increasing visibility to third party packages that need updates. Work to update can be planned and high vulnerabilities can be addressed more quickly with this report attached to code that is under review.

### Merge to mainline branch
A merge to mainline branches such as `dev` and `main` require another Whitesource scan as this is merged code. The `main` branch should be considered shippable code and a report is run for this Git event. However, a JSON file output is not required here, so the pipeline simply runs the scan to update the Whitesource UI and stops.

### Codefresh Pipeline YAML
To enable a Whitesoure scan, a single pipeline yaml file is all that is required to be added to a project directory for a monorepo or to a project repository. The Codefresh yaml will have a step that creates the pre-requisite files that are needed by the Whitesource scanner. Instead of maintaining these supplemental files in the repository, they are generated with each pipeline run and stored temporarily in the build enviornment.

Whitesource Unified Agent documentation can be found here: https://whitesource.atlassian.net/wiki/spaces/WD/pages/1544880156/Unified+Agent+Configuration+Parameters.
There are several programming language specific settings, but most have a default value and if the default is acceptable there is no need to provide it in the agent configuration. 

Changes to Whtesource agent configs can be managed directly to the Codefresh pipeline. 

The agent needs specific settings for a programming language so there will be a template Codefresh file for each one.

### Required Variables
Two variable that is not in the pipeline YAML but are required is `API_KEY` and `USER_KEY`. The API_KEY allows the scan results to be sent to the Deloitte hosted Whitesource UI. The USER_KEY is required in order to generate scan results to a JSON file. Both variables are set as a `Shared Configuration` in the Codefresh UI.

### JSON Parse Script
The Whitesource pipeline checks out two repositories. One for the application code and `codefresh-pipelines` which has the script `parse-json-report.sh`. The parse script uses jq to extract values in the JSON output and create a markdown file that is added to the PR as a Git comment.
