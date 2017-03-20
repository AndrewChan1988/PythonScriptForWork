@echo off &setlocal enabledelayedexpansion

rem ==============================================================
rem  邮件发送脚本，需带有EmailSend.exe工具
rem ==============================================================

call D:\SendEmail\Config\Email_config.bat
rem 项目名
set prj_name=F302

rem 每次抄送收件人列表
call D:\SendEmail\Config\CarbonCopy.bat
rem 分支
set Pro_Branch=mt6737_dev

rem hudson add
set Hudson_Address=http://10.250.115.25:8881/hudson/view/F302/

rem 成功时发送的邮件主题
set mailsubject_true=%prj_name%项目版本集成成功通知
rem 失败时发送的邮件主题
set mailsubject_false=%prj_name%项目%Pro_Branch% 集成失败，请确认是否您的活动导致。

rem 邮件后缀
set mailfrom=@itel-mobile.com

rem 邮件正文
set mailbody=mailbody.txt
echo MailBody=尊敬的> %mailbody%
>%mailbody% set/p=MailBody=尊敬的<nul

rem 版本包所在目录
set version_dir=\\10.250.115.52\itel_Test_Version\MTK6737\F302\Dev_Version

rem 发送的附件，加上文件名不得多余4层,如果不需要附件，直接为空
set attach=ReleaseNotes\CR_List_diff.txt

rem 检查更新的日志文件位置
set history_path=ReleaseNotes\maillist.txt

rem false表示只有失败才发送；true表示失败和成功都发送。
set send_flag=false

echo ========================================================================================================
rem =取出最新的编译包名称以及判断成功失败标志================================================================
rem 上一次发送的版本包的记录
if not exist version_old.txt (
	echo first-build>version_old.txt
)
for /f  "delims=" %%a in (version_old.txt) do (
	set old_version=%%a
)
rem 取出当前最新的版本包
dir /ad /b /w /od %version_dir%>version_dir.txt
for /f "delims=" %%a in (version_dir.txt) do (
	if NOT "%%a" == "dyfeature" (
	    set newest_version=%%a
	)
)

echo 最新的版本包：%version_dir%\%newest_version%

for /f "tokens=1-3 delims=_" %%a in ('echo %newest_version%') do (
        echo "%%c"
	if "%%c" == "fail" (
		set version_flag=false
		echo 最新的版本包：编译失败
	) else (
		if "%send_flag%" == "false" (
			echo 最新的版本包,编译成功,不需发送邮件！
			exit 0
		)
		set version_flag=true
		echo 最新的版本包：编译成功
	)
)
rem 判断是否发送过
if "%newest_version%" == "%old_version%" (
	echo %newest_version%该版本已发送过！
	exit 1
) else (
	echo %newest_version%>version_old.txt
)
rem ===========================================================================================================

rem 以下开始是配置文件EmailInfo.ini的描述
echo [EmailInfo]>EmailInfo.ini
echo MailServer=smtp.qiye.163.com>>EmailInfo.ini
echo MailPort=25>>EmailInfo.ini
echo CredentialType=1 >>EmailInfo.ini
echo //发件人账号>>EmailInfo.ini
echo MailFrom=%MailAccount%>>EmailInfo.ini
echo //发件人账号密码>>EmailInfo.ini
setlocal disabledelayedexpansion
echo MailPassword=%MailPassword%>>EmailInfo.ini
setlocal enabledelayedexpansion
echo //邮件主题>>EmailInfo.ini
if "%version_flag%" == "true" (
	echo MailSubject=%mailsubject_true%: %newest_version%>>EmailInfo.ini
)
if "%version_flag%" == "false" (
	echo MailSubject=%mailsubject_false%: %newest_version%>>EmailInfo.ini
)

rem =活动提交人,收件人列表=============================================================================================
set mailtonumber=0

