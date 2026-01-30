# Concurrency Mastery - Expert Patterns

## Lock-Free Algorithms

### Compare-And-Swap (CAS)
```cpp
// Lock-free stack
template<typename T>
class LockFreeStack {
    struct Node { T data; Node* next; };
    std::atomic<Node*> head{nullptr};
    
public:
    void push(T value) {
        Node* node = new Node{value, head.load()};
        while (!head.compare_exchange_weak(node->next, node));
    }
    
    bool pop(T& result) {
        Node* node = head.load();
        while (node && !head.compare_exchange_weak(node, node->next));
        if (!node) return false;
        result = node->data;
        delete node;
        return true;
    }
};
```

### Memory Ordering
```rust
// Acquire-Release semantics
use std::sync::atomic::{AtomicBool, Ordering};

static FLAG: AtomicBool = AtomicBool::new(false);
static mut DATA: i32 = 0;

// Writer thread
unsafe {
    DATA = 42;
    FLAG.store(true, Ordering::Release); // Synchronizes-with acquire
}

// Reader thread
if FLAG.load(Ordering::Acquire) {
    unsafe { println!("{}", DATA); } // Guaranteed to see 42
}
```

## Actor Model

### Erlang Pattern
```erlang
% Supervisor with restart strategy
-module(worker_supervisor).
-behaviour(supervisor).

init([]) ->
    {ok, {{one_for_one, 5, 10},
          [{worker, {worker, start_link, []},
            permanent, 5000, worker, [worker]}]}}.

% Worker process
-module(worker).
handle_call({process, Data}, _From, State) ->
    Result = heavy_computation(Data),
    {reply, Result, State}.
```

### Akka (Scala)
```scala
class WorkerActor extends Actor {
  def receive = {
    case Work(data) =>
      val result = process(data)
      sender() ! Result(result)
    case Shutdown =>
      context.stop(self)
  }
}

val system = ActorSystem("MySystem")
val worker = system.actorOf(Props[WorkerActor])
worker ! Work(data)
```

## CSP (Communicating Sequential Processes)

### Go Channels
```go
// Pipeline pattern
func generator(nums ...int) <-chan int {
    out := make(chan int)
    go func() {
        for _, n := range nums {
            out <- n
        }
        close(out)
    }()
    return out
}

func square(in <-chan int) <-chan int {
    out := make(chan int)
    go func() {
        for n := range in {
            out <- n * n
        }
        close(out)
    }()
    return out
}

// Fan-out, fan-in
func merge(cs ...<-chan int) <-chan int {
    var wg sync.WaitGroup
    out := make(chan int)
    
    output := func(c <-chan int) {
        for n := range c {
            out <- n
        }
        wg.Done()
    }
    
    wg.Add(len(cs))
    for _, c := range cs {
        go output(c)
    }
    
    go func() {
        wg.Wait()
        close(out)
    }()
    return out
}
```

## STM (Software Transactional Memory)

### Haskell STM
```haskell
import Control.Concurrent.STM

type Account = TVar Int

transfer :: Account -> Account -> Int -> STM ()
transfer from to amount = do
    fromBalance <- readTVar from
    toBalance <- readTVar to
    writeTVar from (fromBalance - amount)
    writeTVar to (toBalance + amount)

-- Atomic execution
atomically $ transfer account1 account2 100
```

## Async/Await Patterns

### Rust Tokio
```rust
use tokio::time::{sleep, Duration};

async fn fetch_data(url: &str) -> Result<String, Error> {
    let response = reqwest::get(url).await?;
    let body = response.text().await?;
    Ok(body)
}

#[tokio::main]
async fn main() {
    let results = tokio::join!(
        fetch_data("url1"),
        fetch_data("url2"),
        fetch_data("url3")
    );
}
```

### Python asyncio
```python
import asyncio

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
```

## Race Condition Detection

### ThreadSanitizer
```bash
# Compile with TSan
g++ -fsanitize=thread -g program.cpp -o program
./program

# Output shows race:
# WARNING: ThreadSanitizer: data race
#   Write of size 4 at 0x7b0400000000 by thread T1
#   Previous read of size 4 at 0x7b0400000000 by main thread
```

