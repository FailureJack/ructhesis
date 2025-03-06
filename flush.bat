@echo off
rem 定义要删除的文件扩展名列表
set "extensions=aux log out bbl blg toc lof lot idx ilg ind synctex.gz bcf fls fdb_latexmk run.xml"

rem 遍历每个扩展名
for %%e in (%extensions%) do (
    rem 递归删除当前目录及其子目录下所有指定扩展名的文件
    for /r %%f in (*.%%e) do (
        del "%%f"
        if %errorlevel% equ 0 (
            echo Deleted: %%f
        ) else (
            echo Failed to delete: %%f
        )
    )
)

echo All LaTeX cache files have been deleted.
pause