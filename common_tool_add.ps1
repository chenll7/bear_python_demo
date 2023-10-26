$package_name = "bear_python_demo"
$input_content = Read-Host -Prompt "Delete ${package_name}/common_tool ? [N/y]"

if($input_content -eq 'y'){
    remove-item -Path "${package_name}/common_tool" -Force -Recurse
    & git subtree add "--prefix=${package_name}/common_tool" common_tool master --squash
}

