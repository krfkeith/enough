# Introduction #

Enough's purposes and scope are replacing virtually the entire body of software in existence. Obviously this is a huge task and cannot be done as one single step.

# Steps of the plan #

## Step 1 ##

Develop a code editor in Python that features:
  * SemanticEditing
  * Unifies similar semantic models (such as C#/Java), allowing multiple syntatic frontends for them
  * Requires less key presses for all common operations
  * Revision control, including merges, conflict handling, and generates far fewer conflicts

## Step 2 (Optional) ##

Re-implement the editor in the lower-level language via the editor, to be self-hosting.
This can be a proof-of-concept project for the editor, to see that it works for real-world projects.

## Step 3 ##

Design a new language in the spirit of Subtext 1 (mostly functional, side effects are new revisions, etc).
Create a fork of the editor that edits this language with LiveProgramming.

## Step 4 ##

Reimplement the editor in the LiveProgramming language, to be self-hosting.

## Step 5 ##

Add network transparency. References to objects can be either local or remote. API's and protocols are inter-changable.

## Step 6 ##

Extend the UI of the LiveProgramming editor, such that it can be used with a very slight learning curve, and add UI features such as:
  * Default actions/functions to handle various datatypes
  * Double-clicking to invoke the default function
  * Grouping of objects that are commonly used in day-to-day tasks

The purpose of this stage is to make the LiveProgramming environment a desktop environment.

## Step 7 ##

Implement AdaptiveProfiling. This should allow for the network-transparent object system to replace the web, file servers, and various other protocols with far more efficient adaptive setups.

## Step 8 ##

Implement a native code compiler and JIT for the live language.

## Step 9 ##

Add a new semantic model that can be used to access platform-specific features.
Implement a kernel and drivers that provides the facilities required by the environment's implementation.

# Result #

The result of this plan should be a self-hosting Operating System, Desktop Environment (User interface), Programming Language and Network collaboration system.

All principles outlined by EnoughWorld should be possible after this plan.
TODO: Explain how each step makes some stuff in EnoughWorld possible.