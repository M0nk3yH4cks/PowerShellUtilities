# PowerShell Utilities

A set of utilities written for the PowerShell to work on Windows just a little faster.

## File Renamer
### What is ?
A PowerShell script to rename easily large amount of files.
### How to use ?
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