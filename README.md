# Documentation of the Bitbucket for admins

Dependencies
kopano-rules depends on a few Python libraries:

python3-kopano

tabulate

binascii


Executing commands:

To get respository in projects owned by you and assigned to you

python bitbuckettool.py -u username -p password my_perm

To get repository in a specific project

python bitbuckettool.py -u username -p password my_perm:project_name

To get respository in projects owned by somebody else

python bitbuckettool.py -u username -p password -o someone_else my_perm

To list permissions for users

python list-permissions.py --user <username> --list
