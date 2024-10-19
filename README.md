# Interview Question Generator

This project is an AI-powered interview question generator that creates tailored questions based on job descriptions. It uses the Gemini AI model to generate a set of interview questions with varying difficulty levels, along with evaluation criteria and sample answers.

## Features

- Generate interview questions based on job descriptions
- Three difficulty levels: Normal, Medium, and Advanced
- Each question includes evaluation criteria and a sample answer
- Real-time statistics on total runs and questions generated
- Responsive web interface

## Technologies Used

- Backend: Flask (Python)
- Frontend: HTML, JavaScript, Tailwind CSS
- AI Model: Google's Gemini AI

## Setup and Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/interview-question-generator.git
   ```

2. Install the required Python packages:
   ```
   pip install flask flask-cors google-generativeai
   ```

3. Set up your Gemini AI API key in the `app.py` file.

4. Run the Flask application:
   ```
   python app.py
   ```

5. Open a web browser and navigate to `http://127.0.0.1:5006` to use the application.

## Usage

1. Enter a job description in the provided text area.
2. Click the "Generate Questions" button.
3. View the generated questions, categorized by difficulty level.
4. Click on each question to reveal the evaluation criteria and sample answer.

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to check [issues page](https://github.com/yourusername/interview-question-generator/issues) if you want to contribute.

## Author

Muhammad Usman - ranausman@outlook.com

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
