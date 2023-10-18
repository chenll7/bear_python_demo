$folder_path = 'package'
if (Test-Path $folder_path) {
    Remove-Item -Path "$folder_path" -Force -Recurse -Confirm:$false
}

$folder_path = 'build'
if (Test-Path $folder_path) {
    Remove-Item -Path "$folder_path" -Force -Recurse -Confirm:$false
}

Write-Output 'Packaging...'
py -m pip wheel -w package --no-index --find-links ./dependency --disable-pip-version-check .
Write-Output `n