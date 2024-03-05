#include <iostream>
#include <array>
#include <vector>
#include <random>
#include <Windows.h>
#include <algorithm>
class Game
{
public:
	Game()
		: m_errors{ 0 }, m_deleted_from_temp_word{ 0 }, m_words{ "энциклопедия", "абстененция", "эксгумация" }
	{}
	void play()
	{
		std::cout << "Добро пожаловать в игру \"Виселица\"!\n";
		m_word = get_random_word();
		m_temp_word = m_word;
		bool right{ false };
		do
		{
			print_hiden_word(right);
			char letter{ set_letter() };
			int result = is_found(letter);
			if (result == 1)
				right = true;
			else if (result == 0)
			{
				right = false;
			}
			else
			{
				right = false;
				m_errors++;
				if (m_errors < 6)
					std::cout << "Неверно! Такой буквы нет, у вас осталось " << 6 - m_errors << " попыток неверно указать букву!\n";
			}
		} while (m_word.size() != m_found_positions.size() && m_errors != 6);
		if (m_errors == 6)
		{
			std::cout << "Вы проиграли!\n";
			std::cout << "Загаданное слово: " << m_word << "\n";
			play_again();
		}
		else
		{
			std::cout << "Вы выиграли!\n";
			std::cout << "Загаданное слово: " << m_word << '\n';
			play_again();
		}
	}
private:
	int m_errors, m_deleted_from_temp_word;
	std::array <std::string, 3> m_words;
	std::vector <int> m_found_positions;
	std::string m_word, m_temp_word;
	std::string get_random_word()
	{
		std::mt19937 mercene_vortex(std::random_device{}());
		return m_words.at(mercene_vortex() % (m_words.size()));
	}
	void print_hiden_word(bool right)
	{
		if (m_found_positions.size() == 0 || !right)
			std::cout << "Слово - ";
		else
			std::cout << "Верно - ";
		for (int i = 0; i < m_word.size(); i++)
		{
			auto iter = std::find(m_found_positions.begin(), m_found_positions.end(), i);
			if (iter != m_found_positions.end())
				std::cout << m_word.at(*iter);
			else
				std::cout << "_";
		}
		std::cout << "\n";
	}
	char set_letter()
	{
		char choise;
		do
		{
			std::cout << "Угадайте букву: ";
			std::cin >> choise;
			std::cin.clear();
			std::cin.ignore(32767, '\n');
		} while (choise<-32 && choise>-1);
		return choise;
	}
	//Если буква найдена = 1, если не найдена = -1, если не найденна, но из повторяющихся = 0
	int is_found(char letter)
	{
		auto iter_word = std::find(m_word.begin(), m_word.end(), letter);
		if (iter_word == m_word.end())
		{
			return -1;
		}
		else
		{
			int pos = static_cast <int> (iter_word - m_word.begin());
			auto iter_pos = std::find(m_found_positions.begin(), m_found_positions.end(), pos);
			if (iter_pos == m_found_positions.end())
			{
				m_found_positions.push_back(pos);
				m_temp_word.erase(std::find(m_temp_word.begin(), m_temp_word.end(), m_word.at(pos)));
				m_deleted_from_temp_word++;
				return 1;
			}
			else
			{
				auto iter = std::find(m_temp_word.begin(), m_temp_word.end(), m_word.at(pos));
				if (iter != m_temp_word.end())
				{
					int p = static_cast <int>(iter - m_temp_word.begin());
					m_found_positions.push_back(p + m_deleted_from_temp_word);
					m_temp_word.erase(m_temp_word.begin() + p);
					m_deleted_from_temp_word++;
					return 1;
				}
				else
					return 0;
			}
		}
	}
	void play_again()
	{
		char choise;
		do
		{
			std::cout << "Хотите сыграть еще? (д/н): ";
			std::cin >> choise;
			std::cin.clear();
			std::cin.ignore(32767, '\n');
		} while (choise != 'д' && choise != 'н');
		if (choise == 'д')
		{
			m_errors = 0;
			m_deleted_from_temp_word = 0;
			m_found_positions.erase(m_found_positions.begin(), m_found_positions.end());
			play();
		}
		else
			exit(0);
	}
};
int main()
{
	setlocale(LC_ALL, "russian");
	SetConsoleCP(1251);
	SetConsoleOutputCP(1251);
	Game().play();
	return 0;
}