
# Food Delivery App

Welcome to the Food Delivery App! This application is built using Django and Django CMS, with an integrated AI assistant powered by RASA, a Python framework. This README provides an overview of the project, instructions for setting up the development environment, and information on how to use the app.

## Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Technology Stack](#technology-stack)
4. [Setup and Installation](#setup-and-installation)
5. [Usage](#usage)
6. [AI Assistant](#ai-assistant)
7. [Contributing](#contributing)
8. [License](#license)

## Project Overview

The Food Delivery App allows users to browse through various restaurants, view menus, place orders, and track their delivery status. The app also includes an AI assistant to help users with their queries and provide a better user experience.

## Features

- User Authentication and Authorization
- Restaurant Listing and Menu Management
- Order Placement and Tracking
- Integrated AI Assistant for user support
- Content Management using Django CMS

## Technology Stack

- **Backend**: Django
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite (for development), PostgreSQL/MySQL (for production)
- **AI Assistant**: RASA (Python framework)
- **Content Management**: Django CMS

## Setup and Installation

### Prerequisites

- Python 3.8+
- Django 3.2+
- Node.js (for RASA)
- pip (Python package installer)
- virtualenv (optional, but recommended)

### Installation Steps

1. **Clone the repository**
    ```sh
    git clone https://github.com/yourusername/food-delivery-app.git
    cd food-delivery-app
    ```

2. **Create a virtual environment**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the required packages**
    ```sh
    pip install -r requirements.txt
    ```

4. **Set up the database**
    ```sh
    python manage.py migrate
    ```

5. **Create a superuser**
    ```sh
    python manage.py createsuperuser
    ```

6. **Run the development server**
    ```sh
    python manage.py runserver
    ```

7. **Set up Django CMS**
    - Access the Django admin panel at `http://127.0.0.1:8000/admin/`
    - Log in with the superuser credentials and create the necessary CMS pages and content.

8. **Set up RASA**
    - Navigate to the `rasa` directory
    ```sh
    cd rasa
    ```
    - Install RASA dependencies
    ```sh
    pip install -r requirements.txt
    ```
    - Train the RASA model
    ```sh
    rasa train
    ```
    - Run the RASA server
    ```sh
    rasa run actions
    rasa run --enable-api --cors "*"
    ```

## Usage

- Access the app at `http://127.0.0.1:8000/`
- Log in with your credentials
- Browse through restaurants, view menus, place orders, and track your delivery status
- Use the AI assistant for any queries or help

## AI Assistant

The AI assistant is built using RASA, a Python framework, and is integrated into the Django app. It helps users with various queries related to the app, such as order status, menu details, and general inquiries.

### RASA Training and Development

- To modify the AI assistant's behavior, update the training data in the `data` directory
- Train the model using `rasa train`
- Test the assistant using `rasa shell`

## Contributing

We welcome contributions! Please fork the repository and create a pull request with your changes. Make sure to follow the project's coding standards and write tests for new features.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

