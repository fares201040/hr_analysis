1) delete the csv file in the unclean_folder and past the new one
2) delete the file named "cleaned.csv" from the clean_data folder
3) execute "python -m src.hr_analysis.data_cleaner"
4) build docker:
==== build and run the container====
docker build -t ghcr.io/fares201040/hr_analysis:latest .
docker run -p 10000:10000 ghcr.io/fares201040/hr_analysis

5) git add . && git commit -m "new csv file" && git push origin main

====connect to ghcr.io====
echo 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 | docker login ghcr.io -u fares201040 --password-stdin
docker push ghcr.io/fares201040/hr_analysis:latest

