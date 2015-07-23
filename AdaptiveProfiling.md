# Summary #
Adaptive profiling is the ability of a system to change dynamically in a way that improves it's performance. The method of change is the duplication or movement of components between host platforms. This is made possible by [Capabilities](Capabilities.md), [OrthogonalPersistence](OrthogonalPersistence.md) and the ability of the operating system to transparentely serialize and move objects between hosts, while retaining their cross-references across a network, transparently.

# Background #
Software is typically made of a large complex of entities that communicate with each other. Some of these entities are actors (programs) and some are information (data). In local, non-networked programs, these entities are all running and stored in the same host computer.  In recent times, though, more of these entities are linked, referenced and distributed over a network.  Examples include:
  * The web (where the data sits separately from the browser code)
  * The X protocol (where the main code sits separately from the display code)
  * File system shares (where the file data sits separately from the code to access it)

Due to differing resources' availability and differing resource requirements of these hosts and components, and due to the dynamic nature of both, it is often desirable to dynmiaclly move or duplicate these components between host computers.

Due to the architecture of today's operating systems and languages, there is no way to seamlessly duplicate or move components between computers.

# A "component" #
A "component" is either code or data and has many properties:
  * Its size
  * Its behaviour or content
  * Its references and links to other components
  * Its requirements:
    * Space and space-performance (disk and ram availability)
    * Run speed (cpu power)
    * Communication speed (networking speed)

A component by itself is typically useless.  Its usefulness is usually a result of its inter-connection with other components. For example, a web browser is useless without its connection to the webpage data.  It is also useless without its connection to the screen, to display its data.

# Desirability of migrating components #
The above-mentioned resources are all limited, and have differing availabilities on different hosts. If a component is movable or duplicate-able from one host to the next, then the differing resource requirements of the components can be satisfied in a better way.

## Current examples of duplicated components ##
Nowadays, some components are already duplicate-able and seamlessly moved. This is a "cache" and it often duplicates components from one host to the other, when the communication speed is low. This is, however, just a limited form of duplication, and far more can be achieved.

## Examples of potential gains ##

### Web Browsers ###
Suppose we have a web site that contains a small code component that generates responses for browsers.  Lets call the web site computer Web-Site, and the client browser computer Web-Browser.  This is actually quite a common scenario.  Let us suppose that the code component in Web-Site is referencing a small piece of data in Web-Site and other sites in the net.  Web-Browser, who has a very slow connection, will have to send multiple requests to Web-Server, so that it runs the small code component, generate a small response, and send it back.  Web-Browser is perfectly capable of running the small code component, containing the small piece of data and referencing other sites, but due to the architecture of the system, it has to pay severe network penalties in order to access the functionality (This is even true now, as I am editing this wiki).  If the small code component, the small data and links to other sites were seamlessly copied to Web-Browser the performance of the system could be greatly enhanced.

### X server ###
You may or may not know, but an X server seamlessly transmits all of the mouse movements and clicks from your displaying computer to a client computer that runs the logic of the program.  Most of these network-hogging mouse movements are quickly discarded by a typically small section of the client logic code (the gui toolkit code).  If the Toolkit code was automatically and seamlessly moved to run in the displaying computer, most of the network use would be eliminated.

### File System shares ###
Almost every work environment and a lot of the home networks have multiple computers. A common way of sharing data is using file system shares, where remote files are accessed in a similar way to local ones.  This is done at the file system level, where reqeusts such as "list this directory" and "delete this file" are sent.  This is great when what you are doing over the share is listing directories and deleting files.  However, no request to "delete this entire directory and all subdirectories" exists, and definitely some more bizarre operations that may be requested by programs such as "get me a list of all files that end with .mp3 in this directory and all subdirectories" exist.  It doesn't make sense to add these requests to the shared file system protocol.  In order to implement these requests, many tiny requests are ping-ponged across the network (list directory, list subdirectory, delete file 1, delete file 2, etc etc), and it is often much more efficient to go and perform the high-level deletion request at the appropriate computer manually.

If the (small) code component that implements the high-level logic (for example enumerating all subdirectories and filtering files that have .mp3 in them) was seamlessly copied to the file system share computer, the requests would become local instead of hopping over a slower network.  This could speed up work with file system shares, without having to jump between controlling multiple computers.

### Distributed computing ###
A lot of work in computer science, is devoted to distributed computing, where specifically code components can be asked to run remotely in order to use the network's CPU resources more effectively.  Programs that are able to do this are specifically tailored for this need and profiled manually in order to decide how to distribute them.  With Adaptive Profiling, any code component would be able to be copied or moved to another computer in order to free up some cycles from a busy CPU and use up some cycles of an idle CPU.  This would make all programs properly distributed.

# How? #
Now that we've seen that the ability to move components in order to better utilize the resources of the computers of the network is desirable (and even very desirable in many cases), how do we go and implement it?

