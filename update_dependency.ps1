$src_folder_path = '../../20230905-bear_python_components/bear_components'
$folder_path = "dependency"
Write-Output "Deleting folder ${folder_path} ..."
if (Test-Path $folder_path) {
    Remove-Item -Path "$folder_path" -Force -Recurse -Confirm:$false
}
Write-Output `n

Write-Output "Copying folder ${folder_path} to here ..."
copy-item "${src_folder_path}/package/" "dependency" -force -recurse
Write-Output `n