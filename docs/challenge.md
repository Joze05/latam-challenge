# Flight Delay Predictor ⏱✈

## Overview

This is my project of the flight delay predictor, in which, by means of AI, we will be able to know if a flight will be delayed or not.

## About the development

- **Model choosed**: I decided to implement the logistic regression model for a couple of reasons:
    1. In the conclusions of the DS, it tells us that there is no noticeable difference between the XGB and LR models.
    2. When using one-hot encoding, LR is a good choice because, when changing the categorical variables to numerical variables, LR can show an advantage as it is a linear model.
 
    Personally, I think that the ideal would be to do research, such as cross-validation, to determine which model is better for this case.

- **Training**: The ``model.py`` module is made to train the model with the top 10 features. However, it is important to mention that this is because the tests asked for it. There is also a code to do it without these top 10 features. The model that I created (model_delay.pkl) to make the predictions is without the top 10 features since in the API tests we send data that involves the whole dataset.

- **Deployment**: The API was deployed in a GCP instance as sugested, I want to say

## Run locally

1. First, we build the project image with the following command:

```sh
docker build -t delay-image .
```

2. Second, we run a container with the image with the following command:

```sh
docker run -d -p 8000:8000 --name delay-container delay-image
```

## Comments

I want to thank you for the opportunity, it has been a nice test since I enjoy creating AI systems, it's like playing for me.
I apologize in advance for any omission of good practices, it was a little more complicated than usual because I am not used to create models with object oriented programming, I usually work more with imperative programming. <br>
I hope you like my project. 😄