## The Operating System must know ##
Today, the entities operating systems know about are processes/threads, files, and the computer's objects/resources.  The operating system has no idea about how to interpret the content of the file, and it definitely has no idea about which components exist inside processes/threads.
In order to be able to move components between host computers, the components must be explicit. Instead of knowing processes/threads, the operating system must know the high-level objects and the type of each object. It must know the code in a high-level form (i.e: bytecode) that is possible to recompile for different architectures in order to utilize different computer architectures.

The operating system must also know about the references between the components. It must know the exact type of the refered object, and how it is referred, and from where.  Once it knows this, it may serialize local references into transparent [network references](NetworkReferences.md) to these components when sending the component to different host computers.

## Moving vs. Copying ##
Typically all immutable things can be copied across the network (i.e cached) whereas all mutable data must be either temporarily copied, or moved.  So in general, code components would be copied, as they are immutable, while a database would have to be moved.
All such movements or copying will be referred to as migrations.

## Desirability of moving components ##
Now that the operating system is capable of copying components between computers, it must decide when it is _desirable_ to do so.

In order to figure whether the migration of a component is desirable, we must take into account all of the gains and costs of the move.

### Costs ###
Migrating a component entails:
  * Serializing it
  * Transmitting it over the network
  * Deserializing it

Serializing and Deserializing are of negligible costs compared to the transmission over the network, and could thus be ignored.
The Operating System must be able to evaluate the costs of the migration, by estimating the cost of tranmission over the network. This cost entails the time required for the transmission (based on the object size and network speed) and the cost associated with that specific network tranmissions (i.e: pay-per-kilobyte).

### Gains ###
By migrating a component we achieve two things:
  * We shift use of resources from one computer to the next.
  * We change the topography of the links between components.

The resources we can shift are:
  * Fast Space (RAM, low-level caches, etc)
  * Slow space (Disk)
  * CPU usage
  * Network use

If the migration can move components such that less scarce resources are used, then gain is achieved.

The topography change means that some of the links between the components become remote instead of local, and some become local instead of remote.  If the migration can move components such that the heavier-traffic links become local and the lighter-traffic ones are remote, then gain is achieved.

### Profiling ###
In order to make an informed decision, the operating system must know of all these factors.  To do this it must profile the components.

  * Profiling Fast Space (RAM, low-level caches, etc) is not straightforward.  Applies only to code components (data components do not directly use or get stored in fast space). Fast Space is not explicitly requested by code components, but implicitly requested by "touching" (reading or writing) Slow Space.  What is interesting is not how much Fast Space was available to give the component, but how much it was implicitly asking for.  This is not a difficult problem, and it is easy to count the number of accessed and dirty pages of Slow Space touched by a code component.

  * Profiling Slow Space (Disk) is easy and consists of measuring the size of the component.  If it is a mutable data component, it can change in size, in which case a time-local (or time-global) maximum on the size of the component can be used.

  * Profiling CPU use is mostly a solved problem, and basically consists of increasing counters at all context switches between threads and interrupts. Applies only to code components.

  * Profiling Network Use applies only to code components and is also a solved problem. Basically measure the amount of data received or sent over the network by the component directly.

  * Profiling the traffic between components means counting the number and total size of the requests between components. Counting the number of requests is trivial and of negligble costs (consists of a single increment operation per inter-component call or access). Counting the "size" of these requests as if these requests are remote requires an estimate on the serialized size of the requests.  Since objects can simply provide this estimate in an efficient manner, this should not be too expensive as well.

### Decision ###
When deciding whether to make a migration, the operating system should measure the costs as described above, and calculate the gains.  In order to calculate the gains, it should consider each resource and its scarceness in each of the host computers.  It should obviously attempt to utilize resources in the host that is less scarce.  Perhaps more importantly, it should review the topography change and whether the links with the heavier traffic will become local or remote.

In reality, choosing when and how to perform migration is more complicated, as migration of a single small component will rarely yield positive results. Typically, migration would be useful when migrating a set of components and not just one.  While the logistics, method and required profiling of migrating a set of components are the same as of one component, the algorithms required to decide which components to migrate according to the profile-data are more complicated.

# Security Concerns #
The migration of components between computers raises a few security concerns and issues.

## Secrecy ##
Some components (both code and data) may be wanted to be kept secret. This is addressed by Special Cases below, but in general these components will simply not be migrated.

## Immutable Data ##
Immutable data can generally be migrated (since its immutable, copied) to other computers securely, as it gives no new authority to the receiving computer.

## Receiving and running code components ##
One of the main concerns about migrating components transparently is the trustworthyness of code components from a random computer.
In traditional systems, this is indeed a problematic issue.  However, as explained in [Capabilities](Capabilities.md), there is no need to trust code to run it as executables in a capability system are harmless. **Therefore, this is not a real security problem.** There are two main reasons for this:
  * The executables are transmitted between computers in a high-level language format (bytecode) and compiled locally to native code, so they cannot exploit local CPU bugs to take over the system.
  * The executables can only make requests via capabilities they have, and when they are transmitted across the network, they carry their capabilities with them.  While a compromised computer may freely forge capabilities to its own resources, it has no way of forging capabilities of another computer (As these will be cryptographically signed). Therefore, the only capabilities carried by the code component will be the exact same ones it had carried before migration. If it had no capabilities to any resources on the new hosting computer, but a few capabilities in the original hosting computer, then only requests to access objects on the original hosting computer will be possible. See [NetworkReferences](NetworkReferences.md).

