#include "main.h"

// COLOR CODING:
// R1,R2,... = 0,1,2,... 
// WALL = -1
// GROUND = -2
// AGENT = -3

class grid
{
 private:
  
  int **grid1, M, N;

  int **grid1_place_cell_index, *place_cell_x, *place_cell_y;
  int bot_x, bot_y, bot_reset_x, bot_reset_y;
  int place_field_radius, num_place_cells;
  
  int action;
  
  vector<float> reward;  
  int num_rewards, num_pellets;
  
  int current_time;


 public:
  
  //init grid with size MxN;
  grid(int M=M_default, int N=N_default, bool enable_write = true)
  {
    ofstream outfile_state, outfile_reward_timing;
    outfile_state.open("state_data.dat", ios::trunc);
    outfile_reward_timing.open("reward_timing_data.dat", ios::trunc);
    
    num_rewards = 0;
    num_pellets = 0;
    
    action = -1;
    this->M = M;
    this->N = N;
    current_time = 0;
    
    grid1 = (int**)malloc(M*sizeof(int*));
    grid1_place_cell_index = (int**)malloc(M*sizeof(int*));
    
  }

  void parse_param(string str_param)
  { 
    ifstream infile;
    infile.open(str_param);
        
    infile >> M >> N >> num_place_cells >> place_field_radius;

    for(int i=0; i<M; i++)
    {
      grid1[i] = (int*)malloc(N*sizeof(int));
      grid1_place_cell_index[i] = (int*)malloc(N*sizeof(int));
    }

    for(int i=0; i<M; i++)
      for(int j=0; j<N; j++)
      {
	grid1[i][j] = -2;
	grid1_place_cell_index[i][j] = -1;
      }    
        
    // multi-agent
    int num_bots;  
    infile >> num_bots;    
    if(num_bots != 1) std::cerr<<"\nGet me just one bot for now..";
    
    for(int i=0; i<num_bots; i++)
      infile >> bot_reset_x >> bot_reset_y;
    bot_x = bot_reset_x;
    bot_y = bot_reset_y;
    
    // multi-goal rewards/punishments
    int x,y;
    infile >> num_rewards;
    reward.resize(num_rewards);
    
    for (int reward_idx=0; reward_idx<num_rewards; reward_idx++)
    {  
      infile >> num_pellets;
      for(int pellet_idx=0; pellet_idx<num_pellets; pellet_idx++)
      {
	infile >> x >> y;
	throw_food_at(x,y,reward_idx);
      }
    }
    
    // gridworld wall
    int x1,y1,x2,y2,num_walls;
    infile >> num_walls;
    for(int i=0; i<num_walls; i++)
    {
      infile >> x1 >> y1 >> x2 >> y2;
      build_wall_at( x1, y1, x2, y2);
    }

    //create_place_cells_over_grid(place_field_radius, num_place_cells);
    create_place_cells_over_gaps(place_field_radius,num_place_cells);
  }

  ~grid()
  {
    for(int i=0; i<M; i++)
    {
      free(grid1[i]);
    }
    free(grid1);
  }

  //
  vector<int> get_pos_from_place_cell_index(int x)
  {
    vector<int> bot(2,0.0);

    for(int j=0; j<N; j++)
    {
      for(int i=0; i<M; i++)
      {
	if(grid1_place_cell_index[i][j] == x)
	{	  
	  bot[0] = i;
	  bot[1] = j;
	  return bot;
	}
      }
    }
    return bot;
  }
  
  //reset grid
  void reset_grid()
  {
    bot_x = bot_reset_x;
    bot_y = bot_reset_y;
    std::fill(reward.begin(), reward.end(), 0.0);
    action = -1;    
  }

  //reset grid at random
  void reset_grid_random()
  {
    vector<int> bot;
    bot= get_pos_from_place_cell_index(rand()%num_place_cells);
    bot_x = bot[0];
    bot_y = bot[1];
    std::fill(reward.begin(), reward.end(), 0.0);
    action = -1;    
  }

  //reset grid
  void reset_grid_at(int x, int y)
  {    
    bot_x = x;
    bot_y = y;
    std::fill(reward.begin(), reward.end(), 0.0);
    action = -1;    
  }
  
