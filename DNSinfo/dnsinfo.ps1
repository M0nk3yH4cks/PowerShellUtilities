param([String] $command, [String] $argm)
Function getInternalDNS {
    $wmi = Invoke-WebRequest https://whatismyipaddress.com/
    $publicIp = $wmi.ParsedHTML.getElementById("ipv4") | ForEach-Object InnerText
    $internalDNS = nslookup.exe $publicIp | Select-String Server 

    Write-Host "DNS: $internalDNS"
}

function getPublicIP {
    $wmi = Invoke-WebRequest https://whatismyipaddress.com/
    $publicIp = $wmi.ParsedHTML.getElementById("ipv4") | ForEach-Object InnerText

    Write-Host "Public IP: $publicIp"
}

function dnsInfo {
    $nsOut = nslookup -type=ns $argm

    for ($i = 3; $i -lt $nsOut.Count; $i++) {
        Write-Host "DNS Server: $($nsOut[$i].split("=")[1].trim(" "))"
        Write-Host "Server Address: $((nslookup $argm $($nsOut[$i].split("=")[1].trim(" ")))[1].split(":")[1].trim(" "))
        "
    }
}

function printHelp {
    Write-Host "    Help
    ---------------------------------------------
    idns           Get the current internal DNS
    ip             Get the current public IP
    edns           ------------------------------
                   url          www.google.it
                   ------------------------------
                   "
}

if (!$command) {
    printHelp
}else{
    switch ($command) {
        "idns" { getInternalDNS }
        "ip"   { getPublicIP }
        "edns" { dnsInfo }
        Default { printHelp }
    }
}