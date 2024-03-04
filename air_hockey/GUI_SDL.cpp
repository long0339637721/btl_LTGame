#include "GUI_SDL.hpp"
#include <string>


GUI_SDL::GUI_SDL()
{
	if (SDL_Init(SDL_INIT_AUDIO | SDL_INIT_VIDEO) < 0)
	{
		std::cerr << "SDL error: " << SDL_GetError() << std::endl;
		exit(1);
	}

	_win = SDL_CreateWindow("Tiny Football", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, WIDTH, HEIGHT, SDL_WINDOW_SHOWN);
	if (!_win)
	{
		std::cerr << "SDL error: " << SDL_GetError() << std::endl;
		exit(1);
	}

	_rend = SDL_CreateRenderer(_win, -1, SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC);
	if (!_rend)
	{
		std::cerr << "SDL error: " << SDL_GetError() << std::endl;
		exit(1);
	}

	load_ttf();
	load_img();
	load_sound();

	_src = { 0, 0, SIZE_PIECE, SIZE_PIECE };
}

void GUI_SDL::load_ttf()
{
	if (TTF_Init() < 0)
	{
		std::cerr << "TTF error: " << TTF_GetError() << std::endl;
		exit(3);
	}

	_font = TTF_OpenFont("res/abc.ttf", 45);

	if (!_font)
	{
		std::cerr << "TTF error: " << TTF_GetError() << std::endl;
		exit(3);
	}
}

void GUI_SDL::load_img()
{
	if (!(IMG_Init(IMG_INIT_PNG) & IMG_INIT_PNG) || !(IMG_Init(IMG_INIT_JPG) & IMG_INIT_JPG))
	{
		std::cerr << "IMG error: " << IMG_GetError() << std::endl;
		exit(2);
	}

	_ball = IMG_LoadTexture(_rend, "res/ball.png");
	if (!_ball)
	{
		std::cerr << "IMG error: " << IMG_GetError() << std::endl;
		exit(2);
	}
	_bat1 = IMG_LoadTexture(_rend, "res/red.png");
	if (!_bat1)
	{
		std::cerr << "IMG error: " << IMG_GetError() << std::endl;
		exit(2);
	}
	_bat2 = IMG_LoadTexture(_rend, "res/blue.png");
	if (!_bat2)
	{
		std::cerr << "IMG error: " << IMG_GetError() << std::endl;
		exit(2);
	}
}

void GUI_SDL::load_sound()
{
	if (Mix_OpenAudio(44100, MIX_DEFAULT_FORMAT, 2, 4096))
	{
		std::cerr << "MIX error: " << Mix_GetError() << std::endl;
		exit(4);
	}

	_music = Mix_LoadMUS("res/reverse_situation.mp3");
	if (!_music)
	{
		std::cerr << "MIX error: " << Mix_GetError() << std::endl;
		exit(4);
	}
	_board = Mix_LoadWAV("res/board.wav");
	if (!_board)
	{
		std::cerr << "MIX error: " << Mix_GetError() << std::endl;
		exit(4);
	}
	_hit = Mix_LoadWAV("res/hit.wav");
	if (!_hit)
	{
		std::cerr << "MIX error: " << Mix_GetError() << std::endl;
		exit(4);
	}
	_goal = Mix_LoadWAV("res/goal.wav");
	if (!_goal)
	{
		std::cerr << "MIX error: " << Mix_GetError() << std::endl;
		exit(4);
	}
	Mix_PlayMusic(_music, -1);
}

