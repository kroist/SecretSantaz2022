import telebot
import numpy as np
import json

ADMIN_ID = 1234567
TOKEN = "TOKEN"

bot = telebot.TeleBot(TOKEN)

gift_assignments = {}

# try to read the list of registered users from the file
try:
  with open('registered_users.json', 'r') as f:
    registered_users = json.load(f)
except FileNotFoundError:
  # if the file doesn't exist, create an empty list
  registered_users = []

@bot.message_handler(commands=['start'])
def handle_start(message):
  text = """
👋Привет! Это Secret Santaz 2022 edition.
Secret Santaz - это рождественское и новогоднее событие, в котором каждый участник получит подарок от своего тайного Санты!

Как принять участие? простых шага:

1. Запишись в список тайных Сант командой 
/register
2. Подожди, пока бот тебе не сообщит, для кого ты будешь тайным Сантой в 2022 году.
3. Подари подарок! И получи подарок от тайнного Санты!

В этом году Главный Эльф заблудился в лабиринте, помоги ему добраться до санты и получи подарок от Real Santa
/maze
"""
  bot.send_message(message.chat.id, text, parse_mode='MARKDOWN')


@bot.message_handler(commands=['register'])
def handle_register(message):
  tup = {'id': message.from_user.id, 'first_name': message.from_user.first_name, 'username': message.from_user.username}
  if tup in registered_users:
    bot.send_message(message.chat.id, "Ты уже в списке участников!")
    return
  registered_users.append(tup)

  # write the updated list of registered users to a file
  with open('registered_users.json', 'w') as f:
    json.dump(registered_users, f, indent=1)

  bot.send_message(message.chat.id, "Теперь ты в списке участников! Вскоре ты узнаешь, для кого в этом году ты Секретный Санта!")


def is_derangement(permutation):
  # check if any element appears in its original position
  for i in range(len(permutation)):
    if permutation[i] == i:
      return False
  return True

@bot.message_handler(commands=['assign'])
def handle_assign(message):
  if message.from_user.id != ADMIN_ID:
    return
  if len(registered_users) < 2:
    bot.send_message(message.chat.id, "Не достаточно пользователей зарегистрировались.")
    return

  # create a derangement permutation of the registered users
  permutation = np.random.permutation(registered_users)
  while not is_derangement(permutation):
    permutation = np.random.permutation(registered_users)


  # iterate through the permutation and assign each user a gift recipient
  for i in range(len(permutation)):
    gift_assignments[permutation[i]['id']] = permutation[(i + 1) % len(permutation)]

  # send a message to each user with their gift recipient
  for user in registered_users:
    recipient = gift_assignments[user['id']]

    bot.send_message(
      user['id'],
      "В этому году ты секретный санта для: @{} ({})".format(recipient['username'], recipient['first_name'])
    )


