# Inspection record

Replace every bracketed prompt with your own observation. Keep output excerpts short.

## Part 1: First observation

**What appears to be happening?**  
[Your answer]

**What did you observe that supports this?**  
[Your answer]

## Part 2: Standard demo

### Running nodes

**Command:** `[command]`

```text
[relevant output]
```

**Interpretation:** [What does this tell you?]

### Connections and message type

**Commands:**

```text
[commands]
```

```text
[relevant output]
```

**Interpretation:** [Identify the publisher, subscriber, topic, and message structure.]

### Message and rate

**Commands:**

```text
[commands]
```

```text
[relevant output]
```

**Interpretation:** [Describe one message and the approximate rate.]

## Part 4: Your status system

### Nodes and topic

**Commands and relevant output:**

```text
[commands and output]
```

**Interpretation:** [Explain how this supports the required node names, topic, type, publisher, and subscriber.]

### Message and rate

**Commands and relevant output:**

```text
[commands and output]
```

**Interpretation:** [Explain how this supports the required message content and 4 Hz rate.]

## Part 6: Your count system

**Commands and relevant output:**

```text
[commands and output]
```

**Interpretation:** [Explain how this supports the node names, /lab0/count topic, Int32 type, publisher/subscriber connection, increasing values, and 1 Hz rate.]

## CPE 691 extension

Delete this section if you are enrolled in CPE 491.

```text
[output of ros2 topic info /lab0/status --verbose]
```

```text
[output of ros2 topic info /lab0/count --verbose]
```
