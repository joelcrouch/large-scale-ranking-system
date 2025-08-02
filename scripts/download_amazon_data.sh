#!/bin/bash
# Amazon Product Reviews Dataset Download Script
# Run this script when you're ready to download the large Amazon dataset

echo "Downloading Amazon Product Reviews dataset..."
echo "Warning: This will download several GB of data"

# Create directory
mkdir -p data/raw/amazon

# Download specific categories (modify as needed)
categories=("Electronics" "Books" "Movies_and_TV")

for category in "${categories[@]}"; do
    echo "Downloading $category reviews..."
    wget -P data/raw/amazon/ "https://amazon-reviews-pds.s3.amazonaws.com/tsv/amazon_reviews_us_${category}_v1_00.tsv.gz"
done

echo "Download complete!"
