# Introduction #

The computer is an information processor. As such, it must process inputs into outputs. In many cases, especially ones encouraged by LiveProgramming and a UnifiedInterface, the inputs are incrementally modified and not completely replaced.  Normally, this would mean re-running the entire computation on the new incrementally modified input.

A more efficient solution is to run a slightly modified algorithm, a differential algorithm, on the modification, rather than the new input, so it can modify the output instead of recomputing it entirely.

While a normal algorithm (or processor) processes the input it receives, a differential algorithm processes **differences** to the input it receives.

Differential computing raises the issue of [ComputationVsStorage](ComputationVsStorage.md).

## Some examples ##

A computer's media collection is often sorted by title, author, and time.  When adding new media to the collection, the sort must not break. In order for this to occur, most programs incorporate special logic for the insertion of the media into the collection that does not break the sort - or they rescan the entire collection slowly whenever it is changed.
In Enough, one would simply connect the media list to a sort function.  When new media is added, it is re-sorted. In order to avoid an expensive resort of millions of media titles, authors and times, a differential algorithm is always used.  The processing only occurs on the new media title.

# Differential properties propagate #

In order to allow differential computation of inputs to be used, everything must be differential.  Fortunately, input processing into outputs will almost always be a functional program with no side effects.  If a function is processing its inputs via differential functions, then it too becomes differential.
In fact, the function may not and does not have to appear to be differential, but by merely using primitives that are themselves differential, it becomes differential as well, and thus efficient at processing changing inputs.

# Example implementation: A sort algorithm #

A typical sort algorithm takes a collection of elements, performs between N and N\*log(N) comparisons between these elements, and results in a sorted sequence.

A differential sort algorithm would look to the user as though it was a normal sort algorithm, with a normal element collection input and sequential output, but in actuality it will process modifications to the input collection.

When the input is changed, the modification is expressed as "element X added", "element X removed" or "element X changed with: C" (where C would be a recursive expression of a modification of the element). The sort function will process that modification and generate an output modification: "element at position X moved to position Y", or "element at position X removed", or "element X added to position Y".
The sort function would have to be written in a way that is aware of these different possible modifications (unless it can be expressed with lower-level differential primitives) to know how to express the output modifications.

However, users of this sort function use it as though it takes a collection and outputs a sequence, and not modifications.  They implicitly become differential themselves as they do this.

# Consequences #

The consequences of using differential computing are:
  * Since most functions can use existing differential primitives, the functions can become efficiently differential without any extra effort by the developer
  * The common use pattern in a UnifiedInterface and LiveProgramming, of modifying the inputs would be more efficiently processed (rather than reprocessing the entire input at every change).
  * The Enough GUI could avoid quirky jumps when inputs are modified, as these modifications propagate through the processing. The sorted output elements could smoothly move around, visualizing the modification for the user, rather than creating a new result immediately.
  * The modifications can enable efficient version control, without writing extra differential code.