
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    if not current_question_id:
        return True, ''
    
    try:
        session['message_history'].append(answer)
    except Exception as e:
        return False, e
    
    return True, ""


def get_next_question(current_question_id):

    if(not current_question_id):
        return PYTHON_QUESTION_LIST[0], '0'
    
    try:
        PYTHON_QUESTION_LIST[int(current_question_id) + 1]
    except IndexError:
        return '', None
    except Exception as e:
        return '', None
    
    return PYTHON_QUESTION_LIST[int(current_question_id) + 1], str(int(current_question_id) + 1)


def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''

    history = session['message_history']
    count = 0

    for i in range(len(history)):
        if(history[i] == PYTHON_QUESTION_LIST[i]['answer']):
            count += 1
    

    return 'You give {} correct answer out of {}'.format(count, len(PYTHON_QUESTION_LIST))
