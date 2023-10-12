& ./package

$parent_folder_path = "${env:USERPROFILE}/bear-warehouse/tool-homemade/bear_python_demo"
$folder_path = "${parent_folder_path}/package"
Write-Output "Deleting ${folder_path} ..."
if (Test-Path $folder_path) {
    Remove-Item -Path "$folder_path" -Force -Recurse -Confirm:$false
}
Write-Output `n

Write-Output "Copying packages to ${parent_folder_path} ..."
copy-item "package" "${parent_folder_path}" -force -recurse
Write-Output `n

Invoke-Item "${parent_folder_path}"