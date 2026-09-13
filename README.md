# 🧵 Multithreading Assignment

## 📌 Overview

This project demonstrates two multithreading problems:

1. **Producer-Consumer Problem** using Java Threads
2. **Matrix Multiplication** using Python Threads + TensorFlow, with Animation

---

## 📂 Files in this Repository

| File | Description |
|---|---|
| `ProducerConsumer.java` | Producer-Consumer problem using Java threads |
| `matrix_multiply_tf_animated.py` | 100×100 matrix multiplication using Threads + TensorFlow with animation |
| `animation.gif.mp4` | Video demonstration of the matrix multiplication |
| `README.md` | Project documentation |

---

## 1️⃣ Producer-Consumer Problem

The Producer-Consumer problem is implemented using Java threads and a shared, fixed-size buffer (backed by a `LinkedList`).

- The **Producer** adds items to the buffer.
- The **Consumer** removes items from the buffer.
- `synchronized` methods provide safe access to the shared buffer.
- `wait()` is used when the buffer is full or empty.
- `notifyAll()` is used to wake waiting threads.

The program uses a buffer of size **10** and produces/consumes **20** items.

### 🔹 Concepts Used

- Java Threads
- Shared Resource
- Synchronization
- `wait()`
- `notifyAll()`
- Bounded Buffer

### ▶️ How to Run

**Using Eclipse / IntelliJ:**
1. Create a Java project.
2. Add `ProducerConsumer.java` to the `src` folder (keep it inside a `pcdemo` package folder, since the class declares `package pcdemo;` — or delete that line to run it standalone).
3. Run it as a Java Application.

**Using the terminal:**
```bash
javac ProducerConsumer.java
java ProducerConsumer
```

### 🖥️ Sample Output

```
Producer-1 produced -> 1  | buffer size = 1
Consumer-1 consumed -> 1  | buffer size = 0
Producer-1 produced -> 2  | buffer size = 1
Producer-1 produced -> 3  | buffer size = 2
Consumer-1 consumed -> 2  | buffer size = 1
[BUFFER FULL] Producer-1 waiting...
[BUFFER EMPTY] Consumer-1 waiting...
...
Producer-1 finished producing 20 items.
Consumer-1 finished consuming 20 items.

Producer and Consumer have finished.
```

---

## 2️⃣ Matrix Multiplication using Threads + TensorFlow

Two 100×100 matrices are multiplied using Python threads and TensorFlow.

The program creates **10,000 output-cell tasks** — one for every cell of the result matrix.

```
Matrix A (100×100) × Matrix B (100×100)
                    ↓
             Matrix C (100×100)
```

### 🔹 How It Works

- `ThreadPoolExecutor` creates a pool of worker threads (100 threads per row).
- Each `(row, column)` pair is treated as a separate threaded task.
- TensorFlow performs the multiplication and summation using `tf.multiply()` + `tf.reduce_sum()`.
- The result is cross-checked against TensorFlow's own `tf.matmul()`.
- Matplotlib animates the computation live as it happens.

### 🎬 Animation

The animation shows:

- 🔵 **Matrix A** — an amber horizontal line marks the row currently being read.
- 🟣 **Matrix B** — an amber vertical line marks the column currently being read.
- 🟠 **Matrix C** — the result matrix fills in, row by row, as threads finish their cells.

### 🎬 Animation Output

<video src="animation.gif.mp4" controls width="600">
  Your browser (or GitHub's viewer) can't play the embedded video —
  <a href="animation.gif.mp4">click here to download/view it directly</a>.
</video>


### ▶️ Installation

Install the required packages:

```bash
pip install tensorflow numpy matplotlib pillow
```

### ▶️ Run

```bash
python matrix_multiply_tf_animated.py
```

The animation window opens automatically while the threads compute. Once it finishes, the script verifies the result against TensorFlow and saves the matrices.

### 🖥️ Sample Output

```
Multiplying A(100, 100) x B(100, 100)
One thread per output cell -> 100 threads per animated row, 100 rows -> 10000 threads total

Animation saved to matrix_multiplication_animation.gif

Total time (compute + render + save GIF): 14.82s
Max absolute difference vs tf.matmul: 0.003052
Threaded matrix multiplication matches TensorFlow's own result.
Saved matrix_A.csv, matrix_B.csv, matrix_C_result.csv
```

---

## 🛠️ Technologies Used

- Java
- Python
- TensorFlow
- ThreadPoolExecutor
- NumPy
- Matplotlib
- Multithreading

---

## 📋 Requirements

**Java**
- JDK 8 or above

**Python**
- Python 3.10 or 3.11
- TensorFlow
- NumPy
- Matplotlib
- Pillow

Install Python dependencies using:

```bash
pip install tensorflow numpy matplotlib pillow
```

---

## Releases

No releases published
