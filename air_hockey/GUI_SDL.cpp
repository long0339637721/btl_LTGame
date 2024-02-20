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
	_bat1 = IMG_LoadTexture(_rend, "res/bat.png");
	if (!_bat1)
	{
		std::cerr << "IMG error: " << IMG_GetError() << std::endl;
		exit(2);
	}
	_bat2 = IMG_LoadTexture(_rend, "res/puck.png");
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

	_music = Mix_LoadMUS("res/mus.mp3");
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

Event_en GUI_SDL::checkEvent()
{
	SDL_Event event;

	if (SDL_PollEvent(&event))
	{
		switch (event.type)
		{
		case SDL_QUIT:
			return esc;
		case SDL_MOUSEBUTTONUP:
		{
			if (event.button.button == SDL_BUTTON_LEFT)
			{
				if (event.button.y > 10 && event.button.y < 80
					&& event.button.x > 230 && event.button.x < 310)
					return pvp;
				if (event.button.y > 720 && event.button.y < 750
					&& event.button.x > 300 && event.button.x < 440)
					return dific;
				if (event.button.y > 660 && event.button.y < 740
					&& event.button.x > 170 && event.button.x < 250)
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
	_dst.x = 365;
	_dst.y = 10;
	_dst.h = 39;

	_dst.w = 21;
	_ttf = TTF_RenderText_Solid(_font, std::to_string(pieces[5].score).c_str(), _color);
	_text = SDL_CreateTextureFromSurface(_rend, _ttf);
	SDL_RenderCopy(_rend, _text, 0, &_dst);
	SDL_FreeSurface(_ttf);
	SDL_DestroyTexture(_text);


	_color = { BLUE_COLOR };
	_dst.y = 8;
	_dst.x = 405 ;
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
	SDL_RenderPresent(_rend);
}

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
}

void GUI_SDL::draw_field()
{
	SDL_DestroyTexture(_background);
	_background = IMG_LoadTexture(_rend, "res/field1.png");
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
	_background = IMG_LoadTexture(_rend, (x == 1 ? "res/bwin.png" : "res/rwin.png"));
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
