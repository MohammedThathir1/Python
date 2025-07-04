import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ConversationHandler, ContextTypes, filters

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Define states for the conversation
QUESTION_1, QUESTION_2, QUESTION_3, QUESTION_4 = range(4)

# Example questions for the bot
questions = [
    {"question": "What is 2 + 2?", "answer": 4},

    {"question": '''In this space, I bend and break,
The laws of nature for knowledge’s sake.
Waves, forces, and energy collide,
Where theories of motion never hide.
I make the apple fall, the pendulum swing,
In my domain, even light takes wing.
If you're searching for truth in the unknown,
Find where experiments are carefully shown.''', "answer": 13},

    {"question": "What is 10 - 7?", "answer": 3},

    {"question": '''In this space, I bend and break,
The laws of nature for knowledge’s sake.
Waves, forces, and energy collide,
Where theories of motion never hide.
I make the apple fall, the pendulum swing,
In my domain, even light takes wing.
If you're searching for truth in the unknown,
Find where experiments are carefully shown.''', "answer": 13},
]

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('''The first team to correctly solve all 5 questions and 4 riddles will be declared
winner of the treasure hunt.

Create a WhatsApp group that includes team members and one coordinator.
Add +917850056018.

Good luck to all participants, and let the hunt begin!

For locations without room numbers, use the following specific codes:

Workshop: 1000
Indoor Stadium/Games: 2000
Saraswati Mata Idol: 3000
Badminton Court: 4000
Central Lawn: 5000
Parking Lot: 6000
Indian Flag: 7000
Constitution of India: 8000
Reception: 9000
Canteen: 1000
Library:1100
Seminar Hall:1200
Admission Cell:1300
T and P Cell:1400
Reprography Section:1500''')
    await update.message.reply_text(questions[0]["question"])
    return QUESTION_1

# Function to handle each question and check the answer
async def handle_question(update: Update, context: ContextTypes.DEFAULT_TYPE, current_question, next_state):
    try:
        answer = int(update.message.text)
        if answer == questions[current_question]["answer"]:
            if current_question < len(questions) - 1:
                await update.message.reply_text(questions[current_question + 1]["question"])
                return next_state
            else:
                await update.message.reply_text("End of Treasure hunt. You've answered all questions correctly!")
                return ConversationHandler.END
        else:
            await update.message.reply_text(f"Incorrect! Try again: {questions[current_question]['question']}")
            return current_question
    except ValueError:
        await update.message.reply_text("Please enter a valid integer.")
        return current_question

# Error handler to log errors
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

# Define the conversation handler for the bot
def create_conversation_handler():
    return ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            QUESTION_1: [MessageHandler(filters.TEXT & ~filters.COMMAND, lambda update, context: handle_question(update, context, 0, QUESTION_2))],
            QUESTION_2: [MessageHandler(filters.TEXT & ~filters.COMMAND, lambda update, context: handle_question(update, context, 1, QUESTION_3))],
            QUESTION_3: [MessageHandler(filters.TEXT & ~filters.COMMAND, lambda update, context: handle_question(update, context, 2, QUESTION_4))],
            QUESTION_4: [MessageHandler(filters.TEXT & ~filters.COMMAND, lambda update, context: handle_question(update, context, 3, ConversationHandler.END))],
            
        },
        fallbacks=[],
    )

def run_bot(token):
    # Create the bot application
    application = Application.builder().token(token).build()

    # Add the conversation handler to the bot
    conv_handler = create_conversation_handler()
    application.add_handler(conv_handler)

    # Register the error handler to log any errors
    application.add_error_handler(error_handler)

    # Start polling for updates
    application.run_polling()

if __name__ == '__main__':
    # Add your bot's API token here
    token = '6549117226:AAHYjD-FexocORG1fAbg_4qKn47r0aPvC8Y'

    # Run the bot
    run_bot(token)
