#include "game.hpp"

TinyFootball::TinyFootball() : _lib(new GUI_SDL)
{
	_pieces.resize(7); // 0,1,2 - bot, 3,4,5 - player, 6 - ball
	t1 = tplayer;
	t2 = tbot;
}

void TinyFootball::setgame(type_piece t1, type_piece t2) 
{
	this->t1 = t1;
	this->t2 = t2;
}

TinyFootball::~TinyFootball() { }

void TinyFootball::begin_pos()
{
	double hei = (HEIGHT - SIZE_BAT) / 2;
	double wid = (WIDTH - SIZE_BAT) / 2;

	_lib->countdown();
	_lib->draw_field();

	_pieces[1] = { tbot, _pieces[1].score, wid - 50, hei / 2 + 20, wid - 50, hei / 2 + 20, 0, 0 };
	_pieces[3] = { tbot, _pieces[3].score, wid + 50, hei / 2 - 20, wid + 50, hei / 2 - 20 , 0, 0 };
	_pieces[5] = { tbot, _pieces[5].score, wid , hei / 2 - 50, wid , hei / 2 - 50, 0, 0 };
	_pieces[2] = { tbot, _pieces[2].score, wid - 50, hei + hei / 2 + 20, wid - 50, hei + hei / 2 + 20, 0, 0 };
	_pieces[4] = { tbot, _pieces[4].score, wid + 50,hei + hei / 2 - 20, wid + 50, hei + hei / 2 - 20 , 0, 0 };
	_pieces[6] = { tbot, _pieces[6].score, wid, hei + hei / 2 + 50, wid, hei + hei / 2 + 50, 0, 0 };
	_pieces[0] = { tball ,0, wid + 2, hei, wid + 2, hei, 0, 0 };
}

void TinyFootball::hit_ball(int type)
{
	piece& bat = _pieces[type];
	piece& ball = _pieces[tball];

	int bit = 1 + abs(abs(bat.xs) > abs(bat.ys) ? bat.xs : bat.ys) / SIZE_BAT * 2;
	double jumpX = bat.xs / bit, jumpY = bat.ys / bit;

	bool hits = false;
	while (bit)
	{
		bat.xp += jumpX;
		bat.yp += jumpY;

		if (pow(SIZE_BALL, 2) > pow(bat.xp - ball.x, 2) + pow(bat.yp - ball.y, 2))
		{
			if (!hits)
			{
				hits = true;
				double hyp = hypot(bat.xp - ball.x, bat.yp - ball.y);
				double sin = (bat.yp - ball.y) / hyp;
				double cos = (ball.x - bat.xp) / hyp;
				double nSpeed = ball.xs * cos - ball.ys * sin;
				double tSpeed = ball.xs * sin + ball.ys * cos;
				nSpeed = -nSpeed;

				ball.xs = tSpeed * sin  + nSpeed * cos + bat.xs*2;
				ball.ys = tSpeed * cos - nSpeed * sin + bat.ys*2;

				while (pow(MAX_SPEED, 2) < pow(ball.xs, 2) + pow(ball.ys, 2))
				{
					ball.xs *= 0.6;
					ball.ys *= 0.6;
				}
			}
			ball.x += ball.xs;
			ball.y += ball.ys;
		}
		--bit;
	}
	if (hits)
		std::cout << "hit \n";
	//_lib->play_sound(hit);
}

void TinyFootball::behav_ball()
{
	piece& ball = _pieces[tball];

	int wid = WIDTH - SIZE_BALL - 20, hei = HEIGHT - SIZE_BALL - 55;

	ball.x += ball.xs;
	ball.y += ball.ys;

	hit_ball(1);
	hit_ball(2);
	hit_ball(3);
	hit_ball(4);
	hit_ball(5);
	hit_ball(6);

	//boards
	if (ball.x > wid || ball.x < 20)
	{
		ball.x = (ball.x > wid ? wid * 2 - ball.x : 40 - ball.x);
		ball.xs *= -1;
		_lib->play_sound(board);
	}
	if (ball.y > hei || ball.y < 55)
	{
		//goal
		if (ball.x > 180 && ball.x < 262)
		{
			_pieces[(ball.y > hei ? 5 : 6)].score++;
			ball.y = (ball.y > hei ? hei : 55);
			extrude();
			_lib->draw(_pieces);
			_lib->play_sound(goal);
			
			if (_pieces[5].score == 3) {
				_lib->win(0);
				SDL_Delay(5000);
				_pieces[5].score = 0; _pieces[6].score = 0;
				_pvc = _pvp = false;
				_lib->new_game(_hard);
			}
			else if (_pieces[6].score == 3) {
				_lib->win(1);
				SDL_Delay(5000);
				_pieces[5].score = 0; _pieces[6].score = 0;
				_pvc = _pvp = false;
				_lib->new_game(_hard);
			}
			else begin_pos();

			return;
		}
		ball.y = (ball.y > hei ? hei * 2 - ball.y : 110 - ball.y);
		ball.ys *= -1;
		_lib->play_sound(board);

	}
	extrude();

	// deceleration
	ball.xs *= 0.99;
	ball.ys *= 0.99;
	if (abs(ball.xs) < 0.7 && abs(ball.ys) < 0.7)
	{
		ball.xs = 0;
		ball.ys = 0;
	}
}

