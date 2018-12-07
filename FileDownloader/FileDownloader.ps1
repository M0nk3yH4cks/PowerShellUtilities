$links = Get-Content -Path ".\url.list"
$destination = ".\FileDownloader"

Foreach ($link in $links)
{

$filename = [System.Net.WebRequest]::Create($link).GetResponse()
$basename = Split-Path($filename.ResponseUri.OriginalString) -leaf
$filename.Close()
$output = Join-Path $destination $basename

Invoke-WebRequest -URI $filename.ResponseUri -Outfile $output
}