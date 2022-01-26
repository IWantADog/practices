"""如何使用greenlet"""

from greenlet import greenlet

def echo_user_input(user_input):
	print(f"<<< {user_input.strip()}")
	return user_input

def process_commands():
	while True:
		line = ''
		while not line.endswith('\n'):
			line += read_next_char()
		echo_user_input(line)
		if line == 'quit\n':
			print("Are you sure?")
			if echo_user_input(read_next_char()) != 'y':
				continue
			print("Exiting loop.")
			break
		process_command(line)

def process_command(line):
	print(f"process command {line.strip()}")

g_processor = greenlet(process_commands)

main_greenlet = greenlet.getcurrent()

def event_keydown(key):
	g_processor.switch(key)

def read_next_char():
	next_char = main_greenlet.switch("blocking in read_next_char")
	return next_char

def gui_mainloop():
	for c in 'hello\n':
		event_keydown(c)
	
	for c in 'quit\n':
		event_keydown(c)

	event_keydown('y')

if __name__ == '__main__':
	g_processor.switch()
	gui_mainloop()

	