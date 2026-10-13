from environment import Maze
from agent import QLearningAgent


EPISODES = 5000
MAX_STEPS = 200


def train():
    maze = Maze()
    agent = QLearningAgent()

    recent_rewards = []
    recent_successes = []

    print("PROJECT NEURO")
    print("=" * 50)
    print("Training AI...")

    for episode in range(1, EPISODES + 1):
        state = maze.reset()

        total_reward = 0
        success = False

        for _ in range(MAX_STEPS):
            action = agent.choose_action(state)

            next_state, reward, done = maze.step(action)

            agent.learn(
                state,
                action,
                reward,
                next_state,
                done
            )

            state = next_state
            total_reward += reward

            if done:
                success = reward > 0
                break

        agent.reduce_exploration()

        recent_rewards.append(total_reward)
        recent_successes.append(int(success))

        if episode % 500 == 0:
            avg_reward = sum(recent_rewards[-500:]) / 500
            success_rate = (
                sum(recent_successes[-500:]) / 500
            ) * 100

            print(
                f"Episode {episode:4} | "
                f"Avg reward: {avg_reward:7.2f} | "
                f"Success rate: {success_rate:5.1f}% | "
                f"Exploration: {agent.epsilon:.3f}"
            )

    print("\nTraining complete!")
    return maze, agent


def demonstrate(maze, agent):
    print("\nAI DEMONSTRATION")
    print("=" * 50)

    state = maze.reset()
    total_reward = 0

    # Disable random exploration for the demonstration.
    original_epsilon = agent.epsilon
    agent.epsilon = 0

    maze.display()

    for step in range(1, MAX_STEPS + 1):
        action = agent.choose_action(state)

        next_state, reward, done = maze.step(action)

        state = next_state
        total_reward += reward

        print(f"Step {step}: action={action}, reward={reward}")
        maze.display()

        if done:
            if reward > 0:
                print("AI reached the goal!")
            else:
                print("AI fell into a trap.")

            break

    print(f"Total reward: {total_reward}")

    agent.epsilon = original_epsilon


if __name__ == "__main__":
    maze, agent = train()
    demonstrate(maze, agent)