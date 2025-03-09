function Show-Tree {
    param (
        [string]$path,
        [string[]]$exclude,
        [int]$level = 0
    )

    # 获取当前目录下的文件和文件夹
    $items = Get-ChildItem -Path $path

    foreach ($item in $items) {
        # 如果当前项是目录且不在排除列表中
        if ($item.PSIsContainer -and $exclude -notcontains $item.Name) {
            # 输出树状图的前缀
            Write-Host (" " * $level + "├── " + $item.Name)
            # 递归调用，进入子目录
            Show-Tree -path $item.FullName -exclude $exclude -level ($level + 1)
        }
        elseif (-not $item.PSIsContainer) {
            # 输出文件
            Write-Host (" " * $level + "├── " + $item.Name)
        }
    }
}

# 调用函数，排除 .idea, .venv, __pycache__
Show-Tree -path "D:\AIChessGame" -exclude @(".idea", ".venv", "__pycache__")
