#include "snake.h"

#define WINDOW_X 20
#define WINDOW_Y 20
#define WINDOW_WIDTH 1770
#define WINDOW_HEIGHT 1405

void handle_input(SDL_Event event, Game_t * game){
    Snake_t * snake = game->snake;
    // Handle inputs and update head dir
    while(SDL_PollEvent(&event)){
        switch(event.type){
            case SDL_QUIT:
                game->running = false;
                break;
            case SDL_KEYUP:
                break;
            case SDL_KEYDOWN:
                switch(event.key.keysym.sym){
                    case SDLK_ESCAPE:
                        game->running = false;
                        break;
                    case SDLK_UP:
                        if(snake->head->last_dir != SNAKE_DOWN && !game->pause)
                            snake->head->dir = SNAKE_UP;
                        break;
                    case SDLK_DOWN:
                        if(snake->head->last_dir != SNAKE_UP && !game->pause)
                            snake->head->dir = SNAKE_DOWN;
                        break;
                    case SDLK_LEFT:
                        if(snake->head->last_dir != SNAKE_RIGHT && !game->pause)
                            snake->head->dir = SNAKE_LEFT;
                        break;
                    case SDLK_RIGHT:
                        if(snake->head->last_dir != SNAKE_LEFT && !game->pause)
                            snake->head->dir = SNAKE_RIGHT;
                        break;
                    case SDLK_p:
                        game->pause = true;
                        break;
                    case SDLK_c:
                        if(game->crash == false)
                            game->pause = false;
                        break;
                    case SDLK_r:
                        game->reset = true;
                        break;
                }
                break;
        }
    }
}

void render_game(SDL_Renderer * renderer, Game_t * game, int x, int y){
    Snake_t * snake = game->snake;
    food_t * food = game->food;
    int block_size = GRID_DIM / game->grid_size;

    // Grid
    SDL_SetRenderDrawColor(renderer, 0x40, 0x40, 0x40, 255);
    SDL_Rect cell;
    cell.w = block_size;
    cell.h = block_size;
    for(int i = 0; i < game->grid_size; i++){
        for(int j = 0; j < game->grid_size; j++){
            cell.x = x + (i * block_size);
            cell.y = y + (j * block_size);
            SDL_RenderDrawRect(renderer, &cell);
        }
    }

    //snake
    SDL_SetRenderDrawColor(renderer, 0x00, 0xff, 0x00, 255);
    SDL_Rect seg;
    seg.w = block_size;
    seg.h = block_size;
    SnakeSeg_t * curr_seg = snake->head;
    while(curr_seg != NULL){
        seg.x = x + curr_seg->x * block_size;
        seg.y = y + curr_seg->y * block_size;
        SDL_RenderFillRect(renderer, &seg);
        curr_seg = curr_seg->next;
    }
    
    //food
    SDL_SetRenderDrawColor(renderer, 0xff, 0x00, 0x00, 255);
    SDL_Rect foodSeg;
    foodSeg.w = block_size;
    foodSeg.h = block_size;
    foodSeg.x = x + food->x * block_size;
    foodSeg.y = y + food->y * block_size;
    SDL_RenderFillRect(renderer, &foodSeg);
    return;
}


int main(){
    SDL_Window * window;
    SDL_Renderer * renderer;
    if(SDL_Init(SDL_INIT_VIDEO) < 0){
        fprintf(stderr, "ERROR: SDL_INIT_VIDEO");
    }
    window = SDL_CreateWindow("Snake",WINDOW_X,WINDOW_Y,WINDOW_WIDTH,WINDOW_HEIGHT,SDL_WINDOW_BORDERLESS);
    if(NULL == window){
        fprintf(stderr, "ERROR: Window");
        exit(EXIT_FAILURE);
    }
    renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);
    if(NULL == renderer){
        fprintf(stderr, "ERROR: Renderer");
        exit(EXIT_FAILURE);
    }

    //Game init
    Game_t * game = game_init(50, 3);
    int grid_x = (WINDOW_WIDTH / 2) - (GRID_DIM / 2);
    int grid_y = (WINDOW_HEIGHT / 2) - (GRID_DIM / 2);
        
    // Game Loop Begins
    SDL_Event event;
    while(game->running){
        // handle user inputs
        handle_input(event, game);

        // Move snake based on inputs
        if(!game->pause)
            snake_move(game);
        
        if(game->reset)
            game_reset(game);
        
        // Render game if snake has not crashed 
        if(!game->crash){
            SDL_RenderClear(renderer);
            render_game(renderer, game, grid_x, grid_y);
            SDL_SetRenderDrawColor(renderer, 0x11, 0x11, 0x11, 255);
            SDL_RenderPresent(renderer);
        }
        
        SDL_Delay(1000/15);
    }

    // Game Loop Ends
    game_destroy(game);
    // Release resources
    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();
    return 0;
}