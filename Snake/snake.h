#ifndef __SNAKE__H__
#define __SNAKE__H__

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <time.h>

#define SDL_MAIN_HANDLED
#include <SDL2/SDL.h>

#define GRID_DIM 1200

enum{
    SNAKE_UP,
    SNAKE_DOWN,
    SNAKE_LEFT,
    SNAKE_RIGHT,
};

typedef struct _snake_seg{
    int x; 
    int y;
    int dir;
    int last_dir;
    struct _snake_seg *next;
} SnakeSeg_t;

typedef struct _snake{
    SnakeSeg_t *head;
    SnakeSeg_t *tail;
    int length;
} Snake_t;

typedef struct _food{
    int x; 
    int y;
} food_t;

typedef struct _game{
    bool running;
    bool pause;
    bool reset;
    bool crash;

    uint16_t grid_size;
    uint16_t start_size;
    
    Snake_t * snake;
    food_t * food;
    uint16_t score;
    uint16_t lastscore;

} Game_t;

// Game constructor
Game_t * game_init(uint16_t grid_size, uint16_t start_size);

// Reset snake
void game_reset(Game_t * game);

// Game destructor
void game_destroy(Game_t * game);

// Snake constructor
void snake_init(Game_t * game);

// Increase snake size when snake eats food
void snake_increment(Snake_t *snake);

// Move snake based on key inputs
void snake_move(Game_t * game);

// Snake Destructor
void snake_destroy(Game_t * game);

// Food constructor
void food_init(Game_t * game);

// Place food in grid
void food_place(Game_t * game);

// Food destructor
void food_destroy(Game_t * game);


#endif