void TinyFootball::extrude()
{
	piece& player = _pieces[tplayer];
	piece& bot = _pieces[tbot];
	piece& ball = _pieces[tball];
	int d = pow(SIZE_BALL, 2);

	while (true)
	{
		if (d > pow(bot.x - ball.x, 2) + pow(bot.y - ball.y, 2))
		{
			bot.x -= bot.xs * 0.1;
			bot.y -= bot.ys * 0.1;
		}
		else if (d > pow(player.x - ball.x, 2) + pow(player.y - ball.y, 2))
		{
			player.x -= player.xs * 0.1;
			player.y -= player.ys * 0.1;
		}
		else
			break;
	}
}

void TinyFootball::confines(int type)
{
	piece& bat = _pieces[type];
	//left player
	if (type == 1 || type == 2) {
		if (bat.x > (WIDTH - SIZE_BAT)/2)
		{
			//_lib->play_sound(board);
			bat.x = (WIDTH - SIZE_BAT) / 2;
		}
		if (bat.x < WID_BORDER)
		{
			//_lib->play_sound(board);
			bat.x = WID_BORDER;
		}
		if (bat.y > HEIGHT - (SIZE_BAT / 2) - HEI_BORDER)
		{
			//_lib->play_sound(board);
			bat.y = HEIGHT - (SIZE_BAT) / 2 - HEI_BORDER;
		}
		if (bat.y < (SIZE_BAT / 2) + HEI_BORDER)
		{
			//_lib->play_sound(board);
			bat.y = (SIZE_BAT / 2) + HEI_BORDER;
		}
	}
	//right player
	if (type == 3 || type == 4) {
		if (bat.x > (WIDTH - WID_BORDER - SIZE_BAT))
		{
			//_lib->play_sound(board);
			bat.x = (WIDTH - WID_BORDER - SIZE_BAT);
		}
		if (bat.x < (WIDTH + SIZE_BAT) / 2)
		{
			//_lib->play_sound(board);
			bat.x = (WIDTH + SIZE_BAT) / 2;
		}
		if (bat.y > HEIGHT - (SIZE_BAT / 2) - HEI_BORDER)
		{
			//_lib->play_sound(board);
			bat.y = HEIGHT - (SIZE_BAT) / 2 - HEI_BORDER;
		}
		if (bat.y < (SIZE_BAT / 2) + HEI_BORDER)
		{
			//_lib->play_sound(board);
			bat.y = (SIZE_BAT / 2) + HEI_BORDER;
		}
	}
	//red gk
	else if (type == 5) {
		if (bat.x > (WIDTH / 2 + 100))
		{
			//_lib->play_sound(board);
			bat.x = (WIDTH / 2 + 100);
		}
		if (bat.x < (WIDTH / 2 - 100 - SIZE_BAT))
		{
			//_lib->play_sound(board);
			bat.x = (WIDTH / 2 - 100 - SIZE_BAT);
		}
		if (bat.y < (HEI_BORDER))
		{
			//_lib->play_sound(board);
			bat.y = (HEI_BORDER);
		}
		if (bat.y > (HEI_BORDER + 100))
		{
			//_lib->play_sound(board);
			bat.y = (HEI_BORDER + 100);
		}
	}
	//blue gk
	else if (type == 6) {
		if (bat.x > (WIDTH / 2 + 100))
		{
			//_lib->play_sound(board);
			bat.x = (WIDTH / 2 + 100);
		}
		if (bat.x < (WIDTH / 2 - 100 - SIZE_BAT))
		{
			//_lib->play_sound(board);
			bat.x = (WIDTH / 2 - 100 - SIZE_BAT);
		}
		if (bat.y > (HEIGHT - HEI_BORDER - SIZE_BAT))
		{
			//_lib->play_sound(board);
			bat.y = (HEIGHT - HEI_BORDER - SIZE_BAT);
		}
		if (bat.y < (HEIGHT - HEI_BORDER - SIZE_BAT - 100))
		{
			//_lib->play_sound(board);
			bat.y = (HEIGHT - HEI_BORDER - SIZE_BAT - 100);
		}
	}

	bat.xs = bat.x - bat.xp;
	bat.ys = bat.y - bat.yp;
}