# define the maze as a 2D array of characters
maze = [
  ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
  ['#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#', '.', '.', '.', '.', '.', '#', '.', '.', '.', '#', '.', '.', '.', '.', '.', '#', '.', '.', '.', '#', '.', '.', '.', '.', '.', '#'],
  ['#', '#', '#', '.', '#', '#', '#', '#', '#', '.', '#', '#', '#', '#', '#', '.', '#', '.', '#', '#', '#', '#', '#', '.', '#', '.', '#', '.', '#', '#', '#', '.', '#', '#', '#', '.', '#', '#', '#', '#', '#'],
  ['#', '.', '.', '.', '.', '.', '#', '.', '.', '.', '.', '.', '.', '.', '#', '.', '#', '.', '#', '.', '.', '.', '.', '.', '#', '.', '#', '.', '.', '.', '#', '.', '#', '.', '.', '.', '#', '.', '#', '.', '#'],
  ['#', '#', '#', '.', '#', '#', '#', '#', '#', '.', '#', '#', '#', '#', '#', '.', '#', '#', '#', '#', '#', '#', '#', '.', '#', '#', '#', '.', '#', '.', '#', '.', '#', '.', '#', '.', '#', '.', '#', '.', '#'],
  ['#', '.', '#', '.', '#', '.', '.', '.', '#', '.', '.', '.', '#', '.', '.', '.', '.', '.', '#', '.', '.', '.', '#', '.', '.', '.', '.', '.', '#', '.', '#', '.', '.', '.', '#', '.', '#', '.', '#', '.', '#'],
  ['#', '.', '#', '#', '#', '.', '#', '#', '#', '#', '#', '.', '#', '#', '#', '.', '#', '#', '#', '.', '#', '#', '#', '#', '#', '#', '#', '.', '#', '#', '#', '#', '#', '.', '#', '.', '#', '.', '#', '.', '#'],
  ['#', '.', '.', '.', '.', '.', '#', '.', '#', '.', '.', '.', '#', '.', '.', '.', '.', '.', '.', '.', '#', '.', '.', '.', '.', '.', '#', '.', '.', '.', '.', '.', '.', '.', '#', '.', '#', '.', '.', '.', '#'],
  ['#', '.', '#', '.', '#', '.', '#', '.', '#', '#', '#', '.', '#', '#', '#', '.', '#', '#', '#', '.', '#', '#', '#', '#', '#', '.', '#', '#', '#', '#', '#', '.', '#', '.', '#', '.', '#', '#', '#', '.', '#'],
  ['#', '.', '#', '.', '#', '.', '.', '.', '#', '.', '#', '.', '#', '.', '.', '.', '#', '.', '#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#', '.', '#', '.', '#', '.', '#', '.', '.', '.', '#'],
  ['#', '#', '#', '#', '#', '.', '#', '#', '#', '.', '#', '.', '#', '#', '#', '.', '#', '.', '#', '.', '#', '#', '#', '#', '#', '#', '#', '.', '#', '#', '#', '.', '#', '#', '#', '.', '#', '#', '#', '.', '#'],
  ['#', '.', '.', '.', '#', '.', '.', '.', '.', '.', '.', '.', '#', '.', '.', '.', '#', '.', '.', '.', '.', '.', '#', '.', '.', '.', '#', '.', '.', '.', '.', '.', '#', '.', '.', '.', '.', '.', '.', '.', '#'],
  ['#', '#', '#', '.', '#', '.', '#', '.', '#', '.', '#', '.', '#', '.', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '.', '#', '#', '#', '.', '#', '#', '#', '#', '#', '#', '#', '#', '#', '.', '#'],
  ['#', '.', '.', '.', '.', '.', '#', '.', '#', '.', '#', '.', '#', '.', '#', '.', '#', '.', '.', '.', '#', '.', '#', '.', '#', '.', '.', '.', '.', '.', '.', '.', '#', '.', '#', '.', '.', '.', '.', '.', '#'],
  ['#', '#', '#', '.', '#', '.', '#', '#', '#', '.', '#', '#', '#', '.', '#', '.', '#', '.', '#', '#', '#', '.', '#', '.', '#', '.', '#', '#', '#', '.', '#', '.', '#', '.', '#', '#', '#', '.', '#', '#', '#'],
  ['#', '.', '.', '.', '#', '.', '.', '.', '#', '.', '#', '.', '.', '.', '.', '.', '.', '.', '#', '.', '#', '.', '.', '.', '#', '.', '#', '.', '.', '.', '#', '.', '#', '.', '#', '.', '#', '.', '.', '.', '#'],
  ['#', '#', '#', '.', '#', '#', '#', '.', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '.', '#', '#', '#', '.', '#', '.', '#', '#', '#', '#', '#', '#', '#', '.', '#', '.', '#', '#', '#', '.', '#'],
  ['#', '.', '.', '.', '#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#', '.', '#', '.', '.', '.', '.', '.', '#', '.', '#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'],
  ['#', '.', '#', '.', '#', '.', '#', '.', '#', '#', '#', '#', '#', '.', '#', '#', '#', '.', '#', '.', '#', '#', '#', '.', '#', '.', '#', '#', '#', '#', '#', '.', '#', '#', '#', '#', '#', '#', '#', '.', '#'],
  ['#', '.', '#', '.', '#', '.', '#', '.', '.', '.', '.', '.', '#', '.', '#', '.', '.', '.', '#', '.', '#', '.', '.', '.', '.', '.', '#', '.', '.', '.', '.', '.', '#', '.', '.', '.', '.', '.', '#', '.', '#'],
  ['#', '#', '#', '.', '#', '#', '#', '.', '#', '#', '#', '#', '#', '#', '#', '.', '#', '#', '#', '#', '#', '#', '#', '.', '#', '#', '#', '#', '#', '.', '#', '.', '#', '#', '#', '.', '#', '.', '#', '#', '#'],
  ['#', '.', '#', '.', '.', '.', '#', '.', '.', '.', '.', '.', '#', '.', '.', '.', '.', '.', '#', '.', '.', '.', '#', '.', '#', '.', '#', '.', '.', '.', '#', '.', '#', '.', '#', '.', '#', '.', '.', '.', '#'],
  ['#', '.', '#', '.', '#', '.', '#', '#', '#', '.', '#', '.', '#', '.', '#', '#', '#', '.', '#', '.', '#', '#', '#', '#', '#', '.', '#', '.', '#', '#', '#', '#', '#', '.', '#', '#', '#', '.', '#', '#', '#'],
  ['#', '.', '#', '.', '#', '.', '#', '.', '#', '.', '#', '.', '#', '.', '#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#', '.', '#', '.', '.', '.', '.', '.', '#', '.', '.', '.', '.', '.', '.', '.', '#'],
  ['#', '.', '#', '#', '#', '#', '#', '.', '#', '.', '#', '.', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '.', '#', '.', '#', '.', '#', '#', '#', '#', '#', '.', '#', '#', '#', '#', '#', '#', '#'],
  ['#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#', '.', '#', '.', '.', '.', '#', '.', '.', '.', '.', '.', '#', '.', '#', '.', '.', '.', '#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#', '.', '#'],
  ['#', '.', '#', '#', '#', '.', '#', '#', '#', '#', '#', '#', '#', '.', '#', '#', '#', '#', '#', '.', '#', '#', '#', '.', '#', '#', '#', '.', '#', '#', '#', '#', '#', '.', '#', '.', '#', '#', '#', '.', '#'],
  ['#', '.', '.', '.', '#', '.', '#', '.', '.', '.', '#', '.', '.', '.', '.', '.', '#', '.', '.', '.', '.', '.', '.', '.', '#', '.', '.', '.', '.', '.', '#', '.', '#', '.', '#', '.', '.', '.', '.', '.', '#'],
  ['#', '#', '#', '#', '#', '.', '#', '#', '#', '.', '#', '#', '#', '#', '#', '.', '#', '#', '#', '.', '#', '.', '#', '#', '#', '#', '#', '#', '#', '.', '#', '.', '#', '.', '#', '#', '#', '.', '#', '#', '#'],
  ['#', '.', '.', '.', '.', '.', '#', '.', '.', '.', '#', '.', '.', '.', '#', '.', '#', '.', '#', '.', '#', '.', '#', '.', '.', '.', '.', '.', '#', '.', '#', '.', '.', '.', '#', '.', '#', '.', '.', '.', '#'],
  ['#', '.', '#', '#', '#', '#', '#', '.', '#', '#', '#', '.', '#', '#', '#', '.', '#', '.', '#', '#', '#', '.', '#', '.', '#', '.', '#', '.', '#', '.', '#', '#', '#', '#', '#', '.', '#', '.', '#', '.', '#'],
  ['#', '.', '.', '.', '.', '.', '.', '.', '#', '.', '.', '.', '.', '.', '#', '.', '.', '.', '#', '.', '.', '.', '.', '.', '#', '.', '#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#', '.', '#'],
  ['#', '#', '#', '#', '#', '.', '#', '#', '#', '#', '#', '.', '#', '#', '#', '.', '#', '#', '#', '.', '#', '#', '#', '.', '#', '#', '#', '#', '#', '#', '#', '.', '#', '#', '#', '.', '#', '#', '#', '#', '#'],
  ['#', '.', '#', '.', '.', '.', '#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#', '.', '#', '.', '#', '.', '#', '.', '.', '.', '.', '.', '#', '.', '#', '.', '#', '.', '.', '.', '#'],
  ['#', '.', '#', '.', '#', '#', '#', '.', '#', '#', '#', '#', '#', '.', '#', '.', '#', '#', '#', '#', '#', '.', '#', '.', '#', '.', '#', '#', '#', '.', '#', '#', '#', '.', '#', '.', '#', '.', '#', '#', '#'],
  ['#', '.', '.', '.', '.', '.', '#', '.', '.', '.', '#', '.', '#', '.', '#', '.', '#', '.', '#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#', '.', '#', '.', '.', '.', '#', '.', '.', '.', '.', '.', '#'],
  ['#', '.', '#', '#', '#', '.', '#', '.', '#', '.', '#', '.', '#', '.', '#', '#', '#', '.', '#', '.', '#', '#', '#', '.', '#', '#', '#', '.', '#', '#', '#', '.', '#', '#', '#', '#', '#', '.', '#', '.', '#'],
  ['#', '.', '.', '.', '#', '.', '.', '.', '#', '.', '#', '.', '.', '.', '.', '.', '.', '.', '#', '.', '#', '.', '#', '.', '#', '.', '.', '.', '#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#', '.', '#'],
  ['#', '#', '#', '#', '#', '.', '#', '.', '#', '#', '#', '#', '#', '#', '#', '.', '#', '.', '#', '#', '#', '.', '#', '#', '#', '#', '#', '.', '#', '.', '#', '.', '#', '#', '#', '#', '#', '.', '#', '.', '#'],
  ['#', '.', '.', '.', '.', '.', '#', '.', '#', '.', '.', '.', '.', '.', '.', '.', '#', '.', '#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#', 'F', '#', '.', '.', '.', '.', '.', '#', '.', '#', '.', '#'],
  ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#']
]

