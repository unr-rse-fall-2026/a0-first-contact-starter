# A0: Environment Setup and ROS 2 First Contact

**Theme:** Run. Inspect. Change. Document.  
**Expected time:** 2–3 hours  
**Platform:** Ubuntu 24.04 and ROS 2 Jazzy  
**Work:** Individual

In this assignment, you will make sure your ROS 2 development environment works, use ROS 2's inspection tools to understand a running system, and adapt official Python publisher/subscriber examples into standalone executable files.

The point is not merely to make two terminals print text. By the end, you should be able to answer four questions about an unfamiliar ROS 2 system:

1. What nodes are running?
2. What data are flowing between them?
3. What type and rate does that data have?
4. How do the Python files connect to the nodes, topics, and messages visible in the running system?

## Learning objectives

After completing A0, you should be able to:

- distinguish a node, topic, and message;
- source the ROS 2 underlay;
- use official ROS 2 source code to locate an example and answer questions;
- inspect nodes, topics, message types, and publication rates from the command line;
- make and verify a small change to an existing ROS 2 example; and
- leave a reproducible record of what you ran and what you observed.

## Repository layout

Your completed repository should contain these four programs at its root:

```text
.
├── status_publisher.py
├── status_monitor.py
├── count_publisher.py
├── count_monitor.py
├── evidence/
│   ├── documentation.md
│   ├── inspection.md
│   └── reflection.md
└── tests/
    └── check_assignment.py
```

## Before you begin

Use a unique ROS domain ID whenever you are on a shared network. Your instructor will provide the value or range to use.

```bash
export ROS_DOMAIN_ID=<your assigned number>
source /opt/ros/jazzy/setup.bash
printenv ROS_DISTRO
```

You should see `jazzy`. If you do not, stop here and use the help guide below.

> Each new terminal starts with a clean shell. You must source ROS 2 in every terminal unless you have deliberately added the command to your shell configuration.

## Part 1 — Run a system you did not write

Open two sourced terminals. Run the standard ROS 2 Python demo publisher in one and subscriber in the other:

```bash
ros2 run demo_nodes_py talker
```

```bash
ros2 run demo_nodes_py listener
```

Do not move on as soon as text appears. First, describe in `evidence/inspection.md` what each process appears to do and what evidence supports your answer.

## Part 2 — Inspect the running ROS graph

Keep the talker and listener running. In a third sourced terminal, investigate the system in the order below.

```bash
ros2 node list
ros2 node info /talker
ros2 topic list -t
ros2 topic info /chatter
ros2 interface show std_msgs/msg/String
ros2 topic echo /chatter --once
ros2 topic hz /chatter
```

The commands form a reasoning chain:

- `node list` finds the components that exist.
- `node info` finds the interfaces used by one component.
- `topic list -t` identifies streams and their types.
- `topic info` identifies publishers and subscribers on one stream.
- `interface show` explains the structure of each message.
- `topic echo` shows a real message.
- `topic hz` measures how frequently messages arrive.

Complete the Part 2 prompts in `evidence/inspection.md`. Record short, relevant excerpts—not entire terminal sessions.

## Part 3 — Make the example yours

Use these two Python source files from the official ROS 2 Jazzy examples repository as your starting point. Copy them into the root of this repository.

