param([String] $command, [String] $argm, [String] $prop)
$ErrorActionPreference = "Stop"
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
    if(!$argm -or $argm -ne "url"){
        printHelp
    }else{
        $nsOut = nslookup -type=ns $prop

        for ($i = 3; $i -lt $nsOut.Count; $i++) {
            Write-Host "DNS Server: $($nsOut[$i].split("=")[1].trim(" "))"
            Write-Host "Server Address: $((nslookup $prop $($nsOut[$i].split("=")[1].trim(" ")))[1].split(":")[1].trim(" "))
            "
        }
    }
}

function localDNS {
    if(!$argm -or $argm -ne "url" -and $argm -ne "flush"){
        printHelp
    }else{
        if ($argm -eq "url") {
            if (!$prop) {
                Write-Error -Message "Insert a valid domain"
            }
            $result = Get-DnsClientCache -Name $prop -erroraction 'silentlycontinue'
            if(!$result){
                Write-Host "No occurences found"
            }else{
                Get-DnsClientCache -Name $prop
            }
        }else{
            Clear-DnsClientCache
            Write-Host "Cache cleaned !!!"
        }
    }
}

function printHelp {
    Write-Host "    Help
    --------------------------------------------------
    idns           Get the current internal DNS
    ip             Get the current public IP
    edns           -----------------------------------
                   url          www.google.it
                   -----------------------------------
    ldns           -----------------------------------
                   url          Check specific domain
                   flush        Clear cached data
                   -----------------------------------"
}

if (!$command) {
    printHelp
}else{
    switch ($command) {
        "idns" { getInternalDNS }
        "ip"   { getPublicIP }
        "edns" { dnsInfo }
        "ldns" { localDNS }
        Default { printHelp }
    }
}