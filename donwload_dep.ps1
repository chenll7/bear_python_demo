$folder_path = 'dependency'
if (Test-Path $folder_path) {
    Remove-Item -Path "$folder_path" -Force -Recurse -Confirm:$false
}

& py -m pip download -d "$folder_path" --disable-pip-version-check setuptools

& py -m pip download -d "$folder_path" --disable-pip-version-check setuptools-scm

& py -m pip download -d "$folder_path" --disable-pip-version-check wheel

& py -m pip download -d "$folder_path" --disable-pip-version-check .