# create a dictionary mapping characters to emojis for display
emoji_map = {
  '#': '🧱',  # wall
  '.': '🌫',  # air
  'P': '⛄️',  # player
  'F': '🎅'   # finish
}

# define the initial position of the player
# player_pos = [1, 1]

# try to read the list of registered users from the file
try:
  with open('player_poses.json', 'r') as f:
    player_poses = json.load(f)
except FileNotFoundError:
  # if the file doesn't exist, create an empty list
  player_poses = {}

# try to read the list of registered users from the file
try:
  with open('won_players.json', 'r') as f:
    won_players = json.load(f)
except FileNotFoundError:
  # if the file doesn't exist, create an empty list
  won_players = []


# define the commands for moving the player
commands = {
  'left': [-1, 0],
  'right': [1, 0],
  'up': [0, -1],
  'down': [0, 1]
}

def get_view(player_pos, maze):

  # create an empty view
  view = ""


  # get the indices of the top-left and bottom-right corners of the view
  top_left = [max(player_pos[0]-3, 0), max(player_pos[1]-3, 0)]
  bottom_right = [min(player_pos[0]+3, len(maze[0])-1), min(player_pos[1]+3, len(maze)-1)]

  # iterate through the rows of the maze
  for y in range(top_left[1], bottom_right[1]+1):
    # iterate through the columns of the maze
    for x in range(top_left[0], bottom_right[0]+1):
      # add the corresponding emoji for the current maze cell to the view
      if x == player_pos[0] and y == player_pos[1]:
        view += emoji_map['P']
      else:
        view += emoji_map[maze[y][x]]
    # add a newline character after each row
    view += "\n"

  return view

