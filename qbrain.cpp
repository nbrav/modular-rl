#include <iostream>
#include <stdlib.h>
#include <vector>
#include <fstream>
#include <time.h>
#include <algorithm>
#include <math.h>
#define PI 3.14159265

using namespace std;

class qbrain
{
 private:
  int _M,_N; // Size of the grid-world
  int _time;
  
  int _state, _state_prime;
  std::vector< float > _reward;
  int _action;
  int _reward_current;

  std::vector< float > _rpe;    
  std::vector< float > _rpe_cum;
  
  int _state_size;
  int _reward_size;
  int _action_size;

  int _state_internal_size;
  std::vector< float > _state_internal;
  std::vector< float > _state_internal_opt;
  
  std::vector< std::vector< std::vector<float> > > _qvalue;
  
  std::vector< float > _motivation;
  
  float _alpha; // Learning rate
  std::vector< float > _zeta; // Discount factor for H
  std::vector< float > _gamma; // Discount factor for Q
  float _epsilon; // Greedy arbitration exploration
  std::vector< float > _rho; // Drive parameter

  FILE *qvalue_outfile;
  FILE *qmax_outfile;
  FILE *state_internal_outfile;
  FILE *motivation_outfile;

 public:

  bool VERBOSE;
  
  qbrain()
  {
    //std::cout<<"\nSetting up Q-Brain...";
 
    parse_param();    
    
    // Initialize Q_{i,t}(s,a) matrix
    _qvalue.resize(_reward_size);
    for (int reward_idx=0; reward_idx<_reward_size; reward_idx++)
    {
      _qvalue[reward_idx].resize(_state_size);
      for (int state_idx=0; state_idx<_state_size; state_idx++)
      {
	_qvalue[reward_idx][state_idx].resize(_action_size,1);
	for (int action_idx=0; action_idx<_action_size; action_idx++)
	{
	  _qvalue[reward_idx][state_idx][action_idx] = ((float)rand()/(1-_gamma[reward_idx])/(RAND_MAX));
	}
      }
    }

    qvalue_outfile = fopen("qvalue.log", "wb");
    fclose(qvalue_outfile);

    // Initiate delta_i
    _rpe.resize(_reward_size);
    std::fill(_rpe.begin(), _rpe.end(), 1.0);

    _rpe_cum.resize(_reward_size);
    std::fill(_rpe_cum.begin(), _rpe_cum.end(), 0.0);
    
    //Initialize motivation_i
    _motivation.resize(_reward_size);    
    std::fill(_motivation.begin(), _motivation.end(), 1.0/float(_reward_size));

    motivation_outfile = fopen("motivation.log", "wb");
    fclose(motivation_outfile);

    // Logger setup
    state_internal_outfile = fopen("internal_state.log", "wb");
    fclose(state_internal_outfile);

    // Intialize H_{i,t}
    _state_internal_size = _reward_size;

    _state_internal_opt.resize(_state_internal_size);    
    for (int reward_idx=0; reward_idx<_reward_size; reward_idx++)
      _state_internal_opt[reward_idx] = 5.0;
    //_state_internal_opt[_reward_size-2] = 10.0;
    //_state_internal_opt[_reward_size-1] = 15.0;

    _state_internal.resize(_state_internal_size);
    for (int reward_idx=0; reward_idx<_reward_size; reward_idx++)
      _state_internal[reward_idx] = ((float)rand())*_state_internal_opt[reward_idx]/((float)RAND_MAX);
    //std::fill(_state_internal.begin(), _state_internal.end(), 1.0/float(_reward_size));
  }

  void parse_param()
  {
    ifstream infile;
    infile.open("grid_paramfile.par");

    int temp;
    
    infile >> _M >> _N;
    infile >> _state_size;
    infile >> temp >> temp >> temp >> temp;
    
    _action_size = 5;  //TODO: must get it from paramfile
    infile >> _reward_size;
    
    _alpha = 0.1;

    _zeta.resize(_reward_size);
    _gamma.resize(_reward_size);
    _rho.resize(_reward_size);

    for (int reward_idx=0; reward_idx<_reward_size; reward_idx++)
    {
      _zeta[reward_idx] = 0.995;
      _gamma[reward_idx] = 0.9;
      _rho[reward_idx] = 1.0;
    }
    _epsilon = 0.8;    
  }

  void reset()
  {    
  }

  void update_H()
  {
    // update physiological state from reward
    for (int reward_idx=0; reward_idx<_reward_size; reward_idx++)
    {
      _state_internal[reward_idx] = _zeta[reward_idx]*_state_internal[reward_idx] + _reward[reward_idx];
    }

    //std::cout<<" H"<<_state_internal[0]<<" "<<_state_internal[1]<<" M["<<_motivation[0]<<" "<<_motivation[1]<<"]";    
  }

  void update_rho()
  {
    // update rho
    for (int reward_idx=0; reward_idx<_reward_size; reward_idx++)
    {
      _rho[reward_idx] = _qvalue[reward_idx][_state][_action]; //*(1-_gamma[reward_idx]);
    }    

    // update motivational drive for plottinh alone
    for (int reward_idx=0; reward_idx<_reward_size; reward_idx++)
    {      
      _motivation[reward_idx] = _rho[reward_idx];
    }

  }
  
  void qvalue_log()
  {
    qvalue_outfile = fopen("qvalue.log", "ab"); //ab
    for (int reward_idx=0; reward_idx<_reward_size; reward_idx++)
      for (int state_idx=0; state_idx<_state_size; state_idx++)
	fwrite(&_qvalue[reward_idx][state_idx][0], sizeof(float) , _action_size, qvalue_outfile);
    fclose(qvalue_outfile);
  }

