# CS4485
Reminder to create a new branch with the task name (ex: backend-5-jy) <br>
Delete your branch after you merge changes <br>
Make sure to git checkout (branch-name) when you work on code <br>

If changes have been pushed to main and you haven't updated your branch with the current changes: <br>
git checkout main <br>
git pull <br>
git checkout (your-branch) <br>
git merge main <br>
Then resolve your conflicts within vscode

To run the application: <br>
Make sure you have python installed <br>
Either create a virtual environment and use pip to install the packages, or install the packages to your current environment <br>
Change directory to project directory and run "flask --app "app" run" <br>
