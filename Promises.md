# Summary #
Promises, (or _Futures_ in the original Active Object notation) are objects representing a future state, or result, of a concurrent operation. Work is performed with requests, and a promise represents the fullfilment of a request. Promises allow the programmer to concentrate on the higher-level synchronization of the system, thinking in terms of the tasks performed instead of in terms of low-level primitives.

Promises are related to [lazy evaluation](LazyEvaluation.md) and [capabilities](Capabilities.md).

See the Limitations section in the end of this page for final conclusions and how promises relate to LiveProgramming.

See also ConcurrencyModels.

# Background #
Promises should address the [issues of traditional synchronization techniques](SynchronizationProblems.md).

For those who are familiar with Twisted, the Python asynchronous framework, the concept of Promises is similar to Deffered objects in Twisted. See [Twisted's Deferred objects](http://twistedmatrix.com/projects/core/documentation/howto/defer.html).

# What is a promise? #
In a programming task we can note "request granting" parts of the system. In concurrent systems the goal is to process indepedant requests in parallel. Normally, a request granter (such as an object with a method) is blocking - a method returns when the request is granted. For parallelization, we need to create threads in which we process independant requests. With promises, the concept of a thread is hidden from the programmer. A request granter **never** blocks and methods return immediately, and its immediate result is a **promise** for the fulfillment of the request.

A promise is an object that looks exactly like the result. Every operation on the result can also be performed on the promise. Many such operations can be _invoked_ on the promise while the request is being processed concurrently. Once the result is really available, all the invoked operations on the promise are actually performed on the real result.

Working with promises has it's methodologies. For example, sometimes a result is needed before the program can continue (such as printing the result on the screen so that the user can make a choice). For these cases, we have to wait for the promise to be fulfilled, and a special mechanism exists for this purpose (such as the "when" keyword in E). Obviously, many design patterns can be thought of for working with promises.

### Example ###
The almost surprising fact is that we humans are generally concurrent coordinators. This does not refer to the ability to perform several tasks at once. The point here is the ability to _use_ many asynchronous objects in a coordinated way. We don't (usually) use semaphores or other low-level synchronization primitives. So how do we do it?

The human way of concurrency depends a lot on _assumptions_. We assume that a certain future state will occur, and plan our actions accordingly. This will be illustrated by an example:

#### Loktar's pizza place ####
Loktar is a manager of a pizza place. To speed up work, he decides to hire two workers, Rubin and Berko. Loktar wants to handle incoming pizza requests. For each incoming phonecall, Rubin should answer the phone and write down the order. Then, for every order, Berko should make a pizza.

With us humans, this isn't hard. Loktar tells Rubin: "When the phone rings, answer and write an order". He then goes to Berko and says: "When an order is ready, read it and make a pizza". Then Loktar goes to play Solitaire and has nothing to worry about. For interest, we will add another requirement: no more than MAX\_ORDERS\_WAITING written orders should be waiting for Berko to handle, at any time. If more phonecalls arrive, Rubin should not answer the phone until Berko makes at least one pizza (handles at least one order).

With current synchronization techniques, we will need to create two threads: one for Rubin and one for Berko (for clarity we will use textual pseudo-code to illustrate). In total we have three threads: Loktar is the "main" thread and he has two "worker" threads.

For Rubin:
```
def Rubin(orderlist):
   while True:
      if orderlist.length() > MAX_ORDERS_WAITING:
         sleep(1)
         continue
      order = make_order()
      orderlist.append(order)
```
For Berko:
```
def Berko(orderlist):
   while True:
      order = orderlist.pop(0)
      make_pizza(order)
```
For Loktar:
```
def Loktar():
   orderlist = ThreadSafeList()
   new_thread(rubin)
   new_thread(berko)
   while True:
      play_solitaire()
```

Of course, orderlist must be thread safe, or we will have bugs. Also, the infinite loop must be replaced by something that tells them when to stop.

With promises, this looks simpler, and Rubin and Berko don't have to be described specifically:
```
def Loktar():
   make_order.result.set_max_unrealized(MAX_ORDERS_WAITING)
   play_solitaire()
   while True:
      order = make_order()
      pizza = make_pizza(order)
```
All "functions" here return immediately. play\_solitaire begins a solitaire game and returns. make\_order is a "function", or request granter, that returns a **promise** for a "order" object. Any request granter may have a "result" sub-object, which symbolizes the result of this request. Here we set the maximum number of concurrently unrealized results, that is - the number of requests that have not been granted (number of pizza orders that have requested but not created yet). This way, no more than MAX\_ORDERS\_WAITING orders will be pending in the system, and no more requests for getting new pizza orders will be sent until some orders are actually written down. This replaces the low-level mechanism used above.

The concurrency in this case is somewhat implicit. By writing two independant request granters (make\_order and make\_pizza) we allow the system to automatically run these concurrently. The system will know that make\_pizza requires a real order to "realize" the pizza promise, but that it may run independantely of new incoming orders. With AdaptiveProfiling, the system will automatically, dynamically decide how many threads to run (and on which machine).

We could add more explicit control over how this is made concurrent, by using policy control for each request. For example, if we want one thread for make\_order, and one thread for make\_pizza, we will write:
```
   make_order.set_policy("one thread")
   make_pizza.set_policy("one thread")
```
If we want to change the application so a new thread is created for every pizza, we would simply write:
```
   make_pizza.set_policy("new thread for each request")
```

Using promises is like scheduling operations that will occur each after the previous one completes, without explicitly using a scheduling primitive. The scheduling is in the form of a tree, where each succesful "realization" of a promised result may trigger several new actions to realize further results. Or, if viewed from the opposite direction, several operations may depend on a single result to become available. This allows us to construct complex event-handling trees in a very natural and simple way.

# Implementation #
A promise system requires:
  * The side of "promises" as seen by the requested (or promise-disptaching) side. This includes the ability to return immediately a "promise" rather than a real result, and the ability to trigger a realization of the promise when the asynchronous operation has completed.
  * A "promise" primitive for the requesting side. This is an object that remembers what operations were invoked on it, and performs them when the promise becomes "realized".

There are other things that may be implemented to take better advantage of a "promising" system:
  * It will be better to allow a "decoration" technique that allows asynchronous processes to be implemented without having to explicitly return promise objects. This "wrapping" level will automatically transform any asynchronous request into one that returns a promise.
  * Further, we may then design and program the system (if it isn't too complex) in a way that is not dependant on which operations are asynchronous and which are not.

# Realizing promises #
Each tree of operations has a root - a "primeval" promise on which all other promises depend. When that root promise is realized, the whole tree begins to execute. Where I/O or other side effects depend on the promised result, the promise infrastructure will cause "blocking" on the side effect operation until the promise is realized. This will ensure that side effects will occur in the expected order, and not on the random order of promise realization. Compared to traditional systems, this ensures that blocking operations are used only when they are required.

# Promises and Adaptive Profiling #
Concurrency sometimes means that parts of the applications are distributed over a network. For [Adaptive Profiling](AdaptiveProfiling.md) we may use promises to implement the feature of moving a part of the system to a remote host. The other parts of the system will continue using it and will now receive "promises" instead of immediate results. Because of the transparent nature of promises (they look like the real result) this will not affect the operation of the system.

This can lead to much better performance in a system that performs several operations with the (newly) remote object and then a lot of unrelated operations on a local object. The system will not get "stuck" on the remote operations, waiting for the reply. Rather it will already begin the next unrelated local operations. When the remote operations will complete, the operations that depended on them (the operations performed on those promises) will be executed. If the system reaches a point where a local operation depends on a remote promise that has not been realized, it will proceed to "virtual work" by invoking operations on the promise. These operations will occur when the promise will be realized, i.e. when the remote operation completes and a reply arrives.

# Promises and Lazy Evaluation #
[Lazy Evaluation](LazyEvaluation.md) is closely related to promises in that it does not really perform any operation on an object until we know that a side effect depends on it. This way, minimal calculation is performed. If we request a result from an asynchronous object, and receive a promise, with lazy evaluation we will NOT actually even send the request unless it is determined that the result will be used. This can lead to great performance improvements and resource savings.

For example, we may request something from an asynchronous object, and get a promise for that result. Later in the code, we perform a different operation and depending on the result of that later operation, perform different tasks. If only one of the tasks require the original first promise, we can delay sending the request until the condition has been determined. This can lead to optimization if the _other_ task is to be performed, but also to a delay if the original result is in fact required. To cope with this we may implement a system that compensates by sending requests immediately but canceling them prematurely if it is later discovered that they are not actually needed (we will need to implement operation cancelling for the result which may be hard).

The conclusion is that promises and lazy evaluation must be studied further, and that maybe profiling methods should be employed.

# Limitations #

Promises are a solution of a problem in the domain of object-oriented programming. The solution is to use "future results" and to assume they will arrive. However, in different programming methods including actor-based programming and possibly functional programming, promises may not be neccesary in the first place. On the other hand, even in those models concurrency takes place and maybe a promise-like concept can be used. A possible additional use is system analysis where a "promise" will be the future state (or next state as in feedback systems) of the system.

## Promises and Live Programming ##

_Todo - describe this_

# References #
_todo complete this list_

  * E in a Walnut
  * Original paper on Active Objects by ??