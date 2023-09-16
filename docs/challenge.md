# LATAM Challenge
In the sections below, I explain the steps I followed to solve each part of the challenge
## Part I: Set up model

### Step 1: Review the .ipynb file

-   **Run, Review and Understand** the Jupyter Notebook thoroughly.
-   **Identify the Best Model**: I analyzed the different models proposed by the DS and given that both models have similar performance. I considered other factors like simplicity and interpretability. **Logistic Regression** is a relatively simple algorithm that is easier to understand and interpret. Given that both models have the same performance, the simplicity of logistic regression becomes a significant advantage. Also, Logistic Regression would be less prone to overfitting compared to a more complex model like XGBoost. Looking at the metrics in the notebook, the models that perfoms better are those with balanced data and feature importance, Therefore I used that version of the models.

### Step 2: Transcribe the Code

-   **Code Transcription**: I transcribed the necessary parts of the notebook into `model.py`.
-   **Bug Fixing**: While transcribing and testing the app the problems I find were related to versions of installed libraries and compatibilities
-   **Testing**: I implemented unit tests to ensure that the model works correctly. All tests passed successfully.
## Part II: API Development
-   **API Structure**: I used FastAPI to crate the app structure in the `api.py` file.
-   **Model Integration**: I Integrated the model training during the app creation and the inference in the predict endpoint
-   **Testing**: I wrote tests for the API endpoints. Here I faced an issue with the version of anyio that had to be downgraded
## Part III: Cloud Deployment
- **Dockerfile** I started writing the Dockerfile, the only change I made was that I prefered the image python:3.10-slim instead of the latest python image because it's simpler, requires less space in memory and builds faster
-   **Initial Approach - VM Instance**: Initially, I set up a virtual machine instance in Google Cloud Platform. I configured the necessary settings including CPU, memory, and networking options. And then I deployed and exposed the container. However I decided to change to a Cloud Run.     
-   **Shift to Docker and Cloud Run**: I configured Google Cloud Run, to fully manage serverless platform and automatically scale the containers. The reasons for this change include:
	- The API can handle a high number of requests, benefiting from Cloud Run's automatic scaling features.
	- Cloud Run only charges per request
	- Reduces the maintenance load compared to a VM
## Part IV: Implementing CI/CD Pipeline
-   **Github Actions**: Implement GitHub Actions for Continuous Integration and Continuous Deployment. So, I configured the pipeline with the `ci.yml` and `cd.yml` files to include the necessary steps. The pipelines includes:
-   **CI**
	- Install dependencies
	- Run flake8 linting
	- Run Tests
	- Run code coverage
-   **CD**
	- Push Docker image to  [Docker Hub](https://hub.docker.com/r/deayalar/latam)
	- Google Auth
	- Deploy to Cloud Run [Endpoint](https://latam-jv4wystoza-uc.a.run.app)

### HTTP Request
Call the deployed endpoint using this curl command

    curl  -X POST 'https://latam-jv4wystoza-uc.a.run.app/predict' \
    --header 'Content-Type: application/json' \
    --data-raw '{
            "flights": [
                {
                    "OPERA": "Aerolineas Argentinas", 
                    "TIPOVUELO": "N", 
                    "MES": 3
                }
            ]
        }'

 ### Challenge submission
 
    {
	    "name": "David Ayala",
	    "mail": "deayalar@gmail.com",
	    "github_url": "https://github.com/deayalar/latam-challenge.git",
	    "api_url": "https://latam-jv4wystoza-uc.a.run.app" 
    }

I got this response
{
  "status": "OK",
  "detail": "your request was received"
}
