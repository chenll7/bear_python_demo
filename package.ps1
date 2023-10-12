$folder_path = 'package'
if (Test-Path $folder_path) {
    Remove-Item -Path "$folder_path" -Force -Recurse -Confirm:$false
}

$folder_path = 'build'
if (Test-Path $folder_path) {
    Remove-Item -Path "$folder_path" -Force -Recurse -Confirm:$false
}

Write-Output 'Donwloading dependencies...'
# $job1 = Start-Job -Init ([ScriptBlock]::Create("Set-Location '$pwd'")) -ScriptBlock {
    & "venv/Scripts/python" -m pip download -d package --disable-pip-version-check .
    Write-Output `n
# }
Write-Output 'Packaging...'
# $job2 = Start-Job -Init ([ScriptBlock]::Create("Set-Location '$pwd'")) -ScriptBlock {
    & "venv/Scripts/python" -m pip wheel -w package --disable-pip-version-check .
    Write-Output `n
# }
# Wait-Job $job1
# Wait-Job $job2
# Receive-Job -Job $job1
# Receive-Job -Job $job2
# remove-job $job1
# remove-job $job2