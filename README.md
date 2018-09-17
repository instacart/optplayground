# Optimization Model Playground

## Why we need this?

Many optimization model can be NP-hard/NP-complete, i.e., solving them can literally take forever, but "finite", time. An inner problem of Instacart's logistics system can be considered as a super complicated, stochastic vehicle routing problem with several business constraints, such as time window, heterogeneous fleet, multi-trip, multi-depot, etc. It is clearly unrealistic to pursue the global optimal to this NP-complete problem with the presence of random variables. One practical way to tackle the business problem is to decompose the large problem into several small problems, solve each small problem to its best, and construct smart algorithmic processes to reach a solution.

The bad news is that many of our decomposed problem are still NP-hard/NP-complete. One good news is that these problem are often investigated thoroughly and there can be ways to solve them more efficiently. Another good news is that these models are highly data-driven, i.e., efficient solution method can be developed if we get to learn the data better. To accomplish this, we need to develop and learn regulated optimization models that can be flexible with datasets.

This purpose of this repo serves to provide easy accesses to several regulated optimization models that our system encounters on a daily basis. The long-term goal is to build a study base of optimization problems we solve and provide valuable do and do not suggestions for people seeking opportunities in solving Instacat's challenge better.

## Modeling Environment

* Pyomo in Python
* JuMP in Julia

## Existing Problems

* Traveling Sales Man Problem
* Set partition Problem
* Assignment Problem

## Usage
TBD

## Reports
TBD

## Bugs and Requests
TBD
