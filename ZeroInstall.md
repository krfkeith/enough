# Background #

Traditionally, in order to make a piece of software runnable on a computer, the software would have to be "installed" on that computer.

In order to install the program, programs typically have an extra installation program, that performs the above actions.

Zero-Install is a method of representing, running and copying programs in a way that does not require installation or executables.

# The various forms of a traditional program #

A traditional program has many representations:
  * The program's source code
  * The program's executable
  * The program's installer
  * The program's running state

One of the aims of the Enough project is to unite as many representations into a single universal representation of the program, which is both edited and used directly.

LiveProgramming and UnifiedInterface already unite the Program's source code, executable and running state into one editable running object.

ZeroInstall, along with OrthogonalPersistence aims to also get rid of the installer so that programs only have one representation.

# The roles of the installer #

"Installing" a program will always include:
  * Copying its components to the computer
  * Placing it into the menus and program listings
And sometimes it will include:
  * Asking the user some questions to initially configure the application
  * Downloading extra components

## Copying its components to the computer ##

As demonstrated in AdaptiveProfiling, components are easily moved and copied between computers, with any necessary translation done transparently (such as regenerating native code for a target platform). Copying the components would then become either an explicit operation or it could be done seamlessly and implicitly by using the component and letting it be copied directly.

## Placing it into the menus and program listings ##

As discussed in GraphicalInterfacePrinciples, Enough will not have a notion of global menus into which to insert programs.
To replace those, a relational database of objects will exist, in which the user can search for objects by arbitrary attributes.
In order to allow for the copied components to be properly registered into the local database (if the program is seamlessly copied then it was already found by the user in a non-local database), the copying of the program can be done via a database copying method (which can be invoked by dragging the program into the database, for example) which could combine the copying of the objects with the registration of the objects' metadata into the database.

## Asking the user some questions to initially configure the application ##

Initial configuration should always be changable at a later time. This means that this configuration data should be editable after installation as any other data component. This makes the initial configuration invocation a mere recommendation at "installation time". To facilitate such configurations, the configuration data component may contain a special metadata attribute that means "when I am copied into a database, please allow the user to access me".  This would allow the database to expose this special sub-component to the user as it is copied to the database.

## Downloading extra components ##

This current feature of installers is less of a feature for the user, and more of a feature for program publishers to ease the distribution of the latest version to users. Instead, a [NetworkReference](NetworkReferences.md) to the latest version of the component from its distributor can be copied, such that the most recent version is always copied (Note that _download_ and _copy_ are interchangable).

# Summary #

Using the above methods, the installer program is replaced by some metadata attributes that are attached to the objects being copied.  The author, version, name and other metadata attributes may be specified there so they are later searchable in the database.
These metadata attributes would become searchable in the local database only if explicitly copied into the database by invoking its copying method, and not if the object is seamlessly copied when used from another computer. If it is seamlessly copied, then the copy is treated as merely a cache.

Due to [seamless copying](AdaptiveProfiling.md), many explicit installations in networked environments would not be necessary, as the OS would transparently "install" applications in an MRU fashion.