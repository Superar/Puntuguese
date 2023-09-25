# .\experiments\by_dialect\3-extract_features.ps1
$CROSS_VALIDATION_PATH = Join-Path (Get-Location) "data/cv_by_dialect"
$CONTENT_FEATURES_PATH = Join-Path (Get-Location) "data/features_by_dialect/content_features"
$HUMOR_FEATURES_PATH = Join-Path (Get-Location) "data/features_by_dialect/humor_features"
$ALL_FEATURES_PATH = Join-Path (Get-Location) "data/features_by_dialect/all_features"

Push-Location ..\Literature_methods\HumorRecognitionPT

# Resources
$SENTLEX = ".\data\Lexica\SentiLex02.json"
$SLANG = ".\data\Lexica\termos_calao.json"
$ANTONYM_TRIPLES = ".\data\Lexica\antonyms.json"
$EMBEDDINGS = ".\data\Lexica\cbow_s300.txt"
$MWP = ".\data\Lexica\MWP.json"

# ------------- CONTENT FEATURES -------------
Write-Host "CONTENT FEATURES" -ForegroundColor DarkGreen -BackgroundColor Red -NoNewline
Write-Output `n

Get-ChildItem -Path $CROSS_VALIDATION_PATH -Recurse | Where-Object { $_.Name -Match "train.json" } | ForEach-Object {
    $dialect = $_.Directory.Parent.Name
    $fold = $_.Directory.Name 
    Write-Host $dialect / $fold -ForegroundColor DarkGreen -BackgroundColor Cyan -NoNewline
    Write-Output `n

    pipenv run python .\main.py -v feat `
        -i $_.FullName `
        -o (Join-Path (Join-Path (Join-Path $CONTENT_FEATURES_PATH $dialect) $fold) "train") `
        --tfidf

    pipenv run python .\main.py -v feat `
        -i $_.FullName.Replace('train.json', 'test.json') `
        -o (Join-Path (Join-Path (Join-Path $CONTENT_FEATURES_PATH $dialect) $fold) "test") `
        --tfidf `
        --vectorizer (Join-Path (Join-Path (Join-Path $CONTENT_FEATURES_PATH $dialect) $fold) "train\vectorizer.pkl")
}

# ------------- HUMOR FEATURES -------------
Write-Host "HUMOR FEATURES" -ForegroundColor DarkGreen -BackgroundColor Red -NoNewline
Write-Output `n

Get-ChildItem -Path $CROSS_VALIDATION_PATH -Recurse | Where-Object { $_.Extension -Match ".json" } | ForEach-Object {
    $dialect = $_.Directory.Parent.Name
    $fold = $_.Directory.Name 
    $split = $_.BaseName 
    Write-Host $dialect / $fold / $split -ForegroundColor DarkGreen -BackgroundColor Cyan -NoNewline
    Write-Output `n

    pipenv run python .\main.py -v feat `
        -i $_.FullName `
        -o (Join-Path (Join-Path (Join-Path $HUMOR_FEATURES_PATH $dialect) $fold) $split) `
        --sentlex $SENTLEX `
        --slang $SLANG `
        --alliteration `
        --antonym $ANTONYM_TRIPLES `
        --embeddings $EMBEDDINGS `
        --mwp $MWP `
        --ner `
        --ambiguity
}

# ------------- ALL FEATURES -------------
Write-Host "ALL FEATURES" -ForegroundColor DarkGreen -BackgroundColor Red -NoNewline
Write-Output `n

Get-ChildItem -Path $CROSS_VALIDATION_PATH -Recurse | Where-Object { $_.Name -Match "train.json" } | ForEach-Object {
    $dialect = $_.Directory.Parent.Name
    $fold = $_.Directory.Name 
    Write-Host $dialect / $fold -ForegroundColor DarkGreen -BackgroundColor Cyan -NoNewline
    Write-Output `n

    pipenv run python .\main.py -v feat `
        -i $_.FullName `
        -o (Join-Path (Join-Path (Join-Path $ALL_FEATURES_PATH $dialect) $fold) "train") `
        --tfidf `
        --sentlex $SENTLEX `
        --slang $SLANG `
        --alliteration `
        --antonym $ANTONYM_TRIPLES `
        --embeddings $EMBEDDINGS `
        --mwp $MWP `
        --ner `
        --ambiguity

    pipenv run python .\main.py -v feat `
        -i $_.FullName.Replace('train.json', 'test.json') `
        -o (Join-Path (Join-Path (Join-Path $ALL_FEATURES_PATH $dialect) $fold) "test") `
        --tfidf `
        --vectorizer (Join-Path (Join-Path (Join-Path $ALL_FEATURES_PATH $dialect) $fold) "train\vectorizer.pkl") `
        --sentlex $SENTLEX `
        --slang $SLANG `
        --alliteration `
        --antonym $ANTONYM_TRIPLES `
        --embeddings $EMBEDDINGS `
        --mwp $MWP `
        --ner `
        --ambiguity
}

Pop-Location