- [Publisher member-function example](https://github.com/ros2/examples/blob/jazzy/rclpy/topics/minimal_publisher/examples_rclpy_minimal_publisher/publisher_member_function.py)
- [Subscriber member-function example](https://github.com/ros2/examples/blob/jazzy/rclpy/topics/minimal_subscriber/examples_rclpy_minimal_subscriber/subscriber_member_function.py)

Adapt the examples to meet the following specification.

### `status_publisher`

- Node name: `status_publisher`
- Topic: `/lab0/status`
- Message type: `std_msgs/msg/String`
- Rate: 4 Hz (one message every 0.25 seconds)
- Message content: must include `System ready` and an increasing count
- Console log: should make the published message visible

### `status_monitor`

- Node name: `status_monitor`
- Topic: `/lab0/status`
- Message type: `std_msgs/msg/String`
- Console log: should identify the received message

Begin each file with:

```python
#!/usr/bin/env python3
```

Make both files executable and run them directly:

```bash
chmod +x status_publisher.py status_monitor.py
./status_publisher.py
./status_monitor.py
```

Run the programs in separate sourced terminals. Do not copy code from an AI system or an unofficial tutorial without checking it against the official ROS 2 Jazzy source. In `evidence/documentation.md`, identify where the examples import the message type, assign the node and topic names, create the publisher or subscription, schedule or receive callbacks, and initialize and spin the node.

## Part 4 — Verify your system

Run both status nodes, then verify the system from a third terminal. Your evidence should establish all of the following:

- both expected node names appear;
- `/lab0/status` exists and uses `std_msgs/msg/String`;
- the topic has one publisher and one subscriber;
- a real message contains the required status text and a count; and
- the observed rate is reasonably close to 4 Hz.

Choose commands that provide that evidence. The Part 2 chain is a useful model, but you should adapt names and arguments rather than blindly pasting it.

Record the commands, compact output excerpts, and your interpretation in `evidence/inspection.md`.

## Part 5 — Explain what you built

Complete `evidence/reflection.md`. Your explanation should connect:

- the Python class and `main()` function;
- the executable Python files and processes created when you run them;
- the node names, topic names, and message types defined in the source; and
- the nodes, topic, and messages visible in the running ROS graph.

Students enrolled in CPE 691 must also include the output of `ros2 topic info /lab0/status --verbose` and a 150–250 word explanation of what the publisher/subscriber endpoint and QoS information means for this system.

## Part 6 — Change the message contract

A ROS topic is defined by both its name and its message type. Publishers and subscribers can communicate only when they agree on that contract. In this extension, preserve the publisher/subscriber pattern while changing the kind of data being exchanged.

Create `count_publisher.py` and `count_monitor.py` in the repository root, based on your status nodes.

### `count_publisher`

- Node name: `count_publisher`
- Topic: `/lab0/count`
- Message type: `std_msgs/msg/Int32`
- Rate: 1 Hz (one message every 1.0 second)
- Message content: an increasing integer
- Console log: should make the published value visible

### `count_monitor`

- Node name: `count_monitor`
- Topic: `/lab0/count`
- Message type: `std_msgs/msg/Int32`
- Console log: should identify the received integer

Make both files executable, then run them directly:

```bash
chmod +x count_publisher.py count_monitor.py
./count_publisher.py
./count_monitor.py
```

Inspect `/lab0/count` using the Part 2 command chain. Record concise evidence that the topic uses `Int32`, has one publisher and one subscriber, carries increasing integer values, and runs at approximately 1 Hz. In `evidence/reflection.md`, explain which parts of the String system changed, which stayed the same, and why both endpoints must agree on the message type.

> Later, you will apply the same idea to `geometry_msgs/msg/Twist` on `/cmd_vel`, when the message can command a simulated robot and its additional fields have a meaningful purpose.

## Run the repository checks

The repository includes student-facing checks for common structural mistakes. Each check explains what it examines and suggests a next action when it fails. Run them from the repository root:

```bash
python3 tests/check_assignment.py
```

You may also run one check at a time:

```bash
python3 tests/check_assignment.py status-files
python3 tests/check_assignment.py status-publisher
python3 tests/check_assignment.py status-monitor
python3 tests/check_assignment.py count-pair
python3 tests/check_assignment.py evidence
```

These checks inspect files and source code; they cannot prove that your live ROS graph behaved correctly. That is why your inspection evidence and explanation are required.

## Submission checklist

- [ ] The repository is pushed to GitHub.
- [ ] I ran `gh student submit`, and the latest automated checks pass or I have explained a remaining failure.
- [ ] All four Python files run directly using `./filename.py`.
- [ ] All three files in `evidence/` are complete.
- [ ] Output excerpts are short and readable; no screenshots are required.
- [ ] The status pair runs at approximately 4 Hz and the count pair at approximately 1 Hz.

## When to ask for help

Ask for help immediately if any of these happen:

- `source /opt/ros/jazzy/setup.bash` reports that the file does not exist;
- `printenv ROS_DISTRO` does not report `jazzy`;
- the demo nodes cannot be found after sourcing ROS 2;
- you see nodes or topics belonging to another student after setting your assigned `ROS_DOMAIN_ID`; or
- Git authentication prevents you from cloning or pushing.

For a code problem, first spend about 15 focused minutes on this sequence:

1. Read the complete error, including the first error rather than only the last line.
2. Confirm your current directory and which setup files you sourced.
3. Compare the relevant file with the official Jazzy source from Part 3.
4. Run the narrowest useful check again.
5. Commit or save your current work.

Then ask for help. Include the command you ran, the complete error text, what you expected, what you already checked, and a link to your latest pushed commit.

## Assessment

| Area | Points | Evidence |
|---|---:|---|
| Environment and baseline system | 10 | Correct terminal setup and successful demo observations |
| ROS graph inspection | 20 | Part 2 command chain, concise evidence, and accurate interpretations |
| Standalone status publisher/subscriber | 25 | Executable files, required node/topic/type/content/rate, readable code |
| Independent verification | 20 | Graph evidence supporting the required status behavior |
| Message-type extension | 15 | Working Int32 pair and explanation of the changed contract |
| Documentation, reflection, Git, and submission | 10 | Official source trail, explanations, meaningful commits, readable repository |
| **Total** | **100** | |