def generate_buttons():
  # create a list of buttons for the inline keyboard
  buttons = []
  for command in commands:
    # create a button for each movement command
    # use the corresponding emoji for the command in the button text
    if command == 'left':
      button = telebot.types.InlineKeyboardButton(text='⬅️', callback_data=command)
    elif command == 'right':
      button = telebot.types.InlineKeyboardButton(text='➡️', callback_data=command)
    elif command == 'up':
      button = telebot.types.InlineKeyboardButton(text='⬆️', callback_data=command)
    elif command == 'down':
      button = telebot.types.InlineKeyboardButton(text='⬇️', callback_data=command)
    buttons.append(button)

  # create an inline keyboard with the buttons
  keyboard = telebot.types.InlineKeyboardMarkup()
  keyboard.add(*buttons)

  return keyboard

@bot.message_handler(commands=['maze'])
def handle_view(message):
  keyboard = generate_buttons()
  # get the current view
  from_id = message.chat.id
  if str(from_id) in player_poses:
    player_pos = player_poses[str(from_id)]
  else:
    player_pos = [1, 1]
  if maze[player_pos[1]][player_pos[0]] == 'F':
    text = '🎁🎁🎁🎁🎁🎁🎁🎁🎁\n' + 'Поздравляю! Ты прошел лабиринт и получишь специальный подарок от Санты!' + '\n' + '🎁🎁🎁🎁🎁🎁🎁🎁🎁'
    bot.send_message(from_id, text)
    return

  view = get_view(player_pos, maze)
  # send the view and the inline keyboard to the user
  bot.send_message(from_id, view, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(callback_query):
  # get the command from the callback data
  command = callback_query.data
  # get the corresponding movement
  movement = commands[command]

  from_id = callback_query.from_user.id
  if str(from_id) in player_poses:
    player_pos = player_poses[str(from_id)]
  else:
    player_pos = [1, 1]

  if maze[player_pos[1]][player_pos[0]] == 'F':
    text = '🎁🎁🎁🎁🎁🎁🎁🎁🎁\n' + 'Поздравляю! Ты прошел лабиринт и получишь специальный подарок от Санты!' + '\n' + '🎁🎁🎁🎁🎁🎁🎁🎁🎁'
    bot.send_message(from_id, text)
    return

  # update the player's position
  player_pos[0] += movement[0]
  player_pos[1] += movement[1]

  keyboard = generate_buttons()

  # check if the new position is a wall
  if maze[player_pos[1]][player_pos[0]] == '#':
    # if it is a wall, move the player back to their original position
    player_pos[0] -= movement[0]
    player_pos[1] -= movement[1]
    bot.answer_callback_query(callback_query.id, "Нельзя ходить сквозь стены! Попробуй другое направление.")
  elif maze[player_pos[1]][player_pos[0]] == 'F':
    text = '🎁🎁🎁🎁🎁🎁🎁🎁🎁\n' + 'Поздравляю! Ты прошел лабиринт и получишь специальный подарок от Санты!' + '\n' + '🎁🎁🎁🎁🎁🎁🎁🎁🎁'
    won_players.append(str(from_id))
    with open('won_players.json', 'w') as f:
      json.dump(won_players, f, indent=1)
    bot.edit_message_text(text=text, chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, reply_markup=None)
  else:
    # if it is not a wall, update the maze and send the updated view to the user
    view = get_view(player_pos, maze)
    bot.edit_message_text(text=view, chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, reply_markup=keyboard)
  player_poses[str(from_id)] = player_pos
  with open('player_poses.json', 'w') as f:
    json.dump(player_poses, f, indent=1)



bot.polling()

bot.polling()
