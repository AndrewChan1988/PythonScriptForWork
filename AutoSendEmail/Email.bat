@echo off &setlocal enabledelayedexpansion

rem ==============================================================
rem  �ʼ����ͽű��������EmailSend.exe����
rem ==============================================================

call D:\SendEmail\Config\Email_config.bat
rem ��Ŀ��
set prj_name=F302

rem ÿ�γ����ռ����б�
call D:\SendEmail\Config\CarbonCopy.bat
rem ��֧
set Pro_Branch=mt6737_dev

rem hudson add
set Hudson_Address=http://10.250.115.25:8881/hudson/view/F302/

rem �ɹ�ʱ���͵��ʼ�����
set mailsubject_true=%prj_name%��Ŀ�汾���ɳɹ�֪ͨ
rem ʧ��ʱ���͵��ʼ�����
set mailsubject_false=%prj_name%��Ŀ%Pro_Branch% ����ʧ�ܣ���ȷ���Ƿ����Ļ���¡�

rem �ʼ���׺
set mailfrom=@itel-mobile.com

rem �ʼ�����
set mailbody=mailbody.txt
echo MailBody=�𾴵�> %mailbody%
>%mailbody% set/p=MailBody=�𾴵�<nul

rem �汾������Ŀ¼
set version_dir=\\10.250.115.52\itel_Test_Version\MTK6737\F302\Dev_Version

rem ���͵ĸ����������ļ������ö���4��,�������Ҫ������ֱ��Ϊ��
set attach=ReleaseNotes\CR_List_diff.txt

rem �����µ���־�ļ�λ��
set history_path=ReleaseNotes\maillist.txt

rem false��ʾֻ��ʧ�ܲŷ��ͣ�true��ʾʧ�ܺͳɹ������͡�
set send_flag=false

echo ========================================================================================================
rem =ȡ�����µı���������Լ��жϳɹ�ʧ�ܱ�־================================================================
rem ��һ�η��͵İ汾���ļ�¼
if not exist version_old.txt (
	echo first-build>version_old.txt
)
for /f  "delims=" %%a in (version_old.txt) do (
	set old_version=%%a
)
rem ȡ����ǰ���µİ汾��
dir /ad /b /w /od %version_dir%>version_dir.txt
for /f "delims=" %%a in (version_dir.txt) do (
	if NOT "%%a" == "dyfeature" (
	    set newest_version=%%a
	)
)

echo ���µİ汾����%version_dir%\%newest_version%

for /f "tokens=1-3 delims=_" %%a in ('echo %newest_version%') do (
        echo "%%c"
	if "%%c" == "fail" (
		set version_flag=false
		echo ���µİ汾��������ʧ��
	) else (
		if "%send_flag%" == "false" (
			echo ���µİ汾��,����ɹ�,���跢���ʼ���
			exit 0
		)
		set version_flag=true
		echo ���µİ汾��������ɹ�
	)
)
rem �ж��Ƿ��͹�
if "%newest_version%" == "%old_version%" (
	echo %newest_version%�ð汾�ѷ��͹���
	exit 1
) else (
	echo %newest_version%>version_old.txt
)
rem ===========================================================================================================

rem ���¿�ʼ�������ļ�EmailInfo.ini������
echo [EmailInfo]>EmailInfo.ini
echo MailServer=smtp.qiye.163.com>>EmailInfo.ini
echo MailPort=25>>EmailInfo.ini
echo CredentialType=1 >>EmailInfo.ini
echo //�������˺�>>EmailInfo.ini
echo MailFrom=%MailAccount%>>EmailInfo.ini
echo //�������˺�����>>EmailInfo.ini
setlocal disabledelayedexpansion
echo MailPassword=%MailPassword%>>EmailInfo.ini
setlocal enabledelayedexpansion
echo //�ʼ�����>>EmailInfo.ini
if "%version_flag%" == "true" (
	echo MailSubject=%mailsubject_true%: %newest_version%>>EmailInfo.ini
)
if "%version_flag%" == "false" (
	echo MailSubject=%mailsubject_false%: %newest_version%>>EmailInfo.ini
)

rem =��ύ��,�ռ����б�=============================================================================================
set mailtonumber=0

echo ����ļ���%version_dir%\%newest_version%\%history_path%
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

echo ---------��ύ��Ա---------
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

echo ---------�ʼ�������Ա---------
type name.txt 
echo ------------------------------

echo //�ʼ�����>>EmailInfo.ini
>>%mailbody% set /p="<br>��ã����ύ�Ļ��������������ܵ��±��뱨������ٴ���<br>�汾��ȡ·��:<a href="%version_dir%\%newest_version%">%version_dir%\%newest_version%</a> <br>Hudson Address : %Hudson_Address%<br>"<nul 
type %mailbody%>>EmailInfo.ini
echo лл! >>EmailInfo.ini

echo ---------�ʼ�������Ա---------
echo %mailcc%
echo ------------------------------

for /f "delims=" %%i in (name_all.txt) do (
        set /a mailtonumber=!mailtonumber!+1
)

rem ------------------------------
echo //�ռ����б�>>EmailInfo.ini
echo [MailTo]%>>EmailInfo.ini
echo MailToNumber=%mailtonumber% >>EmailInfo.ini

set count=0
for /f "tokens=1 delims= " %%a in (name_all.txt) do (
	set /a count=!count!+1
	echo MailTo!count!=%%a >>EmailInfo.ini
)
rem ------------------------------
rem ========================================================================================================


rem =�������б�=================================================================================================
set mailccnumber=0
for %%a in (%mailcc%) do (
        set /a mailccnumber=!mailccnumber!+1
)
echo //�����ռ����б�>>EmailInfo.ini
echo [MailCC]>>EmailInfo.ini
echo MailCCNumber=%mailccnumber% >>EmailInfo.ini
set /a count=0
for %%a in (%mailcc%) do (
	set /a count=!count!+1
        echo MailCC!count!=%%a%mailfrom% >>EmailInfo.ini
)
rem ========================================================================================================


rem =���͸����б�===========================================================================================
set attachnumber=0
for %%a in (%attach%) do (
        set /a attachnumber=!attachnumber!+1
)

echo //�����б�>>EmailInfo.ini
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
echo ���ڷ����ʼ�......
EmailSend.exe
echo =====================
if exist name.txt del name.txt
if exist version_dir.txt del version_dir.txt
if exist name_all.txt del name_all.txt
echo ========================================================================================================

