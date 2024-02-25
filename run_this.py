from maze_env import Maze
from RL_brain import DeepQNetwork
from queue import Queue


def run_maze(env):
    file = open("record.txt", 'w')
    step = 0
    listbs = []
    for episode in range(300):
        # initial observation
        observation = env.reset()
        listbs.append(env.best_path[0][1])
        while True:
            # fresh env
            env.render()
            # print("step is:",step)
            # RL choose action based on observation
            action = RL.choose_action(observation)

            # RL take action and get next observation and reward
            listbs.append(action)
            observation_, reward, done,C = env.step(action)
            file.write(str(action))
            file.write("->")
            RL.store_transition(observation, action, reward, observation_)

            if (step % 5 == 0):
                file.write("\n")
                file.write("studying")
                RL.learn()

            # swap observation
            observation = observation_

            # break while loop when end of this episode
            if done:
                print("arriving")
                listbs.append(action)
                break
            step += 1

    # end of game
    listbs.append(env.best_path[-1][1])
    print('game over')
    env.destroy()
    file.close()
    return listbs


def listDeal(list):
    res=[]
    q = Queue()

    for i in range(len(list)):
        q.put(list[i])
        q = delQueue(q, list[i])
    while not q.empty():
        res.append(q.get())
    return res

def delQueue(q, i):
    q2 = Queue()
    while (not q.empty()):
        a = q.get()
        if not a == i:
            q2.put(a)
        if a == i:
            q2.put(i)
            break

    return q2


if __name__ == "__main__":
    import os
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    print(os.getcwd())
    # maze game
    env = Maze()
    RL = DeepQNetwork(env.n_actions, env.n_features,
                      learning_rate=0.005,
                      reward_decay=0.7,
                      e_greedy=0.9,
                      replace_target_iter=200,
                      memory_size=2000,
                      # output_graph=True
                      )
    listbs = run_maze(env)
    q = listDeal(listbs)
    C=env.get_cost()
    cost=0
    for i in range(len(q)):
        if(i==(len(q))-1):
            break
        cost=cost+C[q [i]][q[i+1]]
    print(q)
    print("networkCost is:")
    print(cost)
    with open("RL.txt",'w') as f:
        f.write(str(q))
    env.mainloop()
    RL.plot_cost()