echo 检查文件：%version_dir%\%newest_version%\%history_path%
if exist name_all.txt del name_all.txt
rem for /f "tokens=1 delims= " %%a in (%version_dir%\%newest_version%\%history_path%) do (
    for /f %%a in (%version_dir%\%newest_version%\%history_path%) do (
	set name=%%a
	if not "!name!" == "" (
		if not "!name!" == "file" (
			if not "!name!" == "directory" (
				set name_c=!name!
				echo !name_c!>>name_all.txt
			)
		)
	)	
)

echo ---------活动提交人员---------
type name_all.txt
echo ------------------------------
rem for /f "delims=" %%i in (name_all.txt) do (
rem         findstr /c:"%%i" name.txt >nul||echo %%i>>name.txt
rem )

    for /f "tokens=1 delims=@" %%i in (%version_dir%\%newest_version%\%history_path%) do (
	set name=%%i
	if not "!name!" == "" (
		if not "!name!" == "file" (
			if not "!name!" == "directory" (
				set name_c=!name!
				echo !name_c!>>name.txt
rem				echo !name_c!>>%mailbody%
				>>%mailbody% set /p=!name_c!;<nul
			)
		)
	)	
    )

echo ---------邮件接收人员---------
type name.txt 
echo ------------------------------

echo //邮件正文>>EmailInfo.ini
>>%mailbody% set /p="<br>你好，您提交的活动（详见附件）可能导致编译报错，请火速处理。<br>版本获取路径:<a href="%version_dir%\%newest_version%">%version_dir%\%newest_version%</a> <br>Hudson Address : %Hudson_Address%<br>"<nul 
type %mailbody%>>EmailInfo.ini
echo 谢谢! >>EmailInfo.ini

echo ---------邮件抄送人员---------
echo %mailcc%
echo ------------------------------

for /f "delims=" %%i in (name_all.txt) do (
        set /a mailtonumber=!mailtonumber!+1
)

rem ------------------------------
echo //收件人列表>>EmailInfo.ini
echo [MailTo]%>>EmailInfo.ini
echo MailToNumber=%mailtonumber% >>EmailInfo.ini

set count=0
for /f "tokens=1 delims= " %%a in (name_all.txt) do (
	set /a count=!count!+1
	echo MailTo!count!=%%a >>EmailInfo.ini
)
rem ------------------------------
rem ========================================================================================================


rem =抄送人列表=================================================================================================
set mailccnumber=0
for %%a in (%mailcc%) do (
        set /a mailccnumber=!mailccnumber!+1
)
echo //抄送收件人列表>>EmailInfo.ini
echo [MailCC]>>EmailInfo.ini
echo MailCCNumber=%mailccnumber% >>EmailInfo.ini
set /a count=0
for %%a in (%mailcc%) do (
	set /a count=!count!+1
        echo MailCC!count!=%%a%mailfrom% >>EmailInfo.ini
)
rem ========================================================================================================


rem =发送附件列表===========================================================================================
set attachnumber=0
for %%a in (%attach%) do (
        set /a attachnumber=!attachnumber!+1
)

echo //附件列表>>EmailInfo.ini
echo [Attach]>>EmailInfo.ini
echo AttachNumber=%attachnumber% >>EmailInfo.ini
rem echo Attach1=%version_dir%\%newest_version%\%attach%>>EmailInfo.ini
set count=0
for %%a in (%attach%) do (
        set /a count=!count!+1
        for /f "tokens=1,2,3,4 delims=\" %%e in ("%%a") do (
		if not "%%h" == "" (
			for /f "tokens=1" %%i in ('dir /b %version_dir%\%newest_version%\%%a*') do (
       				echo Attach!count!=%version_dir%\%newest_version%\%%e\%%f\%%g\%%i>>EmailInfo.ini		
       			)
		) else (
			if not "%%g" == "" (
				for /f "tokens=1" %%i in ('dir /b %version_dir%\%newest_version%\%%a*') do (
       					echo Attach!count!=%version_dir%\%newest_version%\%%e\%%f\%%i>>EmailInfo.ini   			
       				)	
			) else (
				if not "%%f" == "" (
					for /f "tokens=1" %%i in ('dir /b %version_dir%\%newest_version%\%%a*') do (
       						echo Attach!count!=%version_dir%\%newest_version%\%%e\%%i>>EmailInfo.ini   			
       					)	
				) else (
					for /f "tokens=1" %%i in ('dir /b %version_dir%\%newest_version%\%%a*') do (
       						echo Attach!count!=%version_dir%\%newest_version%\%%i>>EmailInfo.ini   			
       					)
				)
			)
		)
       	)
)
rem ========================================================================================================
echo =====================
echo 正在发送邮件......
EmailSend.exe
echo =====================
if exist name.txt del name.txt
if exist version_dir.txt del version_dir.txt
if exist name_all.txt del name_all.txt
echo ========================================================================================================

