import time
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import tensorflow as tf

import matplotlib.pyplot as plt
import matplotlib.animation as animation




N = 100

# 100 threads are available for each row
MAX_ROW_WORKERS = 100

# Animation speed
FPS = 12



tf.random.set_seed(42)

A = tf.random.uniform(
    (N, N),
    minval=0,
    maxval=10,
    dtype=tf.float32
).numpy()

B = tf.random.uniform(
    (N, N),
    minval=0,
    maxval=10,
    dtype=tf.float32
).numpy()



C = np.full(
    (N, N),
    np.nan,
    dtype=np.float32
)



def compute_cell(i, j):

    """
    Calculates one element of Matrix C.

    C[i][j] =
        A[i][0] * B[0][j]
        +
        A[i][1] * B[1][j]
        +
        ...
        +
        A[i][99] * B[99][j]

    This function runs inside a worker thread.
    """

    
    row = A[i, :]

   
    col = B[:, j]

   
    products = tf.multiply(row, col)

    
    value = tf.reduce_sum(products)

    #
    C[i, j] = value.numpy()



def compute_row_threaded(i):

    """
    Calculates one complete row of Matrix C.

    Each output cell in this row is submitted as a
    separate threaded task.

    Therefore:

        Row 1  -> 100 threaded tasks
        Row 2  -> 100 threaded tasks
        ...
        Row 100 -> 100 threaded tasks

    Total output cells = 10,000
    """

    with ThreadPoolExecutor(
        max_workers=MAX_ROW_WORKERS,
        thread_name_prefix=f"row{i}"
    ) as pool:

        futures = []

        
        for j in range(N):

            future = pool.submit(
                compute_cell,
                i,
                j
            )

            futures.append(future)

        
        for future in futures:

            future.result()




fig, axes = plt.subplots(
    1,
    3,
    figsize=(13, 5)
)




fig.patch.set_facecolor("#0b0e14")

for ax in axes:

    ax.set_facecolor("#0b0e14")

    ax.set_xticks([])

    ax.set_yticks([])



axA, axB, axC = axes


axA.set_title(
    "Matrix A\n100 × 100",
    color="white",
    fontsize=12,
    fontweight="bold"
)



axB.set_title(
    "Matrix B\n100 × 100",
    color="white",
    fontsize=12,
    fontweight="bold"
)


axC.set_title(
    "Result C — 0 / 10000 cells",
    color="white",
    fontsize=12,
    fontweight="bold"
)


imA = axA.imshow(
    A,
    cmap="viridis",
    vmin=0,
    vmax=9
)


imB = axB.imshow(
    B,
    cmap="plasma",
    vmin=0,
    vmax=9
)


imC = axC.imshow(
    np.zeros(
        (N, N),
        dtype=np.float32
    ),
    cmap="magma",
    vmin=0,
    vmax=8100
)



row_marker, = axA.plot(
    [],
    [],
    color="#f5a524",
    linewidth=2
)




col_marker, = axB.plot(
    [],
    [],
    color="#f5a524",
    linewidth=2
)


status_text = fig.text(
    0.5,
    0.02,
    "Starting threaded matrix multiplication...",
    ha="center",
    color="#9aa7b8",
    fontsize=10,
    family="monospace"
)



start_time = time.time()



def animate(frame_row):



    compute_row_threaded(frame_row)

    row_marker.set_data(
        [-0.5, N - 0.5],
        [frame_row, frame_row]
    )

    col_marker.set_data(
        [frame_row, frame_row],
        [-0.5, N - 0.5]
    )

    filled = np.nan_to_num(
        C,
        nan=0.0
    )

    imC.set_data(filled)


    
    completed_cells = (frame_row + 1) * N


    axC.set_title(
        f"Result C — {completed_cells} / {N * N} cells",
        color="white",
        fontsize=12,
        fontweight="bold"
    )

    percentage = (
        completed_cells /
        (N * N)
    ) * 100


    elapsed = time.time() - start_time

    speed = completed_cells / max(
        elapsed,
        0.001
    )


    status_text.set_text(

        f"Row {frame_row + 1}/{N} completed  |  "
        f"{completed_cells}/{N * N} cells  |  "
        f"{percentage:.1f}%  |  "
        f"{speed:.0f} cells/sec  |  "
        f"{N} threads"
    )


    return (
        imC,
        row_marker,
        col_marker,
        status_text
    )

def main():

    print("=" * 60)

    print(
        "THREAD-BASED MATRIX MULTIPLICATION"
    )

    print("=" * 60)

    print()

    print(
        f"Matrix A : {N} x {N}"
    )

    print(
        f"Matrix B : {N} x {N}"
    )

    print(
        f"Matrix C : {N} x {N}"
    )

    print()

    print(
        f"Total output cells : {N * N}"
    )

    print(
        f"Threads per row    : {MAX_ROW_WORKERS}"
    )

    print(
        f"Total multiplication operations : {N * N * N}"
    )

    print()

    print(
        "Starting LIVE animation..."
    )

    print()


    anim = animation.FuncAnimation(

        fig,

        animate,

        frames=N,

        interval=1000 // FPS,

        blit=False,

        repeat=False,

        cache_frame_data=False
    )


    
    plt.tight_layout(
        rect=[
            0,
            0.06,
            1,
            0.96
        ]
    )


    # Open the animation window
    plt.show()

    print()

    print(
        "Animation finished."
    )

    print(
        "Checking result using TensorFlow..."
    )


    C_tf = tf.matmul(
        A,
        B
    ).numpy()

    max_diff = float(
        np.max(
            np.abs(
                C -
                C_tf
            )
        )
    )


    print()

    print(
        f"Maximum difference from TensorFlow result: "
        f"{max_diff:.6f}"
    )


    if max_diff < 1e-2:

        print(
            "✓ Threaded result matches TensorFlow result!"
        )

    else:

        print(
            "✗ Result mismatch!"
        )


    
    np.savetxt(
        "matrix_A.csv",
        A,
        delimiter=","
    )

    np.savetxt(
        "matrix_B.csv",
        B,
        delimiter=","
    )

    np.savetxt(
        "matrix_C_result.csv",
        C,
        delimiter=","
    )


    print()

    print(
        "Matrices saved successfully:"
    )

    print(
        "  matrix_A.csv"
    )

    print(
        "  matrix_B.csv"
    )

    print(
        "  matrix_C_result.csv"
    )

    print()

    print(
        "Program completed successfully!"
    )


if __name__ == "__main__":

    main()