# Reflection: Profile Comparisons

## High-Energy Pop vs. Chill Lofi

These two profiles produced completely non-overlapping top-5 lists, which is exactly what you'd want. The High-Energy Pop user (energy target 0.85, valence 0.82) received Sunrise City, Gym Hero, and Rooftop Lights — all fast, upbeat, dancefloor-ready tracks. The Chill Lofi user (energy target 0.38, valence 0.58) received Library Rain, Midnight Coding, and Focus Flow — all slow, mellow study-session tracks.

The clear separation between these two profiles validates that the energy proximity formula is doing its job. A song like Spacewalk Thoughts (ambient, energy 0.28) appeared at #4 for the Chill Lofi user but did not appear at all for the High-Energy Pop user. This makes complete sense — the 0.57 energy gap would cost Spacewalk Thoughts over 0.85 points, effectively removing it from competition for the pop user.

## Deep Intense Rock vs. Adversarial (Jazz + High Energy)

This comparison is the most instructive. Both profiles want high energy (0.92 and 0.90 respectively), so you'd expect some overlap in the results. Indeed, Gym Hero and Bass Drop City appear in both lists.

The key difference is genre. The Rock user's genre bonus locks Storm Runner and Shatter Zone into the top two spots. The Jazz user's genre bonus pulls Coffee Shop Stories — a relaxed, 0.37-energy jazz track — all the way to #1 despite being almost maximally wrong on energy. This is the genre-dominance failure mode in action.

The lesson: when a user's preferences conflict internally (high energy + jazz genre), the system picks the attribute with the highest weight (genre) and largely ignores the rest. A human DJ would recognize this tension and ask a follow-up question. The algorithm cannot.

## Original Weights vs. Experimental Weights (Adversarial Profile)

Original weights (genre=2.0, energy=1.5): Coffee Shop Stories #1 (slow jazz wins on genre label alone).  
Experimental weights (genre=1.0, energy=3.0): Sunrise City #1 (high-energy happy pop wins on energy closeness).

Doubling the energy weight and halving the genre weight completely reversed the top result for the adversarial user — and the experimental result felt more correct. Someone who asks for high-energy music should not receive the slowest song in the catalog. This shows that weight choices encode assumptions about what users "really mean," and those assumptions can be wrong.

## What Would Make This Feel Like a Real Recommendation?

A real recommender would not have to choose between genre and energy — it would have behavioral data. If a jazz-preferring user keeps skipping slow tracks and finishing fast ones, collaborative filtering would pick up that signal and surface energetic songs even from outside jazz. The content-based system used here has no memory of what the user actually did, so it can only guess based on the static profile. That gap between "what the user said they want" and "what the user actually does" is where most of the interesting problems in real recommendation systems live.
