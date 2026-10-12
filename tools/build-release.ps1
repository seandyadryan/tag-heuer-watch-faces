param([string]$Keystore = 'D:\KEYSTORE\tag-heuer-watch-faces.jks')
$ErrorActionPreference = 'Stop'
if (!(Test-Path -LiteralPath $Keystore)) { throw 'Keystore not found.' }
$password = Read-Host 'Keystore password' -AsSecureString
$pointer = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($password)
try {
    $env:RELEASE_STORE_FILE = (Resolve-Path -LiteralPath $Keystore).Path
    $env:RELEASE_STORE_PASSWORD = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($pointer)
    $env:RELEASE_KEY_PASSWORD = $env:RELEASE_STORE_PASSWORD
    $env:RELEASE_KEY_ALIAS = 'tag-heuer-watch-faces'
    Push-Location (Split-Path -Parent $PSScriptRoot)
    try {
        & .\gradlew.bat :wear:bundleRelease :companion:bundleRelease :wear:assembleRelease :companion:assembleRelease --console=plain
        if ($LASTEXITCODE -ne 0) { throw 'Release build failed.' }
    } finally { Pop-Location }
} finally {
    [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($pointer)
    Remove-Item Env:RELEASE_STORE_FILE,Env:RELEASE_STORE_PASSWORD,Env:RELEASE_KEY_PASSWORD,Env:RELEASE_KEY_ALIAS -ErrorAction SilentlyContinue
}
