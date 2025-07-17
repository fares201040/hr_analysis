docker build -t ghcr.io/fares201040/hr_analysis .
echo <YOUR_GITHUB_TOKEN> | docker login ghcr.io -u <YOUR_GITHUB_USERNAME> --password-stdin
docker push ghcr.io/fares201040/hr_analysis:latest
docker run -p 10000:10000 ghcr.io/fares201040/hr_analysis