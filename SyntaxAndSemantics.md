# Syntax and semantics #
Every language (not just programming) has several seperate levels or layers, two of which are: syntax and semantics. The syntax layer is the "visible" part of the language: it defines how you write or say what you mean. The semantic layer is the part that determines the underlying structure of the language.

## Syntax ##
The syntax has a mission: to convey a meaning. It has no inherent meaning - the meaning of a given syntax is what people agree upon.

Syntax is actually an artificial requirement. It exists for the sake of communication. For two parties to understand each other, meaning must be expressed in some form that both sides understand. Even for a single person, syntax may be required for some complex problems that are hard to consider completely at once. In this case the person can write down some of his thoughts, and communicate with himself. In any case, syntax is not part of the meaning (the example of using different syntactical forms in one language, for the same meaning, is a good proof).

In English, the "if...then" construct has a written syntax and a "hidden" semantic meaning. A common syntax is **if** _a_ **then** _b_, where _a_ and _b_ should be syntactically correct English expressions. The _meaning_ of an "if...then" sentence is it's semantics. You may agree to write "If you are stupid, then go away" or "Go away then if your are stupid". A non-standard (and therefore possibly "incorrect" English) syntax can be defined as follows, without using the words "if..then": "you are stupiiid go away". The triple-i spelling mistake in a word signifies "if..then". Or "moo 45!! anti-monsters extereme you are stupid _KFKSA go away"._

**The point** is that syntax is agreed upon to express a certain meaning. Therefore, syntax is arbitrary (besides practical considerations).

In programming languages, a similar principle applies. In C, code with _the same semantics_ for a condition can have a different syntax:
```
if (expression)
   statement_for_nonzero ;
else
   statement_for_zero ;
```
or:
```
expression ? statement_for_nonzero : statement_for_zero ; 
```
These two syntactical forms have (for our discussion's sake) identical meaning, but not identical syntax (in fact more syntax options exist in C to express the same meaning)

## Semantics ##
If syntax is the physical structure of expression, semantics can be loosely defined as the mental structure of the _meaning_. It is not the same to think of a cat as an animal, and to think of a cat as food (yuck!!). Similarly, it is not the same to think of a program in terms of procedures, and to think of the same program in terms of objects.

### Differing semantics ###
#### Similar but different meanings ####
In natural languages we often have similar but not identical semantics. "If you are stupid, go away" means one things, but "A person who is stupid should go away" means something else. The meaning is similar but not identical. Or we could say "If you _think_ you are stupid, go away". This too has a different meaning (the person could be stupid but not think it). The diversity of semantics allow us to express different meanings.

For computer languages, this is like the difference (in Python) between:
```
if stupid in this_person.properties:
   this_person.go_away()
```
and:
```
for person in people:
   if stupid in person.properties:
      person.should_go_away = True
```
and:
```
if stupid in this_person.personal_self_opinions:
   this_person.go_away()
```
Forgive the silly example. These code pieces differ in their meaning.

#### Different semantics for identical objects of thought ####
The more interesting case is the one mentioned above, regarding procedural vs. object oriented thinking. Notice the word _thinking_. Semantics are more about how we think about something than about its manifestation. In science in general and also very much in software engineering, how you think about something is very important. In many cases, you think about the same problem in several different terms - different semantics.

For a programming example, let's return to the allegedly stupid person:
```
if stupid in this_person.properties:
   this_person.go_away()
```
This is an object-centered (object oriented if you must) point of view on the person. The same code can be written as:
```
if is_stupid(this_person):
   make_go_away(this_person)
```
This one is the more procedural point of view. In this simple example it may be less arguable (and not very important) which view is adopted.

The great question in software design is how to look at a given problem, and _in what context_, or which semantics, to solve it.

#### Thinking outside the language ####
In C, the concept of object orientation does not exist. The language _does_ supply the means to implement any object-oriented design of any system - but it does not contain the semantics. This means that you can think about objects and implement your code as objects, by defining functions in a way that conveys your intention. A common way to do this is with a struct:
```
struct person {
   ...
};

struct person *new_person(void) {
   ...
}

void destory_person(struct person **person) {
   ...
   free(*person);
   *person = NULL;
}

... other person "methods" ...
```
Here, we obviously think about 'person' as an object. But from a purely C standpoint, there is no such thing as an object. There are functions, variables, statements, expressions, etc. But no objects.

This is an example of thinking outside the language. In our mind (and conversations and documentation) we may use semantics that don't exist in the language we use to implement the program.