  void state_internal_log()
  {
    state_internal_outfile = fopen("internal_state.log", "ab"); //ab
    fwrite(&_state_internal[0], sizeof(float) , _state_internal_size, state_internal_outfile);
    fclose(state_internal_outfile);
  }
  
  void motivation_log()
  {
    motivation_outfile = fopen("motivation.log", "ab"); //ab
    fwrite(&_motivation[0], sizeof(float) , _reward_size, motivation_outfile);
    fclose(motivation_outfile);    
  }
  
  void set_state(int state)
  {
    _state = state;
  }

  int get_action_minimize_worst_drive()
  {
    float dist_Ht, dist_Ht_max=0.0;
    float dist_Ht1, dist_Ht1_min=999;
    int _r,_action;
    
    for(int reward_idx=0; reward_idx<_reward_size; reward_idx++)
    {
      // | H_i* - H_{i,t} |^rho_i
      dist_Ht = pow(abs(_state_internal_opt[reward_idx] - _state_internal[reward_idx]), _rho[reward_idx]); 

      if(dist_Ht>dist_Ht_max)
      {
	dist_Ht_max=dist_Ht;
	_r=reward_idx;
	_reward_current=reward_idx;
	dist_Ht1_min = 999;
		
	for(int action_idx=0; action_idx<_action_size; action_idx++)      
	{
	  // |H_i*-gamma_i*H_{i,t}-(1-gamma)Q_{i,t}(S_t,A)|_L1
	  dist_Ht1 = abs(_state_internal_opt[reward_idx] - _zeta[reward_idx]*_state_internal[reward_idx] - (1-_gamma[reward_idx])*_qvalue[_r][_state][action_idx]);
	  
	  if(dist_Ht1<dist_Ht1_min)
	  {
	    dist_Ht1_min=dist_Ht1;
	    _action = action_idx;
	  }
	}
      }
    }
    return _action;
  }

  int get_action_minimize_drive()
  {
    std::vector <float> drive(_action_size);    
    int _r,_action;
    
    for(int _a=0; _a<_action_size; _a++)
    {
      drive[_a] = 0.0;
      for(int _r=0; _r<_reward_size; _r++)
      {
	// | H_i* - zeta*H_{i,t} - Q |
	drive[_a] += pow(abs(_state_internal_opt[_r] - _zeta[_r]*_state_internal[_r] - (1-_gamma[_r])*_qvalue[_r][_state][_a]), _rho[_r]);      
      }
    }
    _action = std::distance(drive.begin(), std::min_element(drive.begin(), drive.end()));
    return _action;
  }

  int get_action_minimize_greedy_drive()
  {
    float dist_Ht, dist_Ht_max=0.0;
    float dist_Ht1, dist_Ht1_min=999;
    int _r,_action;
    
    for(int reward_idx=0; reward_idx<_reward_size; reward_idx++)
    {
      // | H_i* - H_{i,t} |^rho_i
      dist_Ht = abs(_state_internal_opt[reward_idx] - _state_internal[reward_idx]); 

      if(dist_Ht>dist_Ht_max)
      {
	dist_Ht_max=dist_Ht;
	_r=reward_idx;
	_reward_current=reward_idx;
	dist_Ht1_min = 999;
		
	for(int action_idx=0; action_idx<_action_size; action_idx++)      
	{
	  // |H_i*-gamma_i*H_{i,t}-(1-gamma)Q_{i,t}(S_t,A)|_L1
	  dist_Ht1 = abs(_state_internal_opt[reward_idx] - _zeta[reward_idx]*_state_internal[reward_idx] - (1-_gamma[reward_idx])*_qvalue[_r][_state][action_idx]);
	  
	  if(dist_Ht1<dist_Ht1_min)
	  {
	    dist_Ht1_min=dist_Ht1;
	    _action = action_idx;
	  }
	}
      }
    }
    return _action;
  }

  int get_action_epsilon_greedy()
  {
    int greedy_action = get_action_minimize_greedy_drive();
    
    if (((float)rand()/RAND_MAX) < _epsilon) // Exploit
    {
      _action = greedy_action; 
    }
    else // Explore
    {
      _action = rand()%_action_size;
    }
    return _action;    
  }
  
  void advance_timestep(int state_prime, std::vector< float > reward, int episode, int time)    
  {
    _state_prime = state_prime;

    _reward = reward;
    
    _time = time;
    
    // If you want to see performance live
    //_epsilon = min(_time/100000.0,1.0);
    //if(time > 100000)
    //  _epsilon = 1.0;

    update_H();

    for (int reward_idx=0; reward_idx<_reward_size; reward_idx++)
    {
      //_rpe[reward_idx] = _reward[reward_idx] + _gamma[reward_idx]*(*std::max_element(_qvalue[reward_idx][_state_prime].begin(), _qvalue[reward_idx][_state_prime].end())) - _qvalue[reward_idx][_state][_action];
      _rpe[reward_idx] = _reward[reward_idx] + _gamma[reward_idx]*(*std::max_element(_qvalue[reward_idx][_state_prime].begin(), _qvalue[reward_idx][_state_prime].end())) - _qvalue[reward_idx][_state][_action];
      
      _qvalue[reward_idx][_state][_action] += _alpha*_rpe[reward_idx];
    }

    update_rho();

    qvalue_log();
    state_internal_log();
    motivation_log();
  }  
};
