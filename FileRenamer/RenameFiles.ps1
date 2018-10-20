$ErrorActionPreference = "Stop"
# Var Declaration
$oldNamesFilePath = ".\FileRenamer\oldNames.txt"
$newNamesFilePath = ".\FileRenamer\newNames.txt"
$filePath = "FileRenamer\Files"

# Set the encoding to UTF-8 to handle all the charters
$OutputEncoding = [console]::InputEncoding = [console]::OutputEncoding = New-Object System.Text.UTF8Encoding

########################################
########################################
# Assign the list of old names to a file
$oldNames = ([IO.File]::ReadAllLines($oldNamesFilePath))

# Assign the list of new names to a file
$newNames = ([IO.File]::ReadAllLines($newNamesFilePath))

# Verify the imported file
$countOld = $oldNames.split("`n").count
$countNew = $newNames.split("`n").count
Write-Output "Imported $countOld old names"
Write-Output "Imported $countNew new names"

if ($countOld -ne $countNew) {
    Write-Error -Message "File lines are not equal" -Category "Malformed File" -RecommendedAction "Review input files"
}

################
# Do The Magic #
################

# Go to the directory that contains the files
Set-Location $filePath    

# For every element contained in the old names list, 
# change its name according to the new names list corresponding element
for ($i = 0; $i -lt $oldNames.Count; $i++) {
    Move-Item $oldNames[$i] $newNames[$i]
    Write-Output "Renamed $oldNames[$i]"
}