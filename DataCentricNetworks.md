# Credit #

First, credit where credit is due: This idea is taken from [Van Jacobson](http://en.wikipedia.org/wiki/Van_Jacobson) (See Google Tech Talk about it in External References).
It is re-described here (with many of the same examples used in the original Tech Talk) for convenience purposes of the Enough project, and to allow expanding with more associated ideas we find in the future.

# Introduction #

Historically, communication networks achieved the goal of transmitting data between known endpoints.
Both the telephony networks and the internet have worked towards achieving this goal in different ways (The difference between those is well explained in the Google Tech Talk).

This model may fit in some cases: Namely when what the nodes really want is to communicate with other named nodes (for example, send a short message to a specific node in the network).  However, the vast majority of communication in the internet today (and most probably, in the future as well) does not fit this model.  What nodes really want most of the time is:
  * To download a piece of named data.
  * To "broadcast" or publish a piece of data.

We don't care which end points we get the data from, we just want the data.
Today, there is no way for the nodes to communicate their **intent** to the network ("I want today's New York Times") but instead, they must request to speak with www.newyorktimes.com, establish a pipe, and in that pipe request that piece of data.

The result of this is that data is inefficiently and unnecessarily redistributed over the same network pipes again and again.
If instead, we could communicate our intent, the closest router, or a nearby computer in the network could possibly say "Hey! I have today's New York Times!".

# Security #

Today, the authenticity of the data we receive is established by using secure pipes to the entities we trust have the authentic data.
In a data-centric network, the data itself must carry the proof of authenticity, for example via a cryptographic signature.

Once incorrect signatures are discovered, the data can be invalidated and the invalidation can propagate throughout the network.

# Immutability #

If this is to work efficiently, data must no longer have a "true location" (as it would using transparent proxying caches), but instead its validity must be the same wherever it is, and its source/authenticity must be carried within itself. This means that data put into the network must be "immutable". This implies that the data label must include something such as a version that must be updated if a newer version of the data is to be distributed.

# Data Labeling #

In order to get the correct data we want, we must be able to:
  * Find the appropriate unique label for the named data
  * Find the correct data that's associated with the unique label

Both the connection between the unique label according to the naming (VJ's current-day example is "www.newyorktimes.com/today" -> "www.newyorktimes.com/20070402/index.html"), and the connection between the label and the correct data, can be simple signed artifacts distributed as meta data items in the network themselves.

# Data granularity #

Data should be divided into small packets not only for transmission "on the wire", but also in its storage on the network. This allows:
  * More effective distribution of the data via multiple pipes and from various sources.
  * Allows prioritization and QoS between pieces of data, both in storage and transmission.

# Storage as part of the network #

Today, only "hot potatoes" (packets of data that are "on the wire", or in a transmission buffer/queue of a router/host) are considered data in the network. There is no long-term memory of these packets.
In a data-centric network, long-term storage (e.g disk storage) of the data is also a part of the "network" and may serve requestors of that data in the future.
VJ's example involves a large telcom refusal to route certain data packets over their backbone routers being worked-around by automatically sending the data to a nearby air-plane. This air-plane will store the data on its disk, and make it available again in its destination. (This is reminiscient of Tanenbaum's "Never underestimate the bandwidth of a truck full of backup tapes").

# Rigidity of the TCP/IP addressing scheme #

The internet is famous for its ability to automatically update available routes according to new links and crashing links around the network.
However, the internet is not so versatile when it comes to its addressing scheme. Its addressing scheme is much more rigid, as addresses must correspond to the network topography.  Any deviations from the topography are costly in the routing tables all over the internet - often to the point of impossibility.
Even if an address (or address range) topographic location is to be updated, updating it is necessarily a slow and involved process as a limited number of such large-scale changes can occur in the entirety of the network.

This means that changing your topographic location in the network (e.g moving and connecting to another Wi-Fi network) requires changing your address. Since today's network is only aware of the addresses of the endpoints to which it routes data, any change in geographic location, which thus requires a change in the network's topographic location, means that all communications must be re-established.

In a data-centric network, the endpoint topographic address to which data should be sent is a transparent artifact determined automatically by the network according to the data that needs to be exchanged.

# A potential slight improvement #

A potential slight improvement to the idea (which may not be an improvement depending on the efficiency of the implementation of the algorithms involved and the requirements) would be to create a redundant set of "packets" for a given piece of data such that any subset of different packets of the original data size would be usable.

**TBD: refer to an explanation and the name of the mathematical technique**

# Potential implementations #

Having agreed that data awareness of the network allows for more efficiency - how do we go around to implementing this?

Many questions arise:

  * Should data be distributed and stored lazily and only in nodes through which it happened to pass or should it preemptively be sent to anticipated requestors to allow for network distribution?
  * How long should data persist? Should data persist according to its' requests popularity?
  * In case preemptive distribution is used, should it compete for network and storage resources of the network? Is it possible for it to be placed at a lower priority such that it only utilizes idle links and unused disk space?
  * What kind of new security concerns may this arise, with regards to DoS attacks?

## More Bogus Questions ##
  * Does long-term memory of network packets raise privacy issues? (If this memory can be examined to determine the types of requests made by segments of the network)
  * Routers have somehow been made exempt from copyright as they copy copyrighted content to each other on the wire.  Will this exemption be allowed for long-term storage of data as well? What is the copyright status of The Internet Archive?

# Integration with Enough #

I think Enough has a better basis for a data-centric network than today's computing world. Enough has got a high-level object model of which the platform is aware. The division between code and data components, down to the most fine-grained level is something the platform is aware. Versioning schemes of this data is also in the realm of the platform's understanding. This allows for the labeling of such components, their meaningful division into high-granularity "packets", their versioning to be done automatically and in a transparent uniform way, regardless of the type of data.

Enough's main way of expressing network use is via [NetworkReferences](NetworkReferences.md). Network References can be divided into multiple categories:
  * A reference to the newest version of an object (A Name and a signer [i.e Public Key of a provider of labels for this Name])
  * A reference to a specific immutable version of an object (A Label and a signer)

A reference to an immutable object and one to a mutable object are very different.  The first refers to a specific version of an object - and does not at all care where the object is (its a reference to the object - wherever it may be - like an emule file hash). The second is a reference to an object in a specific location - because it may need to mutate it.

The use of references can then be divided into multiple categories:
  * Mutation/Active side effects
  * Read-only

Only the first type of references are usable with the first type of use, and only the second type of references are usable with the second type of use. The first type of references, however, are convertible to the second type (which is desirable anyhow, in order to identify the source of any functional computation and be able to repeat it deterministically).

In the first type of references, the object does have a "true location", as it is mutable and is modified "in-place".  Therefore, such references must contain an endpoint as well as an object identifier.

In the second type of references, there is no "true location" as the data is immutable and can be received from anywhere, and persist in any location in the network.

# External references #

A Google Tech-Talk by Van Jacobson that explains this idea: http://video.stumbleupon.com/#p=17d2ylezm3