void TinyFootball::behav_bot()
{

	/*std::vector<piece> & pieces{ _pieces[tbot], _pieces[tbot + 2] ,_pieces[tbot + 4] ,_pieces[tplayer + 2],_pieces[tplayer + 4],_pieces[tball] };*/
	piece& ball = _pieces[0];

	for (int i = 1; i <= 6; i++) {
		double speed = (_hard ? MAX_SPEED / 3 : MAX_SPEED / 6);
		if (_pieces[i].type == tplayer) continue;
		_pieces[i].xp = _pieces[i].x;
		_pieces[i].yp = _pieces[i].y;

		double preX = ball.x + ball.xs;
		double preY = ball.y + ball.ys;

		double distance, distY;
		distance = abs(preX - _pieces[i].x);
		distY = preY - _pieces[i].y;

		_pieces[i].xs = (speed < distance +(i%2 ==0 ? -15 : +15) ? speed : distance) * (preX < _pieces[i].x ? -1 : 1);

		if (i % 2 == 1) {
			if (preY > HEIGHT / 2) {
				_pieces[i].ys -= (_pieces[i].y - speed > 75 ? speed : 0);
			}
			if (preY < _pieces[i].y + SIZE_BAT / 2)
				_pieces[i].ys = -speed;
			else if (distY > distance || speed > distance - SIZE_BALL / 2)
				_pieces[i].ys = (speed < distY ? speed : distY);
			else
				_pieces[i].ys = distY / (distance / speed);
		}
		else {
			if (preY < HEIGHT / 2) {
				_pieces[i].ys += (_pieces[i].y - speed > 75 ? speed : 0);
			}
			if (preY > _pieces[i].y + SIZE_BAT / 2)
				_pieces[i].ys = speed;
			else if (distY > distance || speed > distance - SIZE_BALL / 2)
				_pieces[i].ys = (speed < distY ? speed : distY);
			else
				_pieces[i].ys = distY / (distance / speed);
		}



		speed *= speed;
		while (speed < pow(_pieces[i].xs, 2) + pow(_pieces[i].ys, 2))
		{
			_pieces[i].xs *= 0.8;
			_pieces[i].ys *= 0.8;
		}
		_pieces[i].x += _pieces[i].xs;
		_pieces[i].y += _pieces[i].ys;

		confines(i);
	}

}

