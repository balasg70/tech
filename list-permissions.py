#!/usr/bin/env python3
# 
# 
#

import kopano
from kopano.defs import RIGHT_NAME, EID_EVERYONE
from MAPI.Util import *
import sys
import binascii
from tabulate import tabulate
if sys.version_info <= (3, 0):
    print('Script is only working with python 3 ')
    sys.exit(1)

ecRightsNone = 0x00000000
ecRightsReadAny = 0x00000001
ecRightsCreate = 0x00000002
ecRightsEditOwned = 0x00000008
ecRightsDeleteOwned = 0x00000010
ecRightsEditAny = 0x00000020
ecRightsDeleteAny = 0x00000040
ecRightsCreateSubfolder = 0x00000080
ecRightsFolderAccess = 0x00000100
ecRightsFolderVisible = 0x00000400

ecRightsFullControl = 0x000004FB

ecRightsTemplateNoRights = ecRightsFolderVisible
ecRightsTemplateReadOnly = ecRightsTemplateNoRights | ecRightsReadAny
ecRightsTemplateSecretary = ecRightsTemplateReadOnly | ecRightsCreate | ecRightsEditOwned | ecRightsDeleteOwned | ecRightsEditAny | ecRightsDeleteAny
ecRightsTemplateOwner = ecRightsTemplateSecretary | ecRightsCreateSubfolder | ecRightsFolderAccess
EMS_AB_ADDRESS_LOOKUP = 0x1


def opt_args():
    parser = kopano.parser('skpcfUP')
    parser.add_option("--user", dest="user", action="store", help="Run script for user ")
    parser.add_option("--list", dest="printrules", action="store_true", help="Print rules")
    parser.add_option("--list-all", dest="printrulesall", action="store_true", help="Print rules including the 'hidden' folders")
return parser.parse_args()

def listpermissions(user, options):
    tabledelagate_header = ["User","See private items", "Send copy"]
    tabledelagate_data = []
    #delegate info
    delnames = getdelegateuser(user)

    for deluser in delnames['users']:

        try:
            if delnames['users'][deluser]['delegate']:
                delegate = u"\u2713"
        except:
            delegate = u"\u2717"

        if delnames['users'][deluser].get('private'):
            private = u"\u2713"
        else:
            private =u"\u2717"

        if delegate or private:
            tabledelagate_data.append([delnames['users'][deluser]['name'], private, delegate])

    #acl rules
    table_header = ["Folder", "Fullcontroll", "Owner", "Secretary", "Readonly", "No rights", "Other"]
    tableacl_data =[]

    store = user.store
    if not options.folders:
        perfolder = getpermissions(store)
        tableacl_data.append(['Store', '\n'.join(perfolder['Full control']), '\n'.join(perfolder['Owner']),
                           '\n'.join(perfolder['Secretary']),
                           '\n'.join(perfolder['Readonly']), '\n'.join(perfolder['No rights']),
                           '\n'.join(perfolder['Other'])])
    if options.printrulesall:
        folders = store.root.folders()
    else:
        folders = store.folders()

    for folder in folders:
        perfolder = getpermissions(folder)
        folderindent = ''
        if folder.path:
            for i in range(0, len(folder.path.split('/')) - 1):
                folderindent += '-'

        foldername = '%s %s ' % (folderindent, folder.name)
        tableacl_data.append([foldername, '\n'.join(perfolder['Full control']), '\n'.join(perfolder['Owner']),
                           '\n'.join(perfolder['Secretary']),
                           '\n'.join(perfolder['Readonly']), '\n'.join(perfolder['No rights']),
                           '\n'.join(perfolder['Other'])])


    print('Store information {}'.format(user.name))
    if len(tabledelagate_data) > 0:
        print('Delegate information:')
        print(tabulate(tabledelagate_data, headers=tabledelagate_header, tablefmt="grid", stralign="center"))

    print('Folder permissions:')
    print(tabulate(tableacl_data, headers=table_header, tablefmt="grid"))


def main():
    options, args = opt_args()

    if options.calc:
        calculatepermissions()
        sys.exit(0)

    if not options.user:
        print('please use:  %s --user <username>'.format(sys.argv[0]))
        sys.exit(1)

    server = kopano.Server(options)
    user = server.user(options.user)

    if options.printrules or options.printrulesall:
        listpermissions(user, options)
        sys.exit(0)

if __name__ == "__main__":
    main()
