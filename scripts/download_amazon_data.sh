#!/bin/bash
# Amazon Product Reviews Dataset Download Script
# Run this script when you're ready to download the large Amazon dataset

echo "Downloading Amazon Product Reviews dataset..."
echo "This will download the 5-core datasets for Electronics, Books, and Movies & TV."

# Create directory
mkdir -p data/raw/amazon

# Download specific categories (modify as needed)
categories=("Electronics" "Books" "Movies_and_TV")

for category in "${categories[@]}"; do
    echo "Downloading $category reviews..."
    wget -P data/raw/amazon/ "http://deepyeti.ucsd.edu/jianmo/amazon/categoryFiles/${category}.json.gz"
done

echo "Download complete!"
