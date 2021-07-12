import menu
from time import sleep

def main():
	choice = ''
	menu.displayTitle()
	while choice != 'q':
		menu.displayPrompts()
		choice = input("What would you like to do?")
		menu.processChoice(choice)
		if choice != 'q':
			menu.displayTitle()



if __name__ == "__main__":
	main()