  //init bot at position (x,y);
  void throw_bot_at(int x, int y)
  {
    if(x>=M || y>=N)
    {
      return;
    }
    bot_x = x;
    bot_y = y;
  }

  //init food at position(*x,*y) [1]
  void throw_food_at(int x, int y, int reward_idx)
  {
    //std::cout<<"\n FOOD"<<x<<","<<y;
    grid1[x][y] = reward_idx;
  }

  void build_wall_at(int x1, int y1, int x2, int y2)
  {
    std::cout<<"\nBuilding a wall between [";
      std::cout<<x1<<" "<<x2<<"] == ["<<y1<<" "<<y2<<"]" ;
    for(int x=x1; x<=x2; x++)
      for(int y=y1; y<=y2; y++)
      {
	grid1[x][y] = -1;
      }
  }
  
  //
  float is_food_at(int x, int y)
  {
    if(grid1[x][y] < 0)
    {
      return -1;
    }
    else
    {
      return grid1[x][y];
    }
  }
  
  //move bot
  void move_bot_by(int x, int y)
  {
    //uncyclic
    if(bot_x+x<0 || bot_x+x>=M || bot_y+y<0 || bot_y+y>=N)
      return;
    
    int bot_x_temp, bot_y_temp;
    
    bot_x_temp = bot_x + x;
    bot_y_temp = bot_y + y;

    //cyclic
    /*if(bot_x_temp < 0)
      bot_x_temp = M + bot_x_temp;
    if(bot_y_temp < 0)
      bot_y_temp = M + bot_y_temp;
    if(bot_x_temp >= M)
      bot_x_temp %= M;
    if(bot_y_temp >= N)
    bot_y_temp %= N;*/
    
    if(grid1[bot_x_temp][bot_y_temp] != -1)  //if not a wall
    {
      bot_x = bot_x_temp;
      bot_y = bot_y_temp;
    }    
  }
  
  //get position()  
  void print_state(bool print_shell=false)
  {
    if(!print_shell)
      return;
    std::cout<<"\nTIME("<<current_time<<")";
    std::cout<<" POS("<<bot_x<<","<<bot_y<<")";
    std::cout<<" PC("<<place_cell_over_gaps_of(bot_x, bot_y)<<")";

    /*std::cout<<" PC_A[";
    for(int i=0; i<get_state().size(); i++)
    {
      std::cout<<get_state()[i]<<" ";
    }
    std::cout<<"]";
    */

    std::cout<<" R(";
    for (int reward_idx=0; reward_idx<num_rewards; reward_idx++)
      std::cout<<reward[reward_idx]<<",";
    std::cout<<")";
    std::cout<<" AC("<<action<<")";
    fflush(stdout);
  }

  void open_file()
  {
  }
    
  void write_state(bool write_permission)
  {
    if(write_permission)
    {
      ofstream outfile_state, outfile_reward_timing;
      outfile_state.open("state_data.dat", ios::app);	 
      outfile_state<<current_time<<" "<<bot_x<<" "<<bot_y<<" "<< action<<" "<<reward[0]<<endl;

      outfile_reward_timing.open("reward_timing_data.dat", ios::app);
      if(reward[0] == 1)
	outfile_reward_timing<<current_time<<"\n";
    }
  } 
  
  //Assumption: no heirarchy, 1-level field, equal radii, equidistant, regular, square arena, create place cells
  void create_place_cells_over_grid(int place_field_radius, int num_place_cells)
  {
    this->place_field_radius = place_field_radius;
    this->num_place_cells = num_place_cells;
    
    place_cell_x = (int*)malloc(num_place_cells*sizeof(int));
    place_cell_y = (int*)malloc(num_place_cells*sizeof(int));
    int place_cell_index = 0;
    
    for(int j=0; j<N; j++)
    {
      for(int i=0; i<M; i++)
      {
	if(i%(2*place_field_radius+1)==place_field_radius && j%(2*place_field_radius+1)==place_field_radius)  
	{
	  place_cell_x[place_cell_index] = i;
	  place_cell_y[place_cell_index] = j;
	  place_cell_index++;
	}
      }
    }
  }