## Sending a code component to another computer ##
_this section is (almost) a duplicate of the next section! remove either one_
When sending a code component to another computer, we are in fact trusting that other computer to properly run that component. That computer may instead fail to run the code component or run a different component instead (see next item: Sending capabilities to another computer).  The implications would be similar to that of lack of CPU resources.

Migrations of code objects would typically be:
  * To allow for distributed computing: In this case existing solutions already trust the computers to do the same thing.
  * To improve the topology of the "proxy" components: In this case the code component is a "proxy" between code or data components in the sending computer and code or data components in the receiving computer.  Since the receiving computer already controls the code or data components behind the proxy, it already holds the ability to halt or modify the code or data components' operation.

This means that **no such new security concerns are added for distributed computing**, and **no such security problem is introduced by migrating "proxy" components**.
In other cases, however, **this is indeed a legitimate concern and code components should only be sent to a computer trusted to actually give them runtime**.

## Sending code capabilities to another computer ##
When sending a code component to another computer, we must also send the accompanying references to objects (or [Capabilities](Capabilities.md)). If the receiving computer cannot be trusted to actually run the code component that was sent, but may instead abuse the given references, this is a security concern.

Migrations of code objects would typically be:
  * To allow for distributed computing: In this case existing solutions already allow the receiving computer access to the same shared resources.
  * To improve the topology of the "proxy" components: In this case the code component is a "proxy" between code or data components in the sending computer and code or data components in the receiving computer.  The "proxy" does not typically hold special capabilities other than access to the receiving computer resources.

This means that **no such new security concerns are added for distributed computing**, and that **no such security problem is introduced by migrating "proxy" components - as long as those do not hold (or are later given) special capabilities**.
In other cases, however, **this is indeed a legitimate concern and code components should only be sent to another computer if they do not have authority that might be compromised**.
In a modular system, most code components will actually be "proxies" between other components without a lot of authority, so their migration should not be a problem.

This raises the question: how should the operating system determine whether a code component has authority that must not be sent?

  * All immutable data can be sent (unless bound as secret) and does not add authority
  * All objects for which the receiving computer already has capabilities can be sent. This includes:
    * All capabilities to objects in the receiving computer
    * All capabilities that the receiving computer already has. In order to determine whether a receiving computer already has a capability, an object may have, in addition to a globally identifying capability, an identifier that is the same as a capability bar authority. The sending computer may challenge the receiving computer whether it has a capability to the same object, giving it only the identifier (which is not actual authority to access the object).
  * A list of "trusted" computers for this purpose may be set. This would typically include computers inside the LAN under the control of the same administrator.
Are all mutable data that are not already controlled by the

# Problems #
Migration of components can highly improve performance, simplify designs and reduce the need for redundant architectures meant to improve component topology, there are still a few problems (in addition to the above security concerns).

## Inconsistent Persistence ##
Mutable components have a state, and Code Components have running instances. This state is persisted automatically and orthogonally by the operating system.  If a power outage or other form of crash occurs, then these components may regress to a previous state.  As long as all components are in the same computer, they regress in unison and remain in sync. A problem arises when these components are spread across multiple computers, with differing persistencies.
If one host computer has a power outage, its components can revert to a previous state, while the components it was using/being-used-by did not revert.

In cases of a discrepency between a code component and a data component, this is typically not a problem. Code components' only have state if they have side effects on the data, in which case these side effects can be done atomically in transactions, such that any regression in code state will always remain in sync with the data and any regression in data state will revert whole transactions.

However, many data components may need to remain in sync with each other, and if some revert while others don't, it may pose a real problem.
The solution to this problem is simply to create component-sets that are bound together. This would typically apply to data components with such relationships, but also to bind code with its running instance data (typically called a "closure") which would force the entire closure to be migrated in unison.

## Fairness Concerns ##
When a host computer receives a component from another computer, it may de-prioritize it. An Operating System may also send components to run on other computers not because the resources on the other computer are less scarce or to improve the topology, but simply to abuse the resources of the other computer and save one's own resources.

_more on this later_

# Special cases #
Some components are strongly bound to a host computer. For example, the host's devices (mouse, keyboard) and their corresponding software components cannot be migrated (Until teleportation is possible :-).
Some components may be secret (a secret database) and one may not want to send them across the network to an untrusted host computer.
In these special cases it should ofcourse be possible to mark a component non-migratable.

# A Simpler Initial Version #
As this page demonstrates, this feature is intricate and implementing it is not simple.
In order to simplify the feature (especially with regard to security and fairness concerns) and allow for incremental development, a first version can simply establish a network of trust, where migration of components only occurs between fully trusting computers (the LAN, as well as perhaps trusted friends' computers).

# See Also #
[Capabilities](Capabilities.md)
[NetworkReferences](NetworkReferences.md)
[OrthogonalPersistence](OrthogonalPersistence.md)