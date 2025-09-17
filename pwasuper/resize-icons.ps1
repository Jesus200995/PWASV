# Script para redimensionar iconos PWA
Add-Type -AssemblyName System.Drawing

function Resize-Image {
    param(
        [string]$InputPath,
        [string]$OutputPath,
        [int]$Width,
        [int]$Height
    )
    
    $image = [System.Drawing.Image]::FromFile($InputPath)
    $resized = New-Object System.Drawing.Bitmap($Width, $Height)
    $graphics = [System.Drawing.Graphics]::FromImage($resized)
    
    $graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $graphics.DrawImage($image, 0, 0, $Width, $Height)
    
    $resized.Save($OutputPath, [System.Drawing.Imaging.ImageFormat]::Png)
    
    $graphics.Dispose()
    $resized.Dispose()
    $image.Dispose()
}

$InputIcon = "public\icono-original.png"

# Crear icono 192x192
Resize-Image -InputPath $InputIcon -OutputPath "public\pwa-192x192.png" -Width 192 -Height 192
Write-Host "Icono 192x192 creado exitosamente"

# Crear icono 512x512
Resize-Image -InputPath $InputIcon -OutputPath "public\pwa-512x512.png" -Width 512 -Height 512
Write-Host "Icono 512x512 creado exitosamente"

Write-Host "Iconos PWA actualizados correctamente"
