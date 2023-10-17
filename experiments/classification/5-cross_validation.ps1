# .\experiments\classification\5-cross_validation.ps1
$MODELS_PATH = Join-Path (Get-Location) "results\models"
$PREDICTIONS_PATH = Join-Path (Get-Location) "results\predictions"

$CROSS_VALIDATION_PATH = Join-Path (Get-Location) "data/cross_validation"
$CONTENT_FEATURES_PATH = Join-Path (Get-Location) "data/features/content_features"
$HUMOR_FEATURES_PATH = Join-Path (Get-Location) "data/features/humor_features"
$ALL_FEATURES_PATH = Join-Path (Get-Location) "data/features/all_features"

Push-Location ..\Literature_methods\HumorRecognitionPT

# ------------- CONTENT FEATURES -------------
Write-Host "CONTENT FEATURES" -ForegroundColor DarkGreen -BackgroundColor Red -NoNewline
Write-Output `n

Get-ChildItem -Path $CONTENT_FEATURES_PATH -Name | ForEach-Object `
{
    Write-Host $_ -ForegroundColor DarkGreen -BackgroundColor Cyan -NoNewline
    Write-Output `n

    pipenv run python .\main.py -v clemencio train `
    --input (Join-Path (Join-Path $CONTENT_FEATURES_PATH $_) "train\data.hdf5") `
    --output (Join-Path (Join-Path $MODELS_PATH "content_features") $_) `
    --method "RandomForest"

    pipenv run python .\main.py -v clemencio test `
    --input (Join-Path (Join-Path $CONTENT_FEATURES_PATH $_) "test\data.hdf5") `
    --output (Join-Path (Join-Path $PREDICTIONS_PATH "content_features") ($_ + ".json")) `
    --model (Join-Path (Join-Path $MODELS_PATH "content_features") $_)
}

# ------------- HUMOR FEATURES -------------
Write-Host "HUMOR FEATURES" -ForegroundColor DarkGreen -BackgroundColor Red -NoNewline
Write-Output `n

Get-ChildItem -Path $HUMOR_FEATURES_PATH -Name | ForEach-Object `
{
    Write-Host $_ -ForegroundColor DarkGreen -BackgroundColor Cyan -NoNewline
    Write-Output `n

    pipenv run python .\main.py -v clemencio train `
    --input (Join-Path (Join-Path $HUMOR_FEATURES_PATH $_) "train\data.hdf5") `
    --output (Join-Path (Join-Path $MODELS_PATH "humor_features") $_) `
    --method "RandomForest"

    pipenv run python .\main.py -v clemencio test `
    --input (Join-Path (Join-Path $HUMOR_FEATURES_PATH $_) "test\data.hdf5") `
    --output (Join-Path (Join-Path $PREDICTIONS_PATH "humor_features") ($_ + ".json")) `
    --model (Join-Path (Join-Path $MODELS_PATH "humor_features") $_)
}

# ------------- ALL FEATURES -------------
Write-Host "ALL FEATURES" -ForegroundColor DarkGreen -BackgroundColor Red -NoNewline
Write-Output `n

Get-ChildItem -Path $ALL_FEATURES_PATH -Name | ForEach-Object `
{
    Write-Host $_ -ForegroundColor DarkGreen -BackgroundColor Cyan -NoNewline
    Write-Output `n

    pipenv run python .\main.py -v clemencio train `
    --input (Join-Path (Join-Path $ALL_FEATURES_PATH $_) "train\data.hdf5") `
    --output (Join-Path (Join-Path $MODELS_PATH "all_features") $_) `
    --method "RandomForest"

    pipenv run python .\main.py -v clemencio test `
    --input (Join-Path (Join-Path $ALL_FEATURES_PATH $_) "test\data.hdf5") `
    --output (Join-Path (Join-Path $PREDICTIONS_PATH "all_features") ($_ + ".json")) `
    --model (Join-Path (Join-Path $MODELS_PATH "all_features") $_)
}

# ------------- BERT -------------
Write-Host "BERT" -ForegroundColor DarkGreen -BackgroundColor Red -NoNewline
Write-Output `n

Get-ChildItem -Path $CROSS_VALIDATION_PATH -Name | ForEach-Object `
{
    Write-Host $_ -ForegroundColor DarkGreen -BackgroundColor Cyan -NoNewline
    Write-Output `n

    pipenv run python .\main.py -v transformer fine-tune `
    --input (Join-Path (Join-Path $CROSS_VALIDATION_PATH $_) "train.json") `
    --output (Join-Path (Join-Path $MODELS_PATH "bert") $_)

    pipenv run python .\main.py -v transformer test `
    --input (Join-Path (Join-Path $CROSS_VALIDATION_PATH $_) "test.json") `
    --output (Join-Path (Join-Path $PREDICTIONS_PATH "bert") ($_ + ".json")) `
    --model (Join-Path (Join-Path (Join-Path $MODELS_PATH "bert") $_) "checkpoint-3312")
}

Pop-Location
