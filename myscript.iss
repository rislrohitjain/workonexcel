[Setup]
; The name of your app
AppName=WorkOnExcelRohitJianPro
AppVersion=1.0
; The default folder name on the client machine
DefaultDirName={autopf}\windowexework
DefaultGroupName=windowexework
; Where the final installer file will be saved
OutputDir=D:\projects\python\workonexcel\Output
OutputBaseFilename=WorkOnExcelRohitJianPro_Setup
; Ensures it asks for Admin rights to create folders in Program Files
PrivilegesRequired=admin
Compression=lzma
SolidCompression=yes

[Files]
; Point this to your .exe in the 'dist' folder
Source: "D:\projects\python\workonexcel\dist\WorkOnExcelRohitJianPro.exe"; DestDir: "{app}"; Flags: ignoreversion

[Dirs]
; This creates the extra folders you wanted inside 'windowexework'
Name: "{app}\logs"
Name: "{app}\config"
Name: "{app}\database"

[Icons]
; Creates a Start Menu shortcut
Name: "{group}\WorkOnExcelRohitJianPro"; Filename: "{app}\WorkOnExcelRohitJianPro.exe"
; Creates a Desktop shortcut
Name: "{commondesktop}\WorkOnExcelRohitJianPro"; Filename: "{app}\WorkOnExcelRohitJianPro.exe"