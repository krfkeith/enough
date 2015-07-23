# Background #
The external relation between syntax and meaning has a price. There are several limitations and problems.

Most programming languages have a textual syntax. The programmer must express the program as a text file containing the source code, and uses a compiler or interpreter to transform this text into a semantic model which is later translated into a machine-runnable representation.

You may also read [Syntax and Semantics](SyntaxAndSemantics.md), which is about syntax and semantics in general.


# Syntax can be hard to use #
In some languages (such as written French and Perl) the syntax often causes frustration. In French, the syntactical expression of single words (spelling) is very **hard to learn** for a newcomer. So is the French syntactical representation of decimal numbers. In Perl, the problem is that the syntax allows **too many** different ways to specify a single meaning. Of course one can write completely comprehensible programs in perl. But perl allows otherwise, and soon enough this happens, either intentionally (which is ok, because that's what the author wants. See the [Perl Camel](http://www.perlmonks.org/index.pl?node_id=45213) by [Stephen B. Jenkins](http://www.Erudil.com)) or because the programmer doesn't value readability (the much more common and very bad case).

# Syntax limits the language #
The syntax imposes restrictions that the language's semantics don't, restricting our thinking and the language's power. These restrictions are typically not brick walls, but can be worked around. Nonetheless, they still discourage use of certain semantic structures and limit the programmer.
For example, Python's nested function scoping. In Python it would be very easy to express write access to a variable that exists in the scope of an outer function, but due to syntatical limitations, this is not possible and difficult workarounds must be used.  Also impossible is access to variables of sibling function run instances, and so on.
Another example is the virtual function table. It is a very useful way to implement [Polymorphism](Polymorphism.md), but C's syntax adds so much overhead to its syntatic declarations, that most people using C avoid it as much as they can.

# Syntax allows more errors #

Expressing a program correctly according to the specified syntax is not trivial, and there are almost always time-consuming errors.

## Syntax errors ##
Every syntatic mistake (such as forgetting a semicolon) in the text file may lead to _compilation errors_. Thus, the programmer is forced to waste time on "arguing" with the compiler about semicolons, commas and typos (and unfortunately the compiler is always right).
A time-wasting example in C is forgetting a semicolon after a struct in one header file and receiving many errors in another unrelated file. This problem has its roots in the syntactical rules of source file processing.

## Semantic errors caused by bad syntax ##
A worse case is when a syntax error causes a change in the _semantic_ meaning of the program. Here, the program compiles and to the programmer's eye, everything looks fine. Only later (if at all) will the programmer discover that the program is not what he meant it to be, and all because of a typing mistake. The = vs. == example in C is classic - the program compiles and runs but either crashes or acts in an unintended fashion.

# Syntax limits programming aids #
The fact that programs are encoded as text also makes it hard to write tools that aid the programmer by understanding what the code is about. Tools that want to aid the programmer often must work at the semantic level, and therefore must parse through the textual representation.  This adds significant complexity and therefore reduces the quality of the aid that can be given the programmer by the development environment.  The problem is made worse by the fact that the program is not syntatically correct while it is being edited, making the parsing job of the editor a nightmare and limits it even further.

# Syntax makes editing offline #
Programs that are encoded as text are not syntatically correct while they are being edited.  This results in the editing necessarily being "offline" and thus the programmer cannot get "real-time" updates of the program's meaning and execution as he is editing it.  Avoiding syntax and editing the semantic model of the program directly allows the program to be continously valid and thus have a runnable semantic tree at every given moment. This allows showing the programmer the result of his work incrementally and with every minor change made.  This reduces the need for the programmer to visualize the data flow in his head as he is writing the program, as it can be incrementally shown to him while he is editing the code.

# Syntax makes large modifications (even more) difficult #
After a textual source is written, it is very hard to modify the structure of the program.

  * If we want to move a whole set of objects to a different module, we will have to cut and paste the source manually. The complex semantic model encoded by the text contains a lot of cross-referencing, and because of the textual representation, these references must be encoded as unique names within a [scope](scope.md). Both the uniqueness and the scope tend to break when textual representation of code is moved around.
  * If we want to change the name of an object, we will have to search and replace for a textual string, usually through many files, and make sure we only modify those cases where the name actually refers to our object and not to a different one with the same name. As mentioned, there are "refactoring" tools that can ease this task. They can't be perfect - they would need to parse the text in order to know where it is possibly correct to change the name and where it isn't, and even this wouldn't be entirely correct. The tool can not know if the name refers to the same object or to a semantically similar one. To make the problem worse, virtually all of the available source control/versioning tools are unaware of the semantics encoded by the text, so that even if the rename is done perfectly, it may still break when a marge occurs between the work of different programmers.

# Current solutions are ad-hoc #
The currently abundant solutions to the problems mentioned only scratch the surface. They usually treat problem seperately, and solve only one problem, and only partially. Also, because of the overhead - every developer of a new code tool has to solve these problems again - people develop less tools and less advanced tools.

# Summary #
Syntax imposes a lot of problems, and we believe they can be solved by what we call [Live Programming or Semantic Editing](LiveProgramming.md).

# Main references #
  1. Ferdinand de Saussure (1916). _The Course of General Linguistics (Cours de linguistique générale)_
  1. _[Semantics](http://en.wikipedia.org/w/index.php?title=Semantics&oldid=107257033)_ in Wikipedia
  1. _[Manifesto of the Programmer Liberation Front](http://alarmingdevelopment.org/?p=5)_ Jonathan Edwards (June 16, 2004)