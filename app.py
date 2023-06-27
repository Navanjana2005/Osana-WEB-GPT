from flask import Flask, render_template_string, request, jsonify
from gradio_client import Client

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template_string('''
       <!DOCTYPE html>
<html>
<head>
    <title>Osana WEB-GPT</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #dbdbdb;
            margin: 5px;
            padding: 0;
        }

        .chat-container {
            position: relative;
            width: 100%;
            height: 90vh;
            margin: 0 auto;
            background-color: #ffffff;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            border-radius: 10px;
            overflow: hidden;
        }

        .chat-container::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: rgba(0, 123, 255, 0.1);
            z-index: -1;
            animation: pulseAnimation 2s linear infinite;
        }

        @keyframes pulseAnimation {
            0% {
                transform: scale(1);
                opacity: 1;
            }
            50% {
                transform: scale(1.05);
                opacity: 0.8;
            }
            100% {
                transform: scale(1);
                opacity: 1;
            }
        }

        .chat-header {
            background-color: #007bff;
            color: #ffffff;
            padding: 10px;
            text-align: center;
            font-size: 40px;
        }

        .chat-body {
            padding: 20px;
            height: 80%;
            overflow-y: scroll;
        }

        .chat-bubble {
            margin-bottom: 20px;
            width: 100%;
        }

        .user-bubble {
            background-color: #007bff;
            color: #ffffff;
            padding: 10px;
            border-radius: 30px 0px 30px 30px;
            text-align: right;
        }

        .bot-bubble {
            background-color: #f0f0f0;
            color: #000000;
            padding: 10px;
            border-radius: 0px 30px 30px 30px;
        }

        .chat-form {
            display: flex;
            margin-top: 20px;
        }

        .chat-input {
            flex: 1;
            padding: 10px;
            border: none;
            border-bottom: 1px solid #aaaaaa;
            font-size: 16px;
            outline: none;
            color: #000000;
            margin-bottom: 0;
            border-radius: 10px;
        }

        .chat-submit {
            margin-left: 10px;
            padding: 10px 20px;
            border: none;
            background-color: #007bff;
            color: #ffffff;
            font-size: 16px;
            cursor: pointer;
            border-radius: 30px;
            transition: background-color 0.3s;
        }

        .chat-submit:hover {
            background-color: #0056b3;
        }
        @media (max-width: 400px) {
    .chat-header {
        font-size: 30px;
    }

    @media (max-width: 330px) {
    .chat-header {
        font-size: 20px;
    }
    }
    .chat-bubble {
            font-size: 80%;
        }
}

    </style>
</head>
<body>
    <div class="container">
        <div class="chat-container">
            <div class="chat-header">Osana Web-GPT</div>
            <div class="chat-body" id="chat-body">
                <div class="chat-bubble bot-bubble">Welcome to the Osana Web-GPT! Ask me anything.</div>
            </div>
        </div>
        
        <form id="question-form" class="chat-form">
            <div class="input-group">
                <input type="text" id="question-input" name="question" placeholder="Type your message here" class="form-control">
                <div class="input-group-append">
                    <button type="submit" class="btn btn-primary"><i class="fa fa-send"></i></button>
                </div>
            </div>
        </form>
    </div>

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    <script>
        document.getElementById('question-form').addEventListener('submit', function(event) {
            event.preventDefault();
            var question = document.getElementById('question-input').value;
            var chatBody = document.getElementById('chat-body');
            var userBubble = document.createElement('div');
            userBubble.className = 'chat-bubble user-bubble';
            userBubble.textContent = question;
            chatBody.appendChild(userBubble);
            scrollToBottom(chatBody);
            document.getElementById('question-input').value = '';
            fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: 'question=' + encodeURIComponent(question)
            })
            .then(response => response.json())
            .then(result => {
                var botBubble = document.createElement('div');
                botBubble.className = 'chat-bubble bot-bubble';
                botBubble.textContent = result['response'];
                chatBody.appendChild(botBubble);
                scrollToBottom(chatBody);
            });
        });

        function scrollToBottom(element) {
            element.scrollTop = element.scrollHeight;
        }
    </script>
</body>
</html>

    ''')

@app.route('/predict', methods=['POST'])
def predict():
    client = Client("https://malmika-osana-web-gpt.hf.space/")
    prompt = request.form['question']
    result = client.predict(prompt, api_name="/predict")
    return jsonify({'response': result})

if __name__ == '__main__':
    app.run(debug=True)
