import requests
from bs4 import BeautifulSoup
from time import sleep
from csv import writer
from random import choice


class Game:
    BASE_URL = 'http://quotes.toscrape.com'

    def __init__(self):
        self.all_quotes = []
        self.current_page = '/page/1'

    def start(self):
        self.__scrape_data()
        self.__write_to_file()
        self.__play_game()

    def __scrape_data(self):
        # scrape each page
        while self.current_page:
            res = requests.get(f'{self.BASE_URL}{self.current_page}')
            print(f'Now Scraping {self.BASE_URL}{self.current_page}...')
            soup = BeautifulSoup(res.text, 'html.parser')
            quotes = soup.find_all(class_="quote")

            # extract text, author, bio link
            for quote in quotes:
                text = quote.find(class_='text').get_text()
                author = quote.find(class_='author').get_text()
                bio_link = quote.find('a')['href']

                self.all_quotes.append({
                    'text': text,
                    'author': author,
                    'bio_link': bio_link,
                })

            # find next page
            next_btn = soup.find(class_='next')
            self.current_page = next_btn.find('a')['href'] if next_btn else None

    # write data to csv file
    def __write_to_file(self):
        with open('quote_data.csv', 'w', encoding="utf-8") as csv_file:
            csv_writer = writer(csv_file)
            csv_writer.writerow(['text', 'author', 'bio_link'])

            for quote in self.all_quotes:
                csv_writer.writerow([quote['text'], quote['author'], quote['bio_link']])

    def __play_game(self):
        quote = choice(self.all_quotes)
        remaining_guesses = 4
        print("Here's a quote: ")
        print(quote['text'])
        print(quote['author'])
        guess = ''

        while guess.lower() != quote['author'].lower() and remaining_guesses > 0:
            guess = input(f'Who said this quote? Guesses remaining: {remaining_guesses} \n')

            if guess.lower() == quote['author'].lower():
                print('YOU ARE AMAZING!!')
                play_status = input('Would you like to play again? y/n \n')
                if play_status.lower() == 'y':
                    self.__play_game()
                else:
                    print('Thanks for playing!!')
                break
            
            remaining_guesses -= 1
            if remaining_guesses == 3:
                res = requests.get(f"{self.BASE_URL}{quote['bio_link']}")
                soup = BeautifulSoup(res.text, "html.parser")
                birth_date = soup.find(class_="author-born-date").get_text()
                birth_place = soup.find(class_="author-born-location").get_text()
                print(f'HINT: Author was born on {birth_date}, {birth_place}')
            elif remaining_guesses == 2:
                print(f"HINT: Author's first name starts with {quote['author'][0]}")
            elif remaining_guesses == 1:
                last_initial = quote['author'].split(" ")[1][0]
                print(f"HINT: Author's last name starts with {last_initial}")
            else:
                print(f"The Author's name was {quote['author']}, sorry, you lose!")
                play_status = input('Would you like to play again? y/n \n')
                if play_status.lower() == 'y':
                    return self.__play_game()
                else:
                    print('Thanks for playing!!')


new_game = Game()
new_game.start() 