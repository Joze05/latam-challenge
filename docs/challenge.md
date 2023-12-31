# Flight Delay Predictor ⏱✈

## Overview

This is my project of the flight delay predictor, in which, by means of AI, we will be able to know if a flight will be delayed or not.

## About the development

- **Model choosed**: I decided to implement the logistic regression model for a couple of reasons:
    1. In the conclusions of the DS, it tells us that there is no noticeable difference between the XGB and LR models.
    2. When using one-hot encoding, LR is a good choice because, when changing the categorical variables to numerical variables, LR can show an advantage as it is a linear model.

    Personally, I think that the ideal would be to do research, such as cross-validation, to determine which model is better for this case.

- **Training**: The ``model.py`` module is made to train the model with the top 10 features. However, it is important to mention that this is because the tests asked for it. There is also a code to do it without these top 10 features. The model that I created (model_delay.pkl) to make the predictions is without the top 10 features since in the API tests we send data that involves the whole dataset.

- **Tests** (DEPRECATED INFO)🚫: In the repository, there is a branch for each test where you can see the approved reports:
    1. ``test-model``: In this branch, you can access the reports generated by the tests on the model.
    2. ``test-api``: In this branch, you can access the reports generated by the tests on the API.
    3. ``test-stress``: In this branch, you can access the reports generated by the stress test.

    I did this because it can present problems when executing the tests directly (make some-test) since different problems arise, such as project paths or dependencies, due to the fact that I program in Windows. However, I ran the tests in a Linux environment with everything in order so that the tests were validated and registered correctly.

- **Test NEW**❗: Solved the routing and requirements problem; now everything works as it should, and you can run the tests if you want, besides being considered necessary for the CI/CD in my opinion.

- **CI/CD**: For the CI/CD, I decided to define a personal workflow based on how I worked on my project:
    - ``CI``: For the CI, I chose to run the tests every time the 'dev' branch was pushed. I decided to do this because all the changes I make to my code go in this branch, and I think it is important to run the tests to verify that nothing has been changed to damage the tests because that means that our code is affecting the service.
    - ``CD``: For the CD, I made it to display (in the instance) the changes made every time a pull request is made from the dev branch to main. This is because every time valid changes are made in dev, I put them in main by means of a PR. This way, every time I pass code from dev to main, it is ready for production.

    I want to mention that this is my first time doing CI/CD, so apologies if the workflow is obviously flawed.

- **Deployment**: The API was deployed in a GCP instance as sugested. I want to say that I also have knowledge of AWS services and Terraform management as a plus.


## Use the API

You can easily make use of the API through the Swagger interface by using this URL:

```sh
http://35.209.10.24:8000/docs
```

## Run service locally

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

As a **curious fact**, I share the information of a LATAM flight that could be delayed 😮; obviously, it can be predicted with the API.

```
{
  "flights": [
    {
      "OPERA": "Grupo LATAM",
      "TIPOVUELO": "I",
      "MES": 7
    }
  ]
}
```