  void create_place_cells_over_gaps(int place_field_radius, int num_place_cells)
  {
    if (place_field_radius != 0)
      std::cerr<<"\nNot ready for big place cells yet!";

    int place_cell_index = 0;
    
    for(int j=0; j<N; j++)
    {
      for(int i=0; i<M; i++)
      {
	if(grid1[i][j] != -1)
	{
	  grid1_place_cell_index[i][j] = place_cell_index++;
	}
      }
    }
    if(place_cell_index != num_place_cells)
      std::cerr<<"\nMore place cells allocated than needed! "<<place_cell_index<<"!="<<num_place_cells;
  }
  
  //identify place cell index from (x,y) position
  int place_cell_over_grid_of(int x, int y)    
  {
    int min_manhattan_distance = M+N, manhattan_distance;
    int place_cell_index = -1;
    for(int i=0; i<num_place_cells; i++)
    {
      manhattan_distance = abs(place_cell_x[i]-x) + abs(place_cell_y[i]-y);
      //std::cout<<"\n"<<i<<" "<<manhattan_distance;
      if(manhattan_distance < min_manhattan_distance)
      {
	min_manhattan_distance = manhattan_distance;
	place_cell_index = i;
      }
    }
    return place_cell_index;
  }

  int place_cell_over_gaps_of(int x, int y)
  {
    if(x<0 || x>=M || y<0 || y>=N)
    {
      std::cerr<<"\nOut of grid!";
      return 0;
    }
    else
    {
      return grid1_place_cell_index[x][y];
    }
  }
  
  vector<float> get_state_over_grid()
  {
    int x = bot_x, y = bot_y;
    int min_manhattan_distance = M+N, manhattan_distance;
    int place_cell_index = -1;
    for(int i=0; i<num_place_cells; i++)
    {
      manhattan_distance = abs(place_cell_x[i]-x) + abs(place_cell_y[i]-y);
      if(manhattan_distance < min_manhattan_distance)
      {
	min_manhattan_distance = manhattan_distance;
	place_cell_index = i;
      }
    }
    vector<float> state(num_place_cells,0.0);
    state[place_cell_index] = 1.0;
    return state;
  }

  // WRONG!!
  /*int get_scalar_state_over_gaps()
  {
    return grid1_place_cell_index[bot_x][bot_y];
  }*/
  int get_scalar_state_over_gaps()
  {
    return bot_y*M + bot_x;
  }
  
  vector<float> get_state_over_gaps()
  {
    vector<float> state(num_place_cells,0.0);
    state[grid1_place_cell_index[bot_x][bot_y]] = 1.0;
    return state;
  }

  vector<float> get_reward()
  {
    return reward;
  }

  void choose_action(int action)    
  {
    this->action = action;
  }

  void do_action_8()
  {
    switch (this->action)
    {
    case 0: //move up
      move_bot_by(0,-1);
      break;
    case 1: //move up-left
      move_bot_by(-1,-1);
      break;
    case 2: //move left
      move_bot_by(-1,0);
      break;
    case 3: //move down-left
      move_bot_by(-1,1);
      break;
    case 4: //move down
      move_bot_by(0,1);
      break;
    case 5: //move down-right
      move_bot_by(1,1);
      break;
    case 6: //move right
      move_bot_by(1,0);
      break;
    case 7: //move up-right
      move_bot_by(1,-1);
      break;
    }
  }

  void do_action_5()
  {
    switch (this->action)
    {
    case 0: //move up
      move_bot_by(0,-1);
      break;
    case 1: //move left
      move_bot_by(-1,0);
      break;
    case 2: //move down
      move_bot_by(0,1);
      break;
    case 3: //move right
      move_bot_by(1,0);
      break;
    case 4: //stay
      move_bot_by(0,0);
      break;
    }
  }

  void advance_timestep()
  {

    current_time++;
    
    if(action == -1)
    {
      std::cerr<<"Bad Initialization!";
      exit(1);
    }

    std::fill(reward.begin(), reward.end(), 0.0);
    
    //if(is_food_at(bot_x, bot_y) >= 0)
    //{
    //  do_action_5();
    //  return;
    //}
    
    do_action_5(); // do_action_8();
    
    std::fill(reward.begin(), reward.end(), 0.0);    
    if(is_food_at(bot_x, bot_y) >= 0){
      reward[is_food_at(bot_x, bot_y)] = 1.0;
    }
  }
};
