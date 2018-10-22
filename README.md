# PowerShell Utilities

A set of utilities written for the PowerShell to work on Windows just a little faster.

## File Renamer
### What is ?
A PowerShell script to rename easily large amount of files.
### How to use 
In the **head** of the `FileRenamer.ps1` there are three variables.
- `$oldNamesFilePath` : Path to the file that contains the file names that you want to change
- `$newNamesFilePath` : Path to the file that contains the new names for your files 
- `$filePath` : Path to the folder that contains the files that you want to rename

Cloning the repository you can run the example, otherwise you can modify the variables in this way :
```powershell
$oldNamesFilePath = "C:\PathToTheFile\WithOldNames.txt"
$newNamesFilePath = "C:\PathToTheFile\WithNewNames.txt"
$filePath = "C:\PathToTheFolder\WithFilesToRename\"
```
## FileDownloader
### What is ?
PowerShell script to download multiple files.
### How to use 
There are two variables that you can set:
1. `$links` : The path to the file that contain the list of urls to download.
2. `$destination` : The path to the folder where you want to store the downloaded data
```powershell
$links = Get-Content -Path "C:\PathToTheListFile"
$destination = "C:\PathToDestinationFolder"
```
### Invoke-WebRequest
**Get an HTML page**
```powershell
Invoke-WebRequest -OutFile index.html http://example.com
```
**Get a file**
```powershell
Invoke-WebRequest -OutFile image.png http://example.com/file.png
```
## DNSinfo
### What is ?
Multi tool to know the name of DNS used for a specific domain.
### How to use
.\dnsinfo.ps1 `<command>` `<arg>`

**Manual**
| Command  | Description | Arg | Description |
| ------------- | :-------------: | :-------------: | -------------: |
| idns  | Show the current internal DNS which the PC is running  |   |   |
| ip  | Get the current public IP  |   |   |
| edns  | Get the authoritative DNS for a domain  | url  | The domain that you want to verify |