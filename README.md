# Hux-Unified-Solution
Repository for Hux Unified Solution

# Add pre-commit git hooks

Steps

1. Install pre-commit:`pip install pre-commit` in a virtualenv.
2. Define `.pre-commit-config.yaml` with the hooks you want to include. If you already have it, you can skip this step.
3. Execute `pre-commit install` to install git hooks in your `.git/hooks` directory.

Note: In case there are changes in the `.pre-commit-config.yaml`, it is a good idea to run `pre-commit clean`.

Every time you try to commit, checks in the pre-commit hook will run and you will not be allowed to commit if there are any errors.
You can also run `pre-commit run` to make sure there are no errors before comitting your code.

For more info, refer https://pre-commit.com/.
