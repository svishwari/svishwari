## Files related to Whitesource scan for huxunifylib

### wss-agent.config
- Whitesource agent with configurations for Python. The full wss-agent.config is quite large with all supported language settings commented out. 
- Since a high percentage of the standard file is unnecessary, it has been streamlined with the settings for just Python. Still, many of these settings are defaults and are not needed in the actual file. They are in place as a way to document the default settings.

### wss-install-commands.sh
- The intended use of this file is to set up the environment before the scan and maintain commands in this script. This is one place where various pip installs could take place, or any other pre-requisite needs prior to running the scan jar file. 
- The other option is to put the pre-requisite steps in the Codefresh pipeline YAML. In previous testing, there was more success with preparing the environment in the pipeline rather than this file. It is easier to test as well, since pipeline YAML can be changed inline rather than updating the script file, committing, then running the scan.

### codefresh-ws-scan.yaml
- Codefresh pipeline that will run the scan on commit to a mainline branch. 
- There is the variable CF_BRANCH that will be set as `develop` or `main` based on the pipeline trigger which will be set run on on Push Commits to either of those branches. 
- Since we are trying to make the pipeline runs dynamic to the merged branch name, the Whitesource scanner config settings `projectVersion` are set with each pipeline run and not maintained in separate files.
- One variable that is not in the pipeline YAML but is required is `API_KEY`, which allows the scan results to be sent to the Deloitte hosted Whitesource UI. The variable is set as a Shared Configuration in the Codefresh UI.