Event_en GUI_SDL::checkEvent(bool isSelectingGameMode, bool isSelectingDifficult)
{
	SDL_Event event;

	if (SDL_PollEvent(&event))
	{
		switch (event.type)
		{
		case SDL_QUIT:
			return esc;
		case SDL_KEYDOWN:
		{
			if (event.key.keysym.sym == SDLK_UP || event.key.keysym.sym == SDLK_DOWN)
				return btn_down_up;
			if (event.key.keysym.sym == SDLK_KP_ENTER || event.key.keysym.sym == SDLK_RETURN)
				return btn_enter;
		}
		case SDL_MOUSEBUTTONUP:
		{
			if (event.button.button == SDL_BUTTON_LEFT)
			{
				std::cout << event.button.x << ", " << event.button.y << std::endl;
				if (isSelectingGameMode && event.button.y > 675 && event.button.y < 715
					&& event.button.x > 130 && event.button.x < 350)
					return pvp;
				if (isSelectingDifficult && event.button.y > 605 && event.button.y < 645
					&& event.button.x > 140 && event.button.x < 340)
					return normal;
				if (isSelectingDifficult && event.button.y > 675 && event.button.y < 715
					&& event.button.x > 180 && event.button.x < 300)
					return hard;
				if (event.button.y > 605 && event.button.y < 645
					&& event.button.x > 140 && event.button.x < 340)
					return play;
				if (event.button.y > HEIGHT - 54 && event.button.x < 54)
					return mus;
			}
			if (event.button.button == SDL_BUTTON_RIGHT)
				return menu;
			break;
		}

		}
	}
	return nothing;
}

void GUI_SDL::draw(std::vector<piece>& pieces)
{
	SDL_RenderClear(_rend);
	SDL_RenderCopy(_rend, _background, NULL, NULL);

	_color = { RED_COLOR };
	_dst.x = 3;
	_dst.y = 360; 

	_dst.h = 31;
	_dst.w = 16;

	_ttf = TTF_RenderText_Solid(_font, std::to_string(pieces[5].score).c_str(), _color);
	_text = SDL_CreateTextureFromSurface(_rend, _ttf);
	SDL_RenderCopy(_rend, _text, 0, &_dst);
	SDL_FreeSurface(_ttf);
	SDL_DestroyTexture(_text);


	_color = { BLUE_COLOR };
	_dst.x = 3;
	_dst.y = 450 ;
	_ttf = TTF_RenderText_Solid(_font, std::to_string(pieces[6].score).c_str(), _color);
	_text = SDL_CreateTextureFromSurface(_rend, _ttf);
	SDL_RenderCopy(_rend, _text, 0, &_dst);
	SDL_FreeSurface(_ttf);
	SDL_DestroyTexture(_text);

	_dst.h = _dst.w = SIZE_BALL;
	_dst.x = pieces[0].x;
	_dst.y = pieces[0].y;
	SDL_RenderCopy(_rend, _ball, &_src, &_dst);

	_dst.h = _dst.w = SIZE_BAT;
	_dst.x = pieces[1].x;
	_dst.y = pieces[1].y;
	SDL_RenderCopy(_rend, _bat1, &_src, &_dst);

	_dst.x = pieces[3].x;
	_dst.y = pieces[3].y;
	SDL_RenderCopy(_rend, _bat1, &_src, &_dst);

	_dst.x = pieces[5].x;
	_dst.y = pieces[5].y;
	SDL_RenderCopy(_rend, _bat1, &_src, &_dst);

	_dst.x = pieces[2].x;
	_dst.y = pieces[2].y;
	SDL_RenderCopy(_rend, _bat2, &_src, &_dst);

	_dst.x = pieces[4].x;
	_dst.y = pieces[4].y;
	SDL_RenderCopy(_rend, _bat2, &_src, &_dst);

	_dst.x = pieces[6].x;
	_dst.y = pieces[6].y;
	SDL_RenderCopy(_rend, _bat2, &_src, &_dst);

	draw_dynamic();

	SDL_RenderPresent(_rend);
}
/*
void GUI_SDL::new_game(bool hard)
{
	SDL_DestroyTexture(_background);
	SDL_RenderClear(_rend);
	SDL_RenderCopy(_rend, _background, NULL, NULL);
	_background = IMG_LoadTexture(_rend, (hard ? "res/hard1.png" : "res/norm1.png"));
	if (!_background)
	{
		std::cerr << "IMG error: " << IMG_GetError() << std::endl;
		exit(2);
	}

	SDL_RenderClear(_rend);
	SDL_RenderCopy(_rend, _background, NULL, NULL);
	draw_dynamic();
	draw_game_mode_selection();
	SDL_RenderPresent(_rend);
} */