void TinyFootball::start()
{
	_lib->new_game(_hard);
	int player[2] = {5,6};
	bool quit = false;
	while (!quit)
	{
		SDL_Event e;
		//movement handler
		while (!quit) {
			while (SDL_PollEvent(&e) != 0) {
				//quit
				if (e.type == SDL_QUIT) {
					quit = true;
					std::cout << "quit \n";
				}
			}

			// menu handler
			_event = _lib->checkEvent();
			switch (_event)
			{
			case nothing:
				break;
			case esc:
				return;
			case pvp:
				if (!_pvp)
				{
					_pvc = true;
					_pvp = true;
					setgame(tplayer, tplayer);
					begin_pos();
					//draw field
					_lib->draw_field();
				}
				break;
			case play:
				if (!_pvc)
				{
					_pvp = false;
					_pvc = true;
					setgame(tplayer, tbot);
					begin_pos();

					//draw field
					_lib->draw_field();
				}
				break;
			case dific:
				if (!_pvc)
				{
					_hard = !_hard;
					_lib->new_game(_hard);
				}
				break;
			case mus:
				_mute = _lib->change_noise();
				if (_pvc){
					_lib->new_game(_hard);
					break;
				}
			case menu:
				if (_pvc)
				{
					_pvc = false;
					_pieces[5].score = 0;
					_pieces[6].score = 0;
					_lib->new_game(_hard);
				}
				break;
			}

			//init keystate pointer
			const Uint8* currentKeyStates = SDL_GetKeyboardState(NULL);
			//movement handler
			if (_pvc) {
				if (currentKeyStates[SDL_SCANCODE_W])
				{
					_pieces[player[1]].xp = _pieces[player[1]].x;
					_pieces[player[1]].yp = _pieces[player[1]].y;
					_pieces[player[1]].y -= (_hard ? MAX_SPEED / 3 : MAX_SPEED / 4);
					//w_pressed = true;
					//std::cout << "up1 \n";
					if (currentKeyStates[SDL_SCANCODE_D])
					{
						//moving diagonally up-right
						_pieces[player[1]].xp = _pieces[player[1]].x;
						_pieces[player[1]].yp = _pieces[player[1]].y;
						_pieces[player[1]].x += (_hard ? MAX_SPEED / 3 : MAX_SPEED / 4);
						//std::cout << "up-right1 \n";
					}
					else if (currentKeyStates[SDL_SCANCODE_A])
					{
						//moving diagonally up-left
						_pieces[player[1]].xp = _pieces[player[1]].x;
						_pieces[player[1]].yp = _pieces[player[1]].y;
						_pieces[player[1]].x -= (_hard ? MAX_SPEED / 3 : MAX_SPEED / 4);
						//std::cout << "up-left1 \n";
					}
					else if (currentKeyStates[SDL_SCANCODE_J]) {
						_pieces[player[1]].type = tbot;
						player[1] = 2;
						_pieces[player[1]].type = tplayer;
						std::cout << "change player[1][2] \n";
					}
					else if (currentKeyStates[SDL_SCANCODE_K]) {
						_pieces[player[1]].type = tbot;
						player[1] = 6;
						_pieces[player[1]].type = tplayer;
						//std::cout << "change player[1][6] \n";
					}
					else if (currentKeyStates[SDL_SCANCODE_L]) {
						_pieces[player[1]].type = tbot;
						player[1] = 4;
						_pieces[player[1]].type = tplayer;
						//std::cout << "change player[1] \n";
					}
				}
				else if (currentKeyStates[SDL_SCANCODE_D])
				{
					_pieces[player[1]].xp = _pieces[player[1]].x;
					_pieces[player[1]].yp = _pieces[player[1]].y;
					_pieces[player[1]].x += (_hard ? MAX_SPEED / 3 : MAX_SPEED / 4);
					//d_pressed = true;
					//std::cout << "right1 \n";
					if (currentKeyStates[SDL_SCANCODE_W])
					{
						//moving diagonally up-right
						_pieces[player[1]].xp = _pieces[player[1]].x;
						_pieces[player[1]].yp = _pieces[player[1]].y;
						_pieces[player[1]].y -= (_hard ? MAX_SPEED / 3 : MAX_SPEED / 4);
						//std::cout << "up-right1 \n";
					}
					else if (currentKeyStates[SDL_SCANCODE_S])
					{
						//moving diagonally down-right
						_pieces[player[1]].xp = _pieces[player[1]].x;
						_pieces[player[1]].yp = _pieces[player[1]].y;
						_pieces[player[1]].y += (_hard ? MAX_SPEED / 3 : MAX_SPEED / 4);
						//std::cout << "down-right1 \n";
					}
					else if (currentKeyStates[SDL_SCANCODE_J]) {
						_pieces[player[1]].type = tbot;
						player[1] = 2;
						_pieces[player[1]].type = tplayer;
						//std::cout << "change player[1][2] \n";
					}
					else if (currentKeyStates[SDL_SCANCODE_K]) {
						_pieces[player[1]].type = tbot;
						player[1] = 6;
						_pieces[player[1]].type = tplayer;
						//std::cout << "change player[1][6] \n";
					}
					else if (currentKeyStates[SDL_SCANCODE_L]) {
						_pieces[player[1]].type = tbot;
						player[1] = 4;
						_pieces[player[1]].type = tplayer;
						//std::cout << "change player[1][1] \n";
					}
				}
				else if (currentKeyStates[SDL_SCANCODE_S])
				{
					_pieces[player[1]].xp = _pieces[player[1]].x;
					_pieces[player[1]].yp = _pieces[player[1]].y;
					_pieces[player[1]].y += (_hard ? MAX_SPEED / 3 : MAX_SPEED / 4);
					//s_pressed = true;
					//std::cout << "down1 \n";
					if (currentKeyStates[SDL_SCANCODE_D])
					{
						//moving diagonally down-right
						_pieces[player[1]].xp = _pieces[player[1]].x;
						_pieces[player[1]].yp = _pieces[player[1]].y;
						_pieces[player[1]].x += (_hard ? MAX_SPEED / 3 : MAX_SPEED / 4);
						//std::cout << "down-right1 \n";
					}
					else if (currentKeyStates[SDL_SCANCODE_A])
					{
						//moving diagonally down-left
						_pieces[player[1]].xp = _pieces[player[1]].x;
						_pieces[player[1]].yp = _pieces[player[1]].y;
						_pieces[player[1]].x -= (_hard ? MAX_SPEED / 3 : MAX_SPEED / 4);
						//std::cout << "down-left1 \n";
					}
					else if (currentKeyStates[SDL_SCANCODE_J]) {
						_pieces[player[1]].type = tbot;
						player[1] = 2;
						_pieces[player[1]].type = tplayer;
						//std::cout << "change player[2] \n";
					}
					else if (currentKeyStates[SDL_SCANCODE_K]) {
						_pieces[player[1]].type = tbot;
						player[1] = 6;
						_pieces[player[1]].type = tplayer;
						//std::cout << "change player[6] \n";
					}
					else if (currentKeyStates[SDL_SCANCODE_L]) {
						_pieces[player[1]].type = tbot;
						player[1] = 4;
						_pieces[player[1]].type = tplayer;
						//std::cout << "change player[1] \n";
					}
				}
				else if (currentKeyStates[SDL_SCANCODE_A])
				{
					_pieces[player[1]].xp = _pieces[player[1]].x;
					_pieces[player[1]].yp = _pieces[player[1]].y;
					_pieces[player[1]].x -= (_hard ? MAX_SPEED / 3 : MAX_SPEED / 4);
					//a_pressed = true;
					//std::cout << "left1 \n";
					if (currentKeyStates[SDL_SCANCODE_W])
					{
						//moving diagonally up-left
						_pieces[player[1]].xp = _pieces[player[1]].x;
						_pieces[player[1]].yp = _pieces[player[1]].y;
						_pieces[player[1]].y -= (_hard ? MAX_SPEED / 3 : MAX_SPEED / 4);
						//std::cout << "up-left1 \n";
					}
					else if (currentKeyStates[SDL_SCANCODE_S])
					{
						//moving diagonally down-left
						_pieces[player[1]].xp = _pieces[player[1]].x;
						_pieces[player[1]].yp = _pieces[player[1]].y;
						_pieces[player[1]].y += (_hard ? MAX_SPEED / 3 : MAX_SPEED / 4);
						//std::cout << "down-left1 \n";
					}
					else if (currentKeyStates[SDL_SCANCODE_J]) {
						_pieces[player[1]].type = tbot;
						player[1] = 2;
						_pieces[player[1]].type = tplayer;
						//std::cout << "change player[1][2] \n";
					}
					else if (currentKeyStates[SDL_SCANCODE_K]) {
						_pieces[player[1]].type = tbot;
						player[1] = 6;
						_pieces[player[1]].type = tplayer;
						//std::cout << "change player[6] \n";
					}
					else if (currentKeyStates[SDL_SCANCODE_L]) {
						_pieces[player[1]].type = tbot;
						player[1] = 4;
						_pieces[player[1]].type = tplayer;
						//std::cout << "change player \n";
					}
				}
				else if (currentKeyStates[SDL_SCANCODE_J]) {
					_pieces[player[1]].type = tbot;
					player[1] = 2;
					_pieces[player[1]].type = tplayer;
					//std::cout << "change player[2] \n";
				}
				else if (currentKeyStates[SDL_SCANCODE_K]) {
					_pieces[player[1]].type = tbot;
					player[1] = 6;
					_pieces[player[1]].type = tplayer;
					//std::cout << "change player[6] \n";
				}
				else if (currentKeyStates[SDL_SCANCODE_L]) {
					_pieces[player[1]].type = tbot;
					player[1] = 4;
					_pieces[player[1]].type = tplayer;
					//std::cout << "change player[4] \n";
				}

				if (_pvp) {
					if (currentKeyStates[SDL_SCANCODE_UP])
					{
						_pieces[player[0]].xp = _pieces[player[0]].x;
						_pieces[player[0]].yp = _pieces[player[0]].y;
						_pieces[player[0]].y -= (_hard ? MAX_SPEED / 3 : MAX_SPEED / 4);
						//w_pressed = true;
						//std::cout << "up1 \n";
						if (currentKeyStates[SDL_SCANCODE_DOWN])
						{
							//moving diagonally up-right
							_pieces[player[0]].xp = _pieces[player[0]].x;
							_pieces[player[0]].yp = _pieces[player[0]].y;
							_pieces[player[0]].x += (_hard ? MAX_SPEED / 3 : MAX_SPEED / 4);
							//std::cout << "up-right1 \n";
						}
						else if (currentKeyStates[SDL_SCANCODE_LEFT])
						{
							//moving diagonally up-left
							_pieces[player[0]].xp = _pieces[player[0]].x;
							_pieces[player[0]].yp = _pieces[player[0]].y;
							_pieces[player[0]].x -= (_hard ? MAX_SPEED / 3 : MAX_SPEED / 4);
							//std::cout << "up-left1 \n";
						}
						else if (currentKeyStates[SDL_SCANCODE_KP_1]) {
							_pieces[player[0]].type = tbot;
							player[0] = 1;
							_pieces[player[0]].type = tplayer;
							//std::cout << "change player[0][2] \n";
						}
						else if (currentKeyStates[SDL_SCANCODE_KP_2]) {
							_pieces[player[0]].type = tbot;
							player[0] = 5;
							_pieces[player[0]].type = tplayer;
							//std::cout << "change player[0][6] \n";
						}
						else if (currentKeyStates[SDL_SCANCODE_KP_3]) {
							_pieces[player[0]].type = tbot;
							player[0] = 3;
							_pieces[player[0]].type = tplayer;
							//std::cout << "change player[0] \n";
						}
					}
					else if (currentKeyStates[SDL_SCANCODE_RIGHT])
					{
						_pieces[player[0]].xp = _pieces[player[0]].x;
						_pieces[player[0]].yp = _pieces[player[0]].y;
						_pieces[player[0]].x += (_hard ? MAX_SPEED / 3 : MAX_SPEED / 4);
						//d_pressed = true;
						//std::cout << "right1 \n";
						if (currentKeyStates[SDL_SCANCODE_UP])
						{
							//moving diagonally up-right
							_pieces[player[0]].xp = _pieces[player[0]].x;
							_pieces[player[0]].yp = _pieces[player[0]].y;
							_pieces[player[0]].y -= (_hard ? MAX_SPEED / 3 : MAX_SPEED / 4);
							//std::cout << "up-right1 \n";
						}
						else if (currentKeyStates[SDL_SCANCODE_DOWN])
						{
							//moving diagonally down-right
							_pieces[player[0]].xp = _pieces[player[0]].x;
							_pieces[player[0]].yp = _pieces[player[0]].y;
							_pieces[player[0]].y += (_hard ? MAX_SPEED / 3 : MAX_SPEED / 4);
							//std::cout << "down-right1 \n";
						}
						else if (currentKeyStates[SDL_SCANCODE_KP_1]) {
							_pieces[player[0]].type = tbot;
							player[0] = 1;
							_pieces[player[0]].type = tplayer;
							//std::cout << "change player[0][2] \n";
						}
						else if (currentKeyStates[SDL_SCANCODE_KP_2]) {
							_pieces[player[0]].type = tbot;
							player[0] = 5;
							_pieces[player[0]].type = tplayer;
							//std::cout << "change player[0][6] \n";
						}
						else if (currentKeyStates[SDL_SCANCODE_KP_3]) {
							_pieces[player[0]].type = tbot;
							player[0] = 3;
							_pieces[player[0]].type = tplayer;
							//std::cout << "change player[0] \n";
						}
					}
					else if (currentKeyStates[SDL_SCANCODE_DOWN])
					{
						_pieces[player[0]].xp = _pieces[player[0]].x;
						_pieces[player[0]].yp = _pieces[player[0]].y;
						_pieces[player[0]].y += (_hard ? MAX_SPEED / 3 : MAX_SPEED / 4);
						//s_pressed = true;
						//std::cout << "down1 \n";
						if (currentKeyStates[SDL_SCANCODE_RIGHT])
						{
							//moving diagonally down-right
							_pieces[player[0]].xp = _pieces[player[0]].x;
							_pieces[player[0]].yp = _pieces[player[0]].y;
							_pieces[player[0]].x += (_hard ? MAX_SPEED / 3 : MAX_SPEED / 4);
							//std::cout << "down-right1 \n";
						}
						else if (currentKeyStates[SDL_SCANCODE_LEFT])
						{
							//moving diagonally down-left
							_pieces[player[0]].xp = _pieces[player[0]].x;
							_pieces[player[0]].yp = _pieces[player[0]].y;
							_pieces[player[0]].x -= (_hard ? MAX_SPEED / 3 : MAX_SPEED / 4);
							//std::cout << "down-left1 \n";
						}
						else if (currentKeyStates[SDL_SCANCODE_KP_1]) {
							_pieces[player[0]].type = tbot;
							player[0] = 1;
							_pieces[player[0]].type = tplayer;
							//std::cout << "change player[0][2] \n";
						}
						else if (currentKeyStates[SDL_SCANCODE_KP_2]) {
							_pieces[player[0]].type = tbot;
							player[0] = 5;
							_pieces[player[0]].type = tplayer;
							//std::cout << "change player[0][6] \n";
						}
						else if (currentKeyStates[SDL_SCANCODE_KP_3]) {
							_pieces[player[0]].type = tbot;
							player[0] = 3;
							_pieces[player[0]].type = tplayer;
							//std::cout << "change player[0] \n";
						}
					}
					else if (currentKeyStates[SDL_SCANCODE_LEFT])
					{
						_pieces[player[0]].xp = _pieces[player[0]].x;
						_pieces[player[0]].yp = _pieces[player[0]].y;
						_pieces[player[0]].x -= (_hard ? MAX_SPEED / 3 : MAX_SPEED / 4);
						//a_pressed = true;
						//std::cout << "left1 \n";
						if (currentKeyStates[SDL_SCANCODE_UP])
						{
							//moving diagonally up-left
							_pieces[player[0]].xp = _pieces[player[0]].x;
							_pieces[player[0]].yp = _pieces[player[0]].y;
							_pieces[player[0]].y -= (_hard ? MAX_SPEED / 3 : MAX_SPEED / 4);
							//std::cout << "up-left1 \n";
						}
						else if (currentKeyStates[SDL_SCANCODE_DOWN])
						{
							//moving diagonally down-left
							_pieces[player[0]].xp = _pieces[player[0]].x;
							_pieces[player[0]].yp = _pieces[player[0]].y;
							_pieces[player[0]].y += (_hard ? MAX_SPEED / 3 : MAX_SPEED / 4);
							//std::cout << "down-left1 \n";
						}
						else if (currentKeyStates[SDL_SCANCODE_KP_1]) {
							_pieces[player[0]].type = tbot;
							player[0] = 1;
							_pieces[player[0]].type = tplayer;
							//std::cout << "change player[0][2] \n";
						}
						else if (currentKeyStates[SDL_SCANCODE_KP_2]) {
							_pieces[player[0]].type = tbot;
							player[0] = 5;
							_pieces[player[0]].type = tplayer;
							//std::cout << "change player[0][6] \n";
						}
						else if (currentKeyStates[SDL_SCANCODE_KP_3]) {
							_pieces[player[0]].type = tbot;
							player[0] = 3;
							_pieces[player[0]].type = tplayer;
							//std::cout << "change player[0] \n";
						}
					}
					else if (currentKeyStates[SDL_SCANCODE_KP_1]) {
						_pieces[player[0]].type = tbot;
						player[0] = 1;
						_pieces[player[0]].type = tplayer;
						//std::cout << "change player[0][2] \n";
					}
					else if (currentKeyStates[SDL_SCANCODE_KP_2]) {
						_pieces[player[0]].type = tbot;
						player[0] = 5;
						_pieces[player[0]].type = tplayer;
						//std::cout << "change player[0][6] \n";
					}
					else if (currentKeyStates[SDL_SCANCODE_KP_3]) {
						_pieces[player[0]].type = tbot;
						player[0] = 3;
						_pieces[player[0]].type = tplayer;
						//std::cout << "change player[0] \n";
					}
				}
			}

			if (_pvp)
			{
				behav_bot();
				confines(player[0]);
				confines(player[1]);
				_lib->draw(_pieces);
				behav_ball();
			}
			else if (_pvc)
			{
				behav_bot();
				confines(player[0]);
				confines(player[1]);

				_lib->draw(_pieces);
				behav_ball();
			}
			
		}
	}
}