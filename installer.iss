; Chipchipdownload - Inno Setup script (v6.3)
; Cai dat tool vao {pf}\Chipchipdownload, tao shortcut Desktop + Start Menu
; voi icon ga con. Go cai dat se xoa luon cac thu vien tool da tu tai ve
; khi chay (yt-dlp.exe, ffmpeg.exe, ffprobe.exe, config.json, jobs.json).
; Build bang: ISCC.exe installer.iss  (can file dist\Chipchipdownload.exe
; va chipchipdownload.ico o cung thu muc repo).


#define MyAppName "Chipchipdownload"
#define MyAppVersion "7.29"
 #define MyAppPublisher "Gà Con cho CYAN"
#define MyAppExeName "Chipchipdownload.exe"


[Setup]
AppId={{A7C3D9E1-4B2F-4A8C-9E5D-1F3A6B8C0D42}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={pf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
OutputDir=installer-out
OutputBaseFilename=Chipchipdownload-Setup-v{#MyAppVersion}
SetupIconFile=chipchipdownload.ico
Compression=lzma
SolidCompressios
WizardStyle=modern
UninstallDisplayName={#MyAppName}
UninstallDisplayIcon={app}\{#MyAppExeName}
VersionInfoVersion={#MyAppVersion}
; Ghi de exe cu khi cai lai (de update bang ban cai dat)
[Files]
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "chipchipdownload.ico"; DestDir: "{app}"; Flags: ignoreversion


[Icons]
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\chipchipdownload.ico"
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\chipchipdownload.ico"
Name: "{group}\Gỡ cài đặt {#MyAppName}"; Filename: "{uninstallexe}"


[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Mở {#MyAppName} ngay"; Flags: nowait postinstall skipifsilent


; Go cai dat: xoa luon cac file thu vien + du lieu tool da tu tai/tao ra khi
; chay (nam cung thu muc cai dat). Chi xoa sau khi go cai dat xong.
[UninstallDelete]
Type: files; Name: "{app}\yt-dlp.exe"
Type: files; Name: "{app}\ffmpeg.exe"
Type: files; Name: "{app}\ffprobe.exe"
Type: files; Name: "{app}\ffmpeg-essentials.zip"
Type: files; Name: "{app}\config.json"
Type: files; Name: "{app}\jobs.json"
Type: files; Name: "{app}\Chipchipdownload.exe.new"
Type: files; Name: "{app}\capnhat.bat"