void GUI_SDL::new_game(bool isSelectingPvp, bool hard, bool isSelectingGameMode, bool isSelectingDifficulty)
{
	SDL_DestroyTexture(_background);
	_background = IMG_LoadTexture(_rend, "res/start_background.png");
	if (!_background)
	{
		std::cerr << "IMG error: " << IMG_GetError() << std::endl;
		exit(2);
	}

	SDL_RenderClear(_rend);
	SDL_RenderCopy(_rend, _background, NULL, NULL);
	draw_dynamic();
	if (isSelectingGameMode && !isSelectingDifficulty) {
		draw_game_mode_selection(isSelectingPvp);
	}
	if (!isSelectingGameMode && isSelectingDifficulty) {
		draw_difficulty_selection(hard);
	}
	
	SDL_RenderPresent(_rend);
}
/*
void GUI_SDL::countdown()
{
	//countdown
	for (int i = 3; i > 0; i--)
	{
		SDL_DestroyTexture(_background);
		_background = IMG_LoadTexture(_rend, ("res/" + std::to_string(i) + ".png").c_str());
		if (!_background)
		{
			std::cerr << "IMG error: " << IMG_GetError() << std::endl;
			exit(2);
		}
		SDL_RenderClear(_rend);
		SDL_RenderCopy(_rend, _background, NULL, NULL);
		SDL_RenderPresent(_rend);
		SDL_Delay(1000);
	}
} */

void GUI_SDL::clearRend()
{
	SDL_RenderClear(_rend);
}

void GUI_SDL::countdown(int count)
{
	_color = { 255, 0, 0 };
	_dst.y = 260;
	_dst.x = 190;
	_dst.h = 160;
	_dst.w = 100;
	switch (count)
	{
	case 3:
		_ttf = TTF_RenderText_Solid(_font, "3", _color);
		break;
	case 2:
		_ttf = TTF_RenderText_Solid(_font, "2", _color);
		break;
	case 1:
		_ttf = TTF_RenderText_Solid(_font, "1", _color);
		break;
	case 0:
		_ttf = TTF_RenderText_Solid(_font, "0", _color);
		break;
	}
	_text = SDL_CreateTextureFromSurface(_rend, _ttf);
	SDL_RenderCopy(_rend, _text, 0, &_dst);
	SDL_RenderPresent(_rend);
}

void GUI_SDL::draw_field(bool isHard)
{
	SDL_DestroyTexture(_background);
	if (isHard)
	{
		_background = IMG_LoadTexture(_rend, "res/field2.png");
	}
	else
	{
		_background = IMG_LoadTexture(_rend, "res/field1.jpg");
	}
	
	if (!_background)
	{
		std::cerr << "IMG error: " << IMG_GetError() << std::endl;
		exit(2);
	}
	SDL_RenderClear(_rend);
	SDL_RenderCopy(_rend, _background, NULL, NULL);
	SDL_RenderPresent(_rend);
}

void GUI_SDL::win(int x)
{
	//bwin.png rwin.png
	SDL_DestroyTexture(_background);
	SDL_RenderClear(_rend);
	SDL_RenderCopy(_rend, _background, NULL, NULL);
	_background = IMG_LoadTexture(_rend, (x == 1 ? "res/bluewin.jpg" : "res/redwin.jpg"));
	if (!_background)
	{
		std::cerr << "IMG error: " << IMG_GetError() << std::endl;
		exit(2);
	}

	SDL_RenderClear(_rend);
	SDL_RenderCopy(_rend, _background, NULL, NULL);
	SDL_RenderPresent(_rend);
}

