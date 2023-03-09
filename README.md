MNIST Classification Web App
============================

This web app allows users to upload MNIST dataset images and classify them using a convolutional neural network model.

Getting Started
---------------

To get started, you'll need to do the following:

1. Clone the repository to your local machine.
2. Install the necessary dependencies.
3. Start the Flask server.
4. Start the Angular development server.
5. Navigate to `http://localhost:4200/` in your web browser to access the app.


Code Structure
---------------

Frontend - Frontend is built in Angular and can be found in `frontend` directory

Backend - Backend is build using flask and the files are found in the root directory 

Neural Network - The model was trained using `Google Colab` and tensorflow library. 
Jupyter Notebook with the code and results can be found in `ModelFiles` directory 
along with the trained model weights and a few input examples.



### Prerequisites

- Python 3.9 or higher
- Node.js
- Angular CLI
- Docker - for containerization

### Installing Dependencies

To install the necessary dependencies for the Flask server, run the following command in the root directory of the repository:

```
pip install -r requirements.txt

```

To install the necessary dependencies for the Angular app, go to `frontend` directory and run the following command:

```
npm install
```

### Starting the Flask Server

To start the Flask server, run the following command in the root directory of the repository:

```
python app.py
```

This will start the server on `http://localhost:5000/`.

### Starting the Angular Development Server

To start the Angular development server, run the following command in the `frontend` directory:

```
ng serve
```

This will start the server on `http://localhost:4200/`.

### Creating Docker compose

To build and start a Docker containers with docker-compose, run the following command in the root directory of the repository:

```
docker-compose up --build
```

Usage
-----

To use the app, navigate to `http://localhost:4200/` in your web browser. You'll be prompted to log in or sign up if you haven't already.

Once you're logged in, you can upload an MNIST dataset image and classify it using the convolutional neural network model.


Neural Network Description and Results
---------------

The model is a simple convolutional neural network consisting of three 2D convolutional 
layers with a kernel size of 3x3 and having 32, 64 and 128 filters respectively, 
the activation function used is ReLU. Each Conv layer followed by a 2x2 MaxPooling 
layer and a Dropout layer. 

Categorical Crossentropy was used as the loss function and the optimizer used was Adam.

The resulting model had the accuracy of 99.58% on the validation set.
This is a simple model architecture and more accurate model can be implemented
(current record holder achieved the accuracy of 99.91% as of March 2023), by adding more
convolutional layers the accuracy should increase, but that would also result in a larger and
slower model.

More info about the model, together with training results, can be found in `SimpleMNIST.ipynb` notebook.

