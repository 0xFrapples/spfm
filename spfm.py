import os
import json

config = open('config.json')
configData = json.load(config)
showHiddenFiles = configData['showHiddenFiles']
rootIgnore = configData['rootIgnore']
passConfirm = configData['passConfirm'] # When true, performs some commands without confirmation
searchKey = ""
# Home directory output
if os.getuid() == 0:
    currentDir = "/root"
    parentDirs = ['/']
else:
    currentDir = f"/home/{os.getlogin()}"
    parentDirs = ['/', '/home/']

# Directory open function
def openDirectory(searchKey):
    global directory
    directory = os.listdir(currentDir)
    directory.sort()
    os.system('clear')
    if os.getuid() == 0 and rootIgnore == False:
        print("Warning: running as root.")
    
    if searchKey == "":
        print(currentDir)
    else:
        print(f'{currentDir} | Searching results for: "{searchKey}"')

    # Separator
    if len(currentDir) > 10:
        sep = "-"*len(currentDir)
    else:
        sep = "-"*10
    print(sep)
    
    ## Prints all files (if not hidden) in a current directory 
    a = 0

    while a < len(directory):
        if showHiddenFiles == False and directory[a].startswith('.') or searchKey not in directory[a] or os.access(f'{currentDir}/{directory[a]}', os.R_OK) == False and os.getuid() != 0:
            pass
        elif os.path.isfile(f'{currentDir}/{directory[a]}') == True:
            print(f'FILE | {directory[a]}')
        else:
            print(f'DIR  | {directory[a]}')
        a += 1
    
    if currentDir != '/':
        print('DIR  | ..')
    print(sep)

openDirectory(searchKey)

# File manager commands
def comingSoon():
    print("Coming soon."); input()

# Directory prompt loop
while True:
    try:
        reqInput = input()
        searchKey = ""
    except KeyboardInterrupt:
        os.system('clear')
        exit()

    if reqInput.startswith('//'):
        try:
            if reqInput == '//' or reqInput == '//help':
                print("List of commands: \n//help - Show this menu \n//mv - Move a file/directory to a directory \n//del - Delete a file or directory \n//rename - Rename a file/directory \n//open - Open a file \n//find - Find files/directories matching a given prompt (case sensitive!) \n//dotfiles = Toggle dotfiles (hidden files/directories), doesn't affect the config file"); input("Press enter to continue..")
            elif reqInput == '//mv':
                comingSoon()
            elif reqInput == '//del':
                comingSoon()
            elif reqInput == '//rename':
                while True:
                    try:
                        r1 = input("Choose a file/directory you want to rename: ")
                        if r1 in directory:
                            r2 = input("Choose a new name: ")
                            os.system(f'cd {currentDir} && cp {r1} {r2} && rm -rf {r1}')
                            break
                    except KeyboardInterrupt:
                        break
            elif reqInput == '//open':
                open()
            elif reqInput == '//find':
                searchKey = input("Find: ")
            elif reqInput == '//dotfiles':
                if showHiddenFiles == True:
                    showHiddenFiles = False
                else:
                    showHiddenFiles = True
            else:
                pass
        except KeyboardInterrupt:
            pass
    elif os.access(f'{currentDir}/{reqInput}', os.R_OK) == False and os.getuid() != 0:
        pass
    elif '//' in reqInput or os.path.isfile(reqInput) == False \
        and os.path.isdir(reqInput) == False and reqInput.startswith('/') \
        or reqInput == '..' and currentDir == '/' :
        pass
    elif reqInput == '..':
        currentDir = parentDirs[-1]
    elif reqInput == '/' or reqInput.startswith('/'):
        currentDir = reqInput
    elif reqInput == '.' or reqInput == '' \
        or os.path.isfile(f'{currentDir}/{reqInput}') == False and os.path.isdir(f'{currentDir}/{reqInput}') == False:
        pass
    elif currentDir != '/':
        currentDir += (f'/{reqInput}')
    else:
        currentDir = (f'/{reqInput}')

    if currentDir.endswith('/') and currentDir != '/':
        currentDir = currentDir[:-1]
        

    # Parent directory logging
    n = 0; k = 0; symb = []; parentDirs = []; out = ''
    while n < len(currentDir)-1:
        if currentDir == '/':
            pass
        else:
            if currentDir[n] == '/':
                symb.append("/")
            
                if parentDirs:
                    out = parentDirs[-1]
                while k < len(symb)-1:
                    out += symb[k]
                    k += 1
                out += "/"
                k = 0
                parentDirs += [out]
                out = ''
                symb = []
            else:
                symb.append(currentDir[n])
        n += 1
    openDirectory(searchKey)