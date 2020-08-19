import sys
from slack_parse import SlackParse

if __name__ == '__main__':
    try:
        arg = sys.argv[1:]
        path = arg[0]
        show_tree_command = arg[1] if len(sys.argv[1:]) > 1 else ''

        slack_pares = SlackParse(path)
        if 'tree' in show_tree_command:
            slack_pares.show_tree()
        elif 'help' in path:
            SlackParse.help()
        else:
            slack_pares.backup()
            slack_pares.run()

    except (KeyError, IndexError):
        print('''
    You forgot to pass an argument or your arguments not correct!
    See example: 
        python handle_slack_messages.py --help
        python handle_slack_messages.py channels/your-channel-name/ 
        python handle_slack_messages.py channels/your-channel-name/ --tree
    ''')


