# Background: What is ACL? #

In short, an ACL (Access Control List) is a list that stores the permissions available to each user. They are the common way to manage security - used both in Unix-like systems and Microsoft Windows. An ACL is a list of permissions for each user. Typically, every resource has a list of which users are allowed to access the resource and with what permissions.

The actual entities that access resources, however, are not users, but programs. Therefore, each program is assigned a user that it is "running as". This determines the set of permissions that the program has.

In an ACL system, no special privileges are required in order to **request** access to a resource.  When a program requests access to a resource, the ACL is checked whether to allow the request. For example, if a program tries to read a file, the OS will check if the user the program is "running as" has "read" permissions on that file. If the user does not have enough permissions, the operation will fail with a problem such as "Access Denied".

# The Better Approach #
The better approach to security is [Capabilities](Capabilities.md).

# Problems #
There are fundamental problems with ACLs. Those manifests in several ways:
  * Resource control: There are vast amounts of resources in the system, and each one must be attached a list of users. This is difficult to implement in terms of the required data structures and when describing un-enumerable resources (such as network addresses, email addresses, etc).
  * Users: Entities that make requests are not users, but programs. ACL systems assume that all authority that should be held by a user, should also be held by each of the programs he happens to run. For example: The media player should be able to delete or modify any media file that it can access.
  * Granularity: The granularity of ACLs is arbitrary, and is a constant trade-off between speed, space and security. This means that systems are either slower, or less secure. For example, many databases hold ACLs for every row in the database, which is a huge waste of space and requires more access time as well. Databases that fail to do this, are less secure.
  * How do you specify who is allowed to edit each ACL?  And who is allowed to edit the list of users that are allowed to edit the ACL?  Eventually you end up with an arbitrary list containing just the "object owner" or the "administrator". This adds another trade-off between security and administration difficulty.
  * Forgeability: it is possible to forge a reference to a resource that's supposed to be hidden. If permissions for that resource were not correctly specified, any malicious program will be able to access it. For example, if a new file was not created with correct permissions, a malicious program that tries to open that file by simply guessing its name correctly, will be able to do so.
  * Passing authority: In an ACL system, there is no way to pass authority between entities, other than by providing a proxy to it.  Since providing a proxy in order to provide authority is so complex in today's systems, "elevated privilege" is typically used instead. This means that a program that wants to pass data to the printer program cannot pass it authorization to access its files, and therefore the printer program must run with "elevated privileges" that can access all data. Even if the printer program is trusted, it still results in the Confused Deputy problem.

# The Credit Card Metaphor #
Finally, the problem can be described with a metaphor: ACLs are akin to giving out your credit card number to everybody, and then having a list in the bank managing who is and who is not allowed to charge your credit card.

Sounds stupid, right? Nevertheless, this is how all our operating systems work.

(In fact, the real credit card system _does_ work this way, because every time you buy something they get your credit card number and can charge you as much as they want, any time they want. This is why credit card fraud is possible.)

## In a world of capabilities ##
Capability systems mean that you simply never give away your credit card number. You only give it to someone if you want to let them charge your account. If you didn't give it to someone, they can't charge you, and this does not depend on the correctness of any list.
In a typical capability system, after they charge you, you kill them so they can never use that number again or tell it to anyone.  However, that may be the point where analogies break :-)

# See Also #
[Wikipedia on ACLs](http://en.wikipedia.org/wiki/Access_control_list)