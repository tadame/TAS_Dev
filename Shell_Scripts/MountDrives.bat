rem Example file to mount files in Windows at startup
if exist j:\ (
    net use j: /delete
)
ECHO Mounting J drive
net use j: \\resourceA\folderA

if exist s:\ (
    net use s: /delete
)
ECHO Mounting S drive
net use s: \\resourceB\folderB
pause
