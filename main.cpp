/***********************

Master thesis

Author: Naresh Balaji Ravichandran
Supervisor: Anders Lansner

************************/

#include "main.h"
#include "grid.cpp"
#include "qbrain.cpp"
#define _VERBOSE false

int main(int argc, char *argv[])
{
  if(_VERBOSE) std::cout<<"Hello World!";

  grid grid1;
  qbrain qbrain1;

  //qbrain1.VERBOSE = _VERBOSE;
  
  int state,action;
  vector<float> reward(2);

  float any_reward = 0.0;

  srand (time(NULL));
  
  for (int episode=0; episode<1; episode++)
  {
    grid1.reset_grid();
    qbrain1.reset();
    grid1.parse_param("grid_paramfile.par");
    qbrain1.qvalue_log(); //need this??
    qbrain1.motivation_log();
    qbrain1.state_internal_log();
    
    for(int t=0; t<120000; t++)
    {
      state = grid1.get_scalar_state_over_gaps();
      reward = grid1.get_reward();
      
      if(t)
	qbrain1.advance_timestep(state, reward, episode, t);
    
      qbrain1.set_state(state);
      
      action = qbrain1.get_action_epsilon_greedy();
      grid1.choose_action(action);

      grid1.write_state(true);
      grid1.print_state(_VERBOSE);
      grid1.advance_timestep();

      any_reward = 0.0;
      for (int reward_idx=0; reward_idx<2; reward_idx++)
	any_reward += reward[reward_idx];      
    }
  }
  if(_VERBOSE) std::cout<<"\n";
  return 0;
}