### Helgrind (Valgrind)
```bash
valgrind --tool=helgrind ./program

# Detects:
# - Lock ordering problems
# - Data races
# - Misuse of POSIX pthreads API
```

## Deadlock Prevention

### Lock Ordering
```cpp
class BankAccount {
    std::mutex m;
    int balance;
    
public:
    // Always lock in consistent order
    static void transfer(BankAccount& from, BankAccount& to, int amount) {
        // Order by address to prevent deadlock
        std::mutex& first = (&from < &to) ? from.m : to.m;
        std::mutex& second = (&from < &to) ? to.m : from.m;
        
        std::lock_guard<std::mutex> lock1(first);
        std::lock_guard<std::mutex> lock2(second);
        
        from.balance -= amount;
        to.balance += amount;
    }
};
```

### Try-Lock Pattern
```cpp
bool try_transfer(BankAccount& from, BankAccount& to, int amount) {
    std::unique_lock<std::mutex> lock1(from.m, std::defer_lock);
    std::unique_lock<std::mutex> lock2(to.m, std::defer_lock);
    
    if (std::try_lock(lock1, lock2) == -1) {
        from.balance -= amount;
        to.balance += amount;
        return true;
    }
    return false; // Retry later
}
```

## Performance Patterns

### Work Stealing
```cpp
class WorkStealingQueue {
    std::deque<Task> tasks;
    std::mutex m;
    
public:
    void push(Task t) {
        std::lock_guard<std::mutex> lock(m);
        tasks.push_back(t);
    }
    
    bool pop(Task& t) {
        std::lock_guard<std::mutex> lock(m);
        if (tasks.empty()) return false;
        t = tasks.back();
        tasks.pop_back();
        return true;
    }
    
    bool steal(Task& t) {
        std::lock_guard<std::mutex> lock(m);
        if (tasks.empty()) return false;
        t = tasks.front();
        tasks.pop_front();
        return true;
    }
};
```

### Thread Pool
```go
type ThreadPool struct {
    tasks chan func()
    wg    sync.WaitGroup
}

func NewThreadPool(workers int) *ThreadPool {
    p := &ThreadPool{tasks: make(chan func(), 100)}
    for i := 0; i < workers; i++ {
        go p.worker()
    }
    return p
}

func (p *ThreadPool) worker() {
    for task := range p.tasks {
        task()
        p.wg.Done()
    }
}

func (p *ThreadPool) Submit(task func()) {
    p.wg.Add(1)
    p.tasks <- task
}
```

## Common Pitfalls

### Double-Checked Locking (WRONG)
```cpp
// BROKEN - don't use
Singleton* getInstance() {
    if (instance == nullptr) {  // Check 1
        lock_guard<mutex> lock(m);
        if (instance == nullptr) {  // Check 2
            instance = new Singleton();  // Not atomic!
        }
    }
    return instance;
}

// CORRECT - use atomic
atomic<Singleton*> instance{nullptr};
mutex m;

Singleton* getInstance() {
    Singleton* tmp = instance.load(memory_order_acquire);
    if (tmp == nullptr) {
        lock_guard<mutex> lock(m);
        tmp = instance.load(memory_order_relaxed);
        if (tmp == nullptr) {
            tmp = new Singleton();
            instance.store(tmp, memory_order_release);
        }
    }
    return tmp;
}
```

### ABA Problem
```cpp
// Problem: Value changes A→B→A, CAS succeeds incorrectly
// Solution: Use versioned pointers
template<typename T>
struct VersionedPtr {
    T* ptr;
    uint64_t version;
};

atomic<VersionedPtr<Node>> head;

void push(T value) {
    Node* node = new Node{value};
    VersionedPtr<Node> old_head = head.load();
    do {
        node->next = old_head.ptr;
    } while (!head.compare_exchange_weak(
        old_head,
        {node, old_head.version + 1}
    ));
}
```