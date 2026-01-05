<b>FitTrack</b>

FitTrack is a web-based fitness platform developed as part of the ICT 4879 Capstone Project.

The project focuses on encouraging healthy lifestyle habits by combining workout programs, nutrition tracking, and an AI-powered chatbot in a single application.

<b>Features</b>

- FitTrack allows users to browse and follow workout programs.

- Users can track calories and food intake through a simple nutrition system.

- A user dashboard provides access to personal fitness-related information.

- Premium features are available through the platform.

- An AI-powered chatbot assists users with fitness and nutrition questions.

- The interface is fully responsive and designed for ease of use.

<b>AI Chatbot</b>

- FitTrack includes an AI-powered chatbot that helps users with fitness-related questions.

- The chatbot provides guidance on workouts, nutrition, and general healthy habits.

- All chatbot intelligence is handled on the backend using an AI model, while the frontend manages only the user interface.

- The chatbot does not provide medical advice.

<b>Technologies Used</b>

- The backend of the application is built using Python and Django.

- The frontend uses HTML, CSS, and JavaScript.

- SQLite is used as the database during development.

- The chatbot uses the OpenAI API.


<b>Environment Setup</b>

To run the project locally, an environment variable is required.

Create a .env file in the project root directory and add the OpenAI API key as shown below:

OPENAI_API_KEY=your_openai_api_key_here

<b>Run the Project Locally</b>

1. Clone the repository with the following command. Make sure that git is installed into the system. 
   - git clone https://github.com/Nickthequick2002/ICT-4879_Capstone-Project_Orfanidis.git

2. After the repository is cloned, move into the project directory using the following command:
   - cd FitTrack

3. Install the required dependencies using the requirements file.
   - pip install -r requirements.txt

4. Apply database migrations.
   - python manage.py migrate

5. Start the development server.
   - python manage.py runserver

6. Open a browser and navigate to:
   - http://127.0.0.1:8000/
  

**LIVE DEMO**

Below there is a link for testing the website live. The link was created using PythonAnywhere.

- Website URL: [https://nikolasorf.pythonanywhere.com](https://nikolasorf.pythonanywhere.com)







