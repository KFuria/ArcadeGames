#include "snake.h"

Game_t * game_init(uint16_t grid_size, uint16_t start_size){
    Game_t * game = malloc(sizeof(Game_t));
    game->grid_size = grid_size;
    game->start_size = start_size;
    game->running = true;
    game->pause = false;
    game->reset = false;
    game->crash = false;

    snake_init(game); 
    food_init(game);   
    game->lastscore = 0;
    game->score = 0;

    return game;
}

void game_reset(Game_t * game){
    game->score = 0;
    game->crash = false;
    game->pause = false;
    game->reset = false;
    snake_destroy(game);
    snake_init(game);
    food_place(game);
    return;
}


void snake_init(Game_t * game){
    //new snake
    Snake_t *newSnake = malloc(sizeof(Snake_t));
    newSnake->head = NULL;
    newSnake->tail = NULL;
    newSnake->length = 0;
    game->snake = newSnake;

    //head segment
    SnakeSeg_t *newSnakeHead = malloc(sizeof(SnakeSeg_t));
    newSnakeHead->x = game->grid_size / 2;
    newSnakeHead->y = game->grid_size / 2;
    newSnakeHead->dir = SNAKE_UP;
    newSnakeHead->next = NULL;
    game->snake->head = newSnakeHead;
    game->snake->tail = newSnakeHead;

    //add additional starting segments
    for(int i=0; i < game->start_size; i++){
        snake_increment(game->snake);
    }
    return;
}

void snake_increment(Snake_t * snake){
    // new segment
    SnakeSeg_t *newSnakeSeg = malloc(sizeof(SnakeSeg_t));
    newSnakeSeg->x = snake->tail->x;
    newSnakeSeg->y = snake->tail->y;
    newSnakeSeg->dir = snake->tail->dir;
    newSnakeSeg->next = NULL;

    snake->tail->next = newSnakeSeg;
    snake->tail = newSnakeSeg;
    snake->length += 1;
    return;
}

void snake_move(Game_t * game){
    Snake_t * snake = game->snake;
    food_t * food = game->food;

    // Save head x,y 
    int prevX = snake->head->x;
    int prevY = snake->head->y;
    int prevSegX, prevSegY;

    // Move head based on dir
    switch(snake->head->dir){
        case SNAKE_UP:
            snake->head->y--;
            snake->head->last_dir = SNAKE_UP;
            break;
        case SNAKE_DOWN:
            snake->head->y++;
            snake->head->last_dir = SNAKE_DOWN;
            break;
        case SNAKE_LEFT:
            snake->head->x--;
            snake->head->last_dir = SNAKE_LEFT;
            break;
        case SNAKE_RIGHT:
            snake->head->x++;
            snake->head->last_dir = SNAKE_RIGHT;
            break; 
    }

    //update rest of snake segments to follow head
    SnakeSeg_t * curr_seg = snake->head->next; 
    while(curr_seg != NULL){
        prevSegX = curr_seg->x;
        prevSegY = curr_seg->y;
        
        curr_seg->x = prevX;
        curr_seg->y = prevY;

        prevX = prevSegX;
        prevY = prevSegY;

        curr_seg = curr_seg->next;
    }

    // Check for crash
    if(snake->head->x < 0 || snake->head->x >= game->grid_size ||
        snake->head->y < 0 || snake->head->y >= game->grid_size){
            game->pause = true;
            game->crash = true;
            game->lastscore = game->score;
        }
    curr_seg = snake->head->next;
    while(curr_seg != NULL){
        if(curr_seg->x == snake->head->x && curr_seg->y == snake->head->y){
            game->pause = true;
            game->crash = true;
            game->lastscore = game->score;
        }
        curr_seg = curr_seg->next;
    }
    
    // check if snake eats food
    if(snake->head->x == food->x && snake->head->y == food->y){
        snake_increment(snake);
        food_place(game);
        game->score += 1;
    }

    return;
}

void snake_destroy(Game_t * game){
    // free segments
    SnakeSeg_t * currSeg = game->snake->head;
    SnakeSeg_t * temp;
    while(currSeg != NULL){
        temp = currSeg;
        currSeg = currSeg->next;
        free(temp);
    }
    // free snake
    game->snake->head = NULL;
    game->snake->tail = NULL;
    free(game->snake);
    
    return;
}

void food_init(Game_t * game){
    game->food = malloc(sizeof(food_t));
    food_place(game);
    return;
}

void food_place(Game_t * game){
    srand(time(0));
    food_t * food = game->food;
    bool in_snake;
    do{
        in_snake = false;
        game->food->x = rand() % game->grid_size;
        game->food->y = rand() % game->grid_size;
        SnakeSeg_t * currSeg = game->snake->head;
        while(currSeg != NULL){
            if(currSeg->x == food->x && currSeg->y == food->y)
                in_snake = true;
            currSeg = currSeg->next;
        }
    }while(in_snake);
    
    return;
}

void game_destroy(Game_t * game){
    snake_destroy(game);
    food_destroy(game);
    free(game);
    return;
}

void food_destroy(Game_t * game){
    free(game->food);
    return;
}