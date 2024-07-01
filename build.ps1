$exclude = @("venv", "automacao_ponto_sms.zip")
$files = Get-ChildItem -Path . -Exclude $exclude
Compress-Archive -Path $files -DestinationPath "automacao_ponto_sms.zip" -Force