bool GUI_SDL::change_noise()
{
	_noise = !_noise;
	if (_noise)
		Mix_ResumeMusic();
	else
		Mix_PauseMusic();
	return _noise;
}

void GUI_SDL::draw_difficulty_selection(bool hard)
{
	_color = { 102, 178, 255 };
	_dst.y = 510;
	_dst.x = 45;
	_dst.h = 70;
	_dst.w = 390;
	_ttf = TTF_RenderText_Solid(_font, "Select difficulty", _color);
	_text = SDL_CreateTextureFromSurface(_rend, _ttf);
	SDL_RenderCopy(_rend, _text, 0, &_dst);
	SDL_FreeSurface(_ttf);
	SDL_DestroyTexture(_text);

	_dst.y = 590;
	_dst.x = 140;
	_dst.h = 70;
	_dst.w = 200;
	_ttf = TTF_RenderText_Solid(_font, "Normal", _color);
	_text = SDL_CreateTextureFromSurface(_rend, _ttf);
	SDL_RenderCopy(_rend, _text, 0, &_dst);
	SDL_FreeSurface(_ttf);
	SDL_DestroyTexture(_text);

	_dst.y = 660;
	_dst.x = 180;
	_dst.h = 70;
	_dst.w = 120;
	_ttf = TTF_RenderText_Solid(_font, "Hard", _color);
	_text = SDL_CreateTextureFromSurface(_rend, _ttf);
	SDL_RenderCopy(_rend, _text, 0, &_dst);
	SDL_FreeSurface(_ttf);
	SDL_DestroyTexture(_text);

	if (!hard) {
		// Is selecting Normal
		_dst.y = 587;
		_dst.x = 110;
		_dst.h = 64;
		_dst.w = 24;
		_ttf = TTF_RenderText_Solid(_font, "<", _color);
		_text = SDL_CreateTextureFromSurface(_rend, _ttf);
		SDL_RenderCopy(_rend, _text, 0, &_dst);
		SDL_FreeSurface(_ttf);
		SDL_DestroyTexture(_text);

		_dst.y = 587;
		_dst.x = 347;
		_dst.h = 64;
		_dst.w = 24;
		_ttf = TTF_RenderText_Solid(_font, ">", _color);
		_text = SDL_CreateTextureFromSurface(_rend, _ttf);
		SDL_RenderCopy(_rend, _text, 0, &_dst);
		SDL_FreeSurface(_ttf);
		SDL_DestroyTexture(_text);
	}
	else {
		// Is selecting Hard
		_dst.y = 657;
		_dst.x = 150;
		_dst.h = 64;
		_dst.w = 24;
		_ttf = TTF_RenderText_Solid(_font, "<", _color);
		_text = SDL_CreateTextureFromSurface(_rend, _ttf);
		SDL_RenderCopy(_rend, _text, 0, &_dst);
		SDL_FreeSurface(_ttf);
		SDL_DestroyTexture(_text);

		_dst.y = 657;
		_dst.x = 307;
		_dst.h = 64;
		_dst.w = 24;
		_ttf = TTF_RenderText_Solid(_font, ">", _color);
		_text = SDL_CreateTextureFromSurface(_rend, _ttf);
		SDL_RenderCopy(_rend, _text, 0, &_dst);
		SDL_FreeSurface(_ttf);
		SDL_DestroyTexture(_text);
	}
}

