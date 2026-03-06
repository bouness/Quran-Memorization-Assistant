; app.iss - Inno Setup script for QMA

[Setup]
AppName=QMA
AppVersion=latest
DefaultDirName={autopf}\QMA
DefaultGroupName=QMA
OutputDir=installer_output
OutputBaseFilename=QMAInstaller
Compression=lzma
SolidCompression=yes
SetupIconFile=assets\icon.ico
DisableProgramGroupPage=yes
UninstallDisplayIcon={app}\app.exe
ArchitecturesInstallIn64BitMode=x64compatible

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
Source: "dist\app.dist\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs

[Icons]
Name: "{group}\QMA"; Filename: "{app}\app.exe"
Name: "{commondesktop}\QMA"; Filename: "{app}\app.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a desktop icon"; GroupDescription: "Additional icons:"

[Run]
Filename: "{app}\app.exe"; Description: "Launch QMA"; Flags: nowait postinstall skipifsilent