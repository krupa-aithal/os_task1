package pcdemo;

import java.util.LinkedList;
import java.util.Queue;

public class ProducerConsumer {

    public static void main(String[] args) throws InterruptedException {

        SharedBuffer buffer = new SharedBuffer(10);
        int itemCount = 20;

        Thread producer1 =
                new Thread(new Producer(buffer, itemCount), "Producer-1");

        Thread consumer1 =
                new Thread(new Consumer(buffer, itemCount), "Consumer-1");

        producer1.start();
        consumer1.start();

        producer1.join();
        consumer1.join();

        System.out.println("\nProducer and Consumer have finished.");
    }
}


class SharedBuffer {

    private final Queue<Integer> queue = new LinkedList<>();
    private final int capacity;

    public SharedBuffer(int capacity) {
        this.capacity = capacity;
    }


    public synchronized void produce(int item)
            throws InterruptedException {

        while (queue.size() == capacity) {

            System.out.println(
                    "[BUFFER FULL] "
                    + Thread.currentThread().getName()
                    + " waiting..."
            );

            wait();
        }

        queue.add(item);

        System.out.println(
                Thread.currentThread().getName()
                + " produced -> " + item
                + "  | buffer size = " + queue.size()
        );

        notifyAll();
    }


    public synchronized int consume()
            throws InterruptedException {

        while (queue.isEmpty()) {

            System.out.println(
                    "[BUFFER EMPTY] "
                    + Thread.currentThread().getName()
                    + " waiting..."
            );

            wait();
        }

        int item = queue.poll();

        System.out.println(
                Thread.currentThread().getName()
                + " consumed -> " + item
                + "  | buffer size = " + queue.size()
        );

        notifyAll();

        return item;
    }
}


class Producer implements Runnable {

    private final SharedBuffer buffer;
    private final int itemCount;


    public Producer(SharedBuffer buffer, int itemCount) {
        this.buffer = buffer;
        this.itemCount = itemCount;
    }


    @Override
    public void run() {

        try {

            for (int value = 1; value <= itemCount; value++) {

                buffer.produce(value);

                Thread.sleep(
                        (long) (Math.random() * 500)
                );
            }

            System.out.println(
                    Thread.currentThread().getName()
                    + " finished producing "
                    + itemCount + " items."
            );

        } catch (InterruptedException e) {

            Thread.currentThread().interrupt();
        }
    }
}


class Consumer implements Runnable {

    private final SharedBuffer buffer;
    private final int itemCount;


    public Consumer(SharedBuffer buffer, int itemCount) {
        this.buffer = buffer;
        this.itemCount = itemCount;
    }


    @Override
    public void run() {

        try {

            for (
                int consumedSoFar = 1;
                consumedSoFar <= itemCount;
                consumedSoFar++
            ) {

                buffer.consume();

                Thread.sleep(
                        (long) (Math.random() * 800)
                );
            }

            System.out.println(
                    Thread.currentThread().getName()
                    + " finished consuming "
                    + itemCount + " items."
            );

        } catch (InterruptedException e) {

            Thread.currentThread().interrupt();
        }
    }
}