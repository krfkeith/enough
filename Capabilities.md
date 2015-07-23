# What are Capability Systems? #

In short: capabilities mean **granting authority for specific tasks** instead of the currently used opposite - preventing authority for everything else.

Wikipedia seems to have a good entry: http://en.wikipedia.org/wiki/Capabilities

# Mainstream security #
The mainstream in security these days is using ACLs to validate access to objects.
[ACLs are a bad way to implement security](WhyACLsAreBad.md).

# Security via Capabilities #
As mentioned before, capabilities could be summarized as granting authority for specific tasks instead of preventing authority for everything else. This means that if someone (or a program) needs to do something, it will receive the authority to do only that, and no more. Today, most systems use the opposite - they start from allowing virtually everything and then they restrict specific things.

With capabilities, no "security permission checks" are necessary. If you don't explicitly give the application references to internet connections and your secret documents, they can't even _express requests_ to operate on them.

In terms of _references_, capability systems are systems in which an object can not perform operations on other objects because it can not know how to reference them. Thus, a capability can be described as a reference. If you don't have a reference to an object, you can't access it.


# Unification of designation and authority #
In today's world, objects are designated by programs via resource identifiers, which are overt and forgeable. A program designates an object, and the operating system verifies that access is allowed against the ACL.  With capabilities, the only way to designate an object is via a capability. A capability also represents the authority to access that object. Thus, the designation of an object and the authority to access that object are united into one artifact: The capability.  This way, a program only contains a list of objects it can access, without any reverse list to verify it.
The consequences are:
  * A simpler system that contains only designation, without extra mechanisms for verifying authority.
  * A more powerful system that allows fine-grained control over which piece of code can access what objects.
  * [A natural way to extend this on to a network](NetworkReferences.md).

In a real-world system, that would mean that the user operation of designating an input file for a program (i.e: a media file to the media player) would also pass authority to access that file to the program, which would otherwise be unable to request access to the file.  That way, the user does not worry about what he wants to do AND allowing the security of doing it. Implicit authority is passed selectively according to what the user is doing. This would eliminate a lot of the security dialogs, while implementing much more closely the principle of least authority.

# Limited access to objects via capabilities #
Capabilities also allow control of permissions with much finer granularity. One of these control methods are called _facets_. A facet is a proxy to an object, that only allows a subset of the functionality. Instead of giving a capability to an object, one can give a capability to a facet. The facet may later be nullified to revoke the capability, or the permissions may be changed dynamically.

This allows any object holder to create a capability to a limited-subset of the object, without requiring any secure code in the operating system to be written for those specific restrictions.

Here is a simple example. Assume you have a document. You wish to allow access to the document but only to a specific portion. With current security technologies that is impossible - you have to replicate the document and restrict the permissions on the copy or allow access to the full document, because the document is a single file. Capabilities do not place such artificial restrictions on the security management. With capabilities, you would simply create a _facet_ of the document that represents the part you want to allow. You pass that facet around to people and that portion of the document is all they can reference. Also, using proxies of facets, you may even modify _which_ part or even which document they will access. You can modify the facet's target, post-distribution, to point to a different document. Or cause it to be active only during specific hours. The important fact is that you don't have to worry about specific lists for each resource - instead of managing resources, you are managing authorities.

For more on capability patterns, see [E in a walnut - Capability Patterns](http://wiki.erights.org/wiki/Walnut/Secure_Distributed_Computing/Capability_Patterns)

# Capabilities in Safe Languages #
An interesting property of safe languages, is that forging references to objects is not possible. This means that object references are very similar to capabilities.
However, various safe languages have various problems that prohibit their references from being real capabilities.

For example, Java allows casting a reference up and down freely, which allows enhancing access to an object to the full subclass with all of the methods available. This is workaround-able by creating a _facet_.

Another example is Python: It allows free access to the referred object, without limitation. This includes all of the object's internal implementation details. This makes facets impossible to implement in Python.

## Requirements of a safe language ##

In order for a safe language to support capability security, it must support:
  * Unforgeable references.
  * Private object attributes that cannot be accessed by a normal object reference.
  * Limited access to only the object methods via a normal reference (no "casts" must be allowed)
  * No global scopes from which to pry references to random objects.

The above requirements are not satisfied by most safe languages, and therefore most are not suitable for implementing capability security.

Satisfying the above requirements, however, should not be difficult, as long as it is taken as a design requirement through the entire design process of the language.

# Primary references #
See the [main project page](http://code.google.com/p/enough/) for more.
  * [Robust Composition](http://www.erights.org/talks/thesis/index.html): Towards a Unified Approach to Access Control and Concurrency Control, dissertation by Mark Samuel Miller, Johns Hopkins University, May 2006
  * [E in a Walnut](http://wiki.erights.org/wiki/Walnut) by Marc Stiegler

# More resources #
  * [Narrated Intro](http://www.skyhunter.com/marcs/narratedIntros.html) by Marc Steigler (from E)