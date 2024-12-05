import gym_cutting_stock
import time
#import timeit
import gymnasium as gym
from policy import GreedyPolicy, RandomPolicy
from student_submissions.s2210xxx.policy2210xxx import Policy2210xxx

# tạo biến thời gian
start_time = time.time()
print(f"Thời gian bắt đầu: {time.ctime(start_time)}")

# Create the environment
env = gym.make(
    "gym_cutting_stock/CuttingStock-v0",
    render_mode="human",  # Comment this line to disable rendering
)
NUM_EPISODES = 100

if __name__ == "__main__":
    # Reset the environment
    observation, info = env.reset(seed=42)

    # Test GreedyPolicy
    # gd_policy = GreedyPolicy()
    # ep = 0
    # while ep < NUM_EPISODES:
    #     action = gd_policy.get_action(observation, info)
    #     observation, reward, terminated, truncated, info = env.step(action)

    #     if terminated or truncated:
    #         print(info)
    #         observation, info = env.reset(seed=ep)
    #         ep += 1
            

    # Reset the environment
    # observation, info = env.reset(seed=42)

    # Test RandomPolicy
    # rd_policy = RandomPolicy()
    # ep = 0
    # while ep < NUM_EPISODES:
    #     action = rd_policy.get_action(observation, info)
    #     observation, reward, terminated, truncated, info = env.step(action)

    #     if terminated or truncated:
    #         observation, info = env.reset(seed=ep)
    #         print(info)
    #         ep += 1

    # Uncomment the following code to test your policy
    # Reset the environment
    observation, info = env.reset(seed=42)

    policy2210xxx = Policy2210xxx()
    # code lấy từ phía trên 
    ep = 0
    while ep < NUM_EPISODES:
        action = policy2210xxx.get_action(observation, info)
        observation, reward, terminated, truncated, info = env.step(action)

        if terminated or truncated:
            print(info)
            observation, info = env.reset(seed=ep)
            #print(info)
            ep += 1

    # code ban đầu của thầy 
    # for _ in range(200):
    #     action = policy2210xxx.get_action(observation, info)
    #     observation, reward, terminated, truncated, info = env.step(action)

    #     if terminated or truncated:
    #         print(info)
    #         observation, info = env.reset()

    # In thời gian kết thúc
    end_time = time.time()
    print(f"Thời gian kết thúc: {time.ctime(end_time)}")

    # Tính toán thời gian trôi qua (elapse time)
    elapse_time = end_time - start_time
    print(f"Elapse time: {elapse_time:.6f} giây")

env.close()

