#pragma once

#include <iostream>
#include <SDL.h>
#include <SDL_image.h>
#include <SDL_ttf.h>
#include <SDL_mixer.h>
#include <vector>
#include "piece.h"

#define WIDTH 480
#define HEIGHT 840
#define WID_BORDER 20
#define HEI_BORDER 50
#define SIZE_PIECE 542
#define SIZE_BAT 25
#define SIZE_BALL 25
#define BLACK_COLOR 0,0,0
#define RED_COLOR 255,0,0
#define BLUE_COLOR 0,0,255
#define WHITE_COLOR 255,255,255
#define MAX_SPEED SIZE_BALL/2
#define BOOT_SP 6

class GUI_SDL
{
public:
	GUI_SDL();
	~GUI_SDL();

	void new_game(bool pvp, bool hard, bool isSelectingGameMode, bool isSelectingDifficulty);
	Event_en checkEvent(bool isSelectingGameMode, bool isSelectingDifficulty);
	void draw( std::vector<piece> & pieces);
	bool change_noise();
	void countdown(int count);
	void draw_field(bool isHard);
	void win(int x);
	void play_sound(Collision s);
	int getDirectionalAccumulation(int xVector1, int yVector1, int xVector2, int yVector2);
	bool isAPBetweenABAndAC(bool isFirstTriangle, int xP, int yP);
	bool isAPBetweenCAAndCB(bool isFirstTriangle, int xP, int yP);
	bool checkInArrow(int x, int y);
	void clearRend();

private:
	
	void load_ttf();
	void load_img();
	void load_sound();
	void draw_dynamic();
	void draw_game_mode_selection(bool pvp);
	void draw_difficulty_selection(bool hard);
	
	bool _noise = true;
	const int X_A1 = 40, Y_A1 = 270, X_B1 = 72, Y_B1 = 270, X_C1 = 56, Y_C1 = 300;
	const int X_A2 = 410, Y_A2 = 270, X_B2 = 442, Y_B2 = 270, X_C2 = 426, Y_C2 = 300;
	SDL_Window *_win;
	SDL_Renderer *_rend;
	SDL_Surface *_ttf;
	SDL_Texture *_background, *_bat1, *_bat2, *_ball, *_text, *_dynamic, * _count;
	TTF_Font *_font;
	SDL_Color _color;
	SDL_Rect _src, _dst;
	Mix_Music *_music;
	Mix_Chunk *_board, *_hit, *_goal;
};