void GUI_SDL::draw_game_mode_selection(bool pvp)
{
	_color = { 102, 178, 255 };
	_dst.y = 510;
	_dst.x = 45;
	_dst.h = 70;
	_dst.w = 390;
	_ttf = TTF_RenderText_Solid(_font, "Select game mode", _color);
	_text = SDL_CreateTextureFromSurface(_rend, _ttf);
	SDL_RenderCopy(_rend, _text, 0, &_dst);
	SDL_FreeSurface(_ttf);
	SDL_DestroyTexture(_text);

	_dst.y = 590;
	_dst.x = 140;
	_dst.h = 70;
	_dst.w = 200;
	_ttf = TTF_RenderText_Solid(_font, "1 player", _color);
	_text = SDL_CreateTextureFromSurface(_rend, _ttf);
	SDL_RenderCopy(_rend, _text, 0, &_dst);
	SDL_FreeSurface(_ttf);
	SDL_DestroyTexture(_text);

	_dst.y = 660;
	_dst.x = 130;
	_dst.h = 70;
	_dst.w = 220;
	_ttf = TTF_RenderText_Solid(_font, "2 players", _color);
	_text = SDL_CreateTextureFromSurface(_rend, _ttf);
	SDL_RenderCopy(_rend, _text, 0, &_dst);
	SDL_FreeSurface(_ttf);
	SDL_DestroyTexture(_text);

	if (!pvp) {
		// Is selecting 1 player
		_dst.y = 587;
		_dst.x = 110;
		_dst.h = 64;
		_dst.w = 24;
		_ttf = TTF_RenderText_Solid(_font, "<", _color);
		_text = SDL_CreateTextureFromSurface(_rend, _ttf);
		SDL_RenderCopy(_rend, _text, 0, &_dst);
		SDL_FreeSurface(_ttf);
		SDL_DestroyTexture(_text);

		_dst.y = 587;
		_dst.x = 347;
		_dst.h = 64;
		_dst.w = 24;
		_ttf = TTF_RenderText_Solid(_font, ">", _color);
		_text = SDL_CreateTextureFromSurface(_rend, _ttf);
		SDL_RenderCopy(_rend, _text, 0, &_dst);
		SDL_FreeSurface(_ttf);
		SDL_DestroyTexture(_text);
	}
	else {
		// Is selecting 2 players
		_dst.y = 657;
		_dst.x = 100;
		_dst.h = 64;
		_dst.w = 24;
		_ttf = TTF_RenderText_Solid(_font, "<", _color);
		_text = SDL_CreateTextureFromSurface(_rend, _ttf);
		SDL_RenderCopy(_rend, _text, 0, &_dst);
		SDL_FreeSurface(_ttf);
		SDL_DestroyTexture(_text);

		_dst.y = 657;
		_dst.x = 357;
		_dst.h = 64;
		_dst.w = 24;
		_ttf = TTF_RenderText_Solid(_font, ">", _color);
		_text = SDL_CreateTextureFromSurface(_rend, _ttf);
		SDL_RenderCopy(_rend, _text, 0, &_dst);
		SDL_FreeSurface(_ttf);
		SDL_DestroyTexture(_text);
	}
}

void GUI_SDL::draw_dynamic()
{
	_dynamic = IMG_LoadTexture(_rend, (_noise ? "res/on.png" : "res/mute.png"));
	if (!_dynamic)
	{
		std::cerr << "IMG error: " << IMG_GetError() << std::endl;
		exit(2);
	}
	_dst.h = _dst.w = SIZE_BAT;
	_dst.x = 2;
	_dst.y = HEIGHT - 50;
	SDL_RenderCopy(_rend, _dynamic, &_src, &_dst);
	SDL_DestroyTexture(_dynamic);
}

void GUI_SDL::play_sound(Collision s)
{
	if (!_noise)
		return;
	if (s == board)
		Mix_PlayChannel(-1, _board, 0);
	else if (s == hit)
		Mix_PlayChannel(-1, _hit, 0);
	else {
		Mix_PlayChannel(-1, _goal, 0);
		SDL_Delay(300);
	}
}

int GUI_SDL::getDirectionalAccumulation(int xVector1, int yVector1, int xVector2, int yVector2)
{
	return xVector1 * yVector2 - yVector1 * xVector2;
}

bool GUI_SDL::isAPBetweenABAndAC(bool isFirstTriangle, int xP, int yP)
{
	int vector1, vector2, vector3;
	if (isFirstTriangle)
	{
		vector1 = getDirectionalAccumulation(X_B1 - X_A1, Y_B1 - Y_A1, X_C1 - X_A1, Y_C1 - Y_A1);
		vector2 = getDirectionalAccumulation(X_B1 - X_A1, Y_B1 - Y_A1, xP - X_A1, yP - Y_A1);
		vector3 = getDirectionalAccumulation(xP - X_A1, yP - Y_A1, X_C1 - X_A1, Y_C1 - Y_A1);
	}
	else
	{
		vector1 = getDirectionalAccumulation(X_B2 - X_A2, Y_B2 - Y_A2, X_C2 - X_A2, Y_C2 - Y_A2);
		vector2 = getDirectionalAccumulation(X_B2 - X_A2, Y_B2 - Y_A2, xP - X_A2, yP - Y_A2);
		vector3 = getDirectionalAccumulation(xP - X_A2, yP - Y_A2, X_C2 - X_A2, Y_C2 - Y_A2);
	}
	
	if ((vector1 > 0 && vector2 > 0 && vector3 > 0) || (vector1 < 0 && vector2 < 0 && vector3 < 0))
	{
		return true;
	}
	else
	{
		return false;
	}
}

bool GUI_SDL::isAPBetweenCAAndCB(bool isFirstTriangle, int xP, int yP)
{
	int vector1, vector2, vector3;
	if (isFirstTriangle)
	{
		vector1 = getDirectionalAccumulation(X_B1 - X_C1, Y_B1 - Y_C1, X_A1 - X_C1, Y_A1 - Y_C1);
		vector2 = getDirectionalAccumulation(X_B1 - X_C1, Y_B1 - Y_C1, xP - X_C1, yP - Y_C1);
		vector3 = getDirectionalAccumulation(xP - X_C1, yP - Y_C1, X_A1 - X_C1, Y_A1 - Y_C1);
	}
	else 
	{
		vector1 = getDirectionalAccumulation(X_B2 - X_C2, Y_B2 - Y_C2, X_A2 - X_C2, Y_A2 - Y_C2);
		vector2 = getDirectionalAccumulation(X_B2 - X_C2, Y_B2 - Y_C2, xP - X_C2, yP - Y_C2);
		vector3 = getDirectionalAccumulation(xP - X_C2, yP - Y_C2, X_A2 - X_C2, Y_A2 - Y_C2);
	}
	
	if ((vector1 > 0 && vector2 > 0 && vector3 > 0) || (vector1 < 0 && vector2 < 0 && vector3 < 0))
	{
		return true;
	}
	else
	{
		return false;
	}
}

bool GUI_SDL::checkInArrow(int x, int y)
{
	if (((x >= 48) && (x <= 64) && (y >= 240) && (y <= 270)) || ((x >= 417) && (x <= 432) && (y >= 240) && (y <= 270)))
	{
		return true;
	}
	if ((x > X_A1) && (x < X_B1) && (y > Y_A1) && (y < Y_C1))
	{
		if (isAPBetweenABAndAC(true, x, y) && isAPBetweenCAAndCB(true, x, y))
		{
			return true;
		}
	}
	if ((x > X_A2) && (x < X_B2) && (y > Y_A2) && (y < Y_C2))
	{
		if (isAPBetweenABAndAC(false, x, y) && isAPBetweenCAAndCB(false, x, y))
		{
			return true;
		}
	}
	return false;
}

GUI_SDL::~GUI_SDL()
{
	SDL_DestroyTexture(_background);
	SDL_DestroyTexture(_ball);
	SDL_DestroyTexture(_bat1);
	SDL_DestroyTexture(_bat2);
	SDL_DestroyTexture(_dynamic);
	SDL_DestroyTexture(_text);
	TTF_CloseFont(_font);
	Mix_FreeMusic(_music);
	Mix_FreeChunk(_board);
	Mix_FreeChunk(_hit);
	Mix_FreeChunk(_goal);
	SDL_DestroyRenderer(_rend);
	SDL_DestroyWindow(_win);
	Mix_CloseAudio();
	Mix_Quit();
	TTF_Quit();
	SDL_Quit();
}
