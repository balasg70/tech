# Documentation of the Bitbucket for admins

Executing commands:

To get respository in projects owned by you and assigned to you

python bitbucket.py -u username -p password my_issues

To get repository in a specific project

python bitbucket.py -u username -p password my_issues:project_name

To get respository in projects owned by somebody else

python bitbucket.py -u username -p password -o someone_else my_issues
