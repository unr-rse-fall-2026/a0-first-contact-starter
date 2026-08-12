# A0: Environment Setup and ROS 2 First Contact

In this assignment, you will make sure your ROS 2 development environment works, use ROS 2's inspection tools to understand a running system, and adapt the official Python publisher/subscriber example into a small package of your own.

The point is not merely to make two terminals print text. By the end, you should be able to answer four questions about an unfamiliar ROS 2 system:

1. What nodes are running?
2. What data is flowing between them?
3. What type and rate does that data have?
4. Where do the code, package metadata, and executable names connect?

**Expected time:** 2–3 hours  
**Platform:** Ubuntu 24.04 and ROS 2 Jazzy  
**Work:** Individual

## Learning objectives

After completing A0, you should be able to:

- distinguish a workspace, package, node, topic, and message;
- source the ROS 2 underlay and your workspace overlay;
- build and run an `ament_python` package;
- use official ROS 2 documentation to locate an example and answer questions;
- inspect nodes, topics, message types, and publication rates from the command line;
- make and verify a small change to an existing ROS 2 example; and
- leave a reproducible record of what you ran and what you observed.

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

## Part 3 — Follow the authoritative example

Use the official ROS 2 Jazzy tutorial, [Writing a simple publisher and subscriber (Python)](https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Publisher-And-Subscriber.html), as your starting point.

Create the package `lab0_first_contact` in this repository. Your completed repository should contain:

```text
lab0_first_contact/
├── package.xml
├── resource/
│   └── lab0_first_contact
├── setup.cfg
├── setup.py
└── lab0_first_contact/
    ├── __init__.py
    ├── status_monitor.py
    └── status_publisher.py
```

If this repository is cloned inside `~/rse_ws/src`, build from the workspace root:

```bash
cd ~/rse_ws
colcon build --symlink-install --packages-select lab0_first_contact
source install/setup.bash
```

Use `--symlink-install` in this course when building Python packages. It lets many Python-only edits take effect without rebuilding, although metadata and entry-point changes still require a rebuild.

## Part 4 — Make the example yours

Adapt the official example to meet this specification:

### `status_publisher`

- Node name: `status_publisher`
- Topic: `/lab0/status`
- Message type: `std_msgs/msg/String`
- Rate: 2 Hz (one message every 0.5 seconds)
- Message content: must include `System ready` and an increasing count
- Console log: should make the published message visible

### `status_monitor`

- Node name: `status_monitor`
- Topic: `/lab0/status`
- Message type: `std_msgs/msg/String`
- Console log: should identify the received message

Expose both programs as ROS 2 executables with these exact names:

```bash
ros2 run lab0_first_contact status_publisher
ros2 run lab0_first_contact status_monitor
```

Do not copy code from an AI system or an unofficial tutorial without checking it against the official ROS 2 Jazzy documentation. In `evidence/documentation.md`, identify the official page and record where you found the package, publisher, subscriber, build, and run instructions.

## Part 5 — Verify your system

Run both of your nodes, then verify the system from a third terminal. Your evidence should establish all of the following:

- both expected node names appear;
- `/lab0/status` exists and uses `std_msgs/msg/String`;
- the topic has one publisher and one subscriber;
- a real message contains the required status text and a count; and
- the observed rate is reasonably close to 2 Hz.

Choose commands that provide that evidence. The Part 2 chain is a useful model, but you should adapt names and arguments rather than blindly pasting it.

Record the commands, compact output excerpts, and your interpretation in `evidence/inspection.md`.

## Part 6 — Explain what you built

Complete `evidence/reflection.md`. Your explanation should connect:

- the Python class and `main()` function;
- the executable names in `setup.py`;
- the package metadata in `package.xml`; and
- the nodes and topic visible in the running ROS graph.

Students enrolled in CPE 669 must also include the output of `ros2 topic info /lab0/status --verbose` and a 150–250 word explanation of what the publisher/subscriber endpoint and QoS information means for this system.

## Run the repository checks

The repository includes checks that look for common structural mistakes before you submit. Classroom 50 runs the same checks when you submit:

```bash
python3 -m pytest -q
```

These checks cannot prove that your live ROS graph behaved correctly. That is why your inspection evidence and explanation are required.

## Submission checklist

- [ ] The repository is pushed to GitHub.
- [ ] I ran `gh student submit`, and the latest automated checks pass or I have explained a remaining failure.
- [ ] `lab0_first_contact` builds with `colcon build --symlink-install`.
- [ ] Both executables run using `ros2 run`.
- [ ] All three files in `evidence/` are complete.
- [ ] Output excerpts are short and readable; no screenshots are required.
- [ ] I did not commit `build/`, `install/`, or `log/` directories.

## When to ask for help

Ask for help immediately if any of these happen:

- `source /opt/ros/jazzy/setup.bash` reports that the file does not exist;
- `printenv ROS_DISTRO` does not report `jazzy`;
- the demo nodes cannot be found after sourcing ROS 2;
- you see nodes or topics belonging to another student after setting your assigned `ROS_DOMAIN_ID`; or
- Git authentication prevents you from cloning or pushing.

For a build or code problem, first spend about 15 focused minutes on this sequence:

1. Read the complete error, including the first error rather than only the last line.
2. Confirm your current directory and which setup files you sourced.
3. Compare the relevant file with the official Jazzy tutorial.
4. Run the narrowest useful check again.
5. Commit or save your current work.

Then ask for help. Include the command you ran, the complete error text, what you expected, what you already checked, and a link to your latest pushed commit. This is enough information for someone else to begin debugging with you.

## Assessment

| Area | Points | Evidence |
|---|---:|---|
| Environment and reproducibility | 15 | Correct repository/workspace use, sourcing record, clean repository |
| Baseline ROS 2 inspection | 20 | Part 2 command chain and interpretations |
| Adapted publisher/subscriber | 30 | Package, nodes, topic, message, rate, entry points |
| Verification of the modified system | 20 | Commands and compact output supporting each required claim |
| Documentation trail and explanation | 10 | Official sources and code–metadata–graph explanation |
| Git workflow and submission quality | 5 | Meaningful commits, pushed work, readable evidence |
| **Total** | **